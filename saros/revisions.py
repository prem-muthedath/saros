#!/usr/bin/python

from .xml import _Attribute, _XmlElement

# this module contains private classes that work with revisions to identify & 
# fix a doc's broken revision links in Saros.
################################################################################

class _DocRevisionChains:
    # represents a doc's revision chains.
    # builds doc revision chains, spots unlinked revisions, & assembles correct 
    # revision links; works with other classes to update links in Saros.
    def __init__(self):
        # self.__rev_chains = { last: [rev, rev, ..., rev ] }
        self.__rev_chains = {}

    def _link(self, last_revs, saros):
        # identifies & links broken revision chains
        #
        # last_revs = [ (rev, last), .., (rev, last) ]
        # rev_chains = { last1: [rev, rev, .., rev],
        #                last2: [rev, rev, .., rev] }
        # NOTE: last_revs is unordered either by rev or by last
        #
        # algorithm groups revisions by their last revision.  Each group is a 
        # revision chain, & if we've > 1, we've broken revision chains.
        for (rev, last) in last_revs:
            if last not in self.__rev_chains:
                self.__rev_chains[last]=[rev]
            else:
               self.__rev_chains[last].append(rev)
        if self.__no_broken_links():    # skip if no broken links
            return
        rev_links=self.__correct_rev_links()
        _RevisionLinks(saros, rev_links)._update()

    def __correct_rev_links(self):
        # returns correct revision links to fix broken revision chains
        rev_links=[]
        lasts=sorted(self.__rev_chains)
        for each in lasts:
            self.__rev_chains[each].sort()
        for index, each in enumerate(lasts[1:]):
            # scan all rev chains for broken rev links & return corrected links.
            # broken rev link is where a rev is without a valid prev.
            # 1st rev in a rev chain is a broken link, because it has no prev.
            # skip first rev chain, however, as its 1st rev can not have a prev.
            # the 1st rev in all other rev chains is a broken rev link.
            # index starts @ 0, but we loop from [1:], so index -> prev item.
            prev_last=lasts[index]
            prev=self.__rev_chains[prev_last][-1]
            rev=self.__rev_chains[each][0]
            rev_links.append(_RevisionLink(prev, rev, each))
        return rev_links

    def __no_broken_links(self):
        # if we've broken revision links, we'll have > 1 rev chain
        return len(self.__rev_chains) < 2


class _RevisionLinks():
    # represents a collection of valid revision links
    def __init__(self, saros, links):
        self.__saros=saros
        self.__links=links

    def _update(self):
        # working with saros, update valid revision links in Saros repository 
        doc_xmls=[]
        for link in self.__links:
            doc_xmls.append(link._to_xml(self.__saros))
        self.__saros._update_rev_links(doc_xmls)
            

class _RevisionLink:
    # represents a valid revision link
    def __init__(self, prev, rev, last):
        self.__prev=prev    # "rev"'s previous revision
        self.__rev=rev      # revision
        self.__last=last    # last revision in the chain "rev" belongs

    def _to_xml(self, saros):
        # returns xml dump of current doc with right revision link info
        self.__validate()
        xml=saros._doc_xml(self.__rev)
        return self.__update(xml)

    def __validate(self):
        if self.__rev <= 0 or \
                self.__rev != self.__prev + 1 or \
                self.__last < self.__rev:
            raise RuntimeError("invalid revision link: " + \
                "prev: " + str(self.__prev) + " "  \
                "rev: " + str(self.__rev) + " " \
                "last: " + str(self.__last))

    def __update(self, doc_xml):
        for index, each in enumerate(doc_xml):
            name, _ = _XmlElement(each)._parse()
            if name == "prev":
                doc_xml[index]=_Attribute((name, self.__prev))._to_xml()
            elif name == "last":
                doc_xml[index]=_Attribute((name, self.__last))._to_xml()
        return doc_xml


