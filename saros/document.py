#!/usr/bin/python

from .database import _SarosDB
from .xml import _Attribute, _Element

class _Name:
    # represents a doc's name.
    def __init__(self, name):
        self.__name=name

    def _link_revs(self):
        # assembles all revsion chains associated with a `self.__name`, and 
        # works with other classes to link broken revision links.

        # algorithm groups revisions by their last revision.
        # each group is a rev chain, & if we've > 1, we've broken rev chains.
        # rev_chains = { last1: [rev, rev, .., rev],
        #                last2: [rev, rev, .., rev], ... }
        rev_chains={}
        for (rev, last) in self.__last_revs():
            if last not in rev_chains:
                rev_chains[last]=[rev]
            else:
               rev_chains[last].append(rev)
        _RevisionChains(rev_chains)._link(self)

    def __last_revs(self):
        # gathers "last" for all revisions of doc named `self.__name`;
        # returns an unordered [ ("rev", "last") ]
        #
        # last_revs = [ (rev, last), .., (rev, last) ]
        # NOTE: last_revs is unordered either by rev or by last
        return _SarosDB()._last_revs(self.__name)

    def _update(self, rev_links):
        # updates revision links in Saros
        for each in rev_links:
            doc_xml=each._to_xml(self.__name)
            _SarosDB()._load(doc_xml)


class _RevisionChains:
    # represents a doc's revision chains.
    # spots unlinked revisions, & generates correct revision links;
    # calls `Name` to update correct links in Saros.
    def __init__(self, rev_chains):
        # revision chain: 1 or more revisions grouped by their last revision.
        # self.__rev_chains = { last1: [rev, rev, .., rev],
        #                       last2: [rev, rev, .., rev], ... }
        self.__rev_chains = rev_chains

    def _link(self, name):
        # identifies & links broken revision chains
        #
        # if we've > 1 revision chain, we've broken revision chains.
        if self.__no_broken_links():    # skip if no broken links
            return
        name._update(self.__correct_rev_links())

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


class _RevisionLink:
    # represents a valid revision link
    def __init__(self, prev, rev, last):
        self.__prev=prev    # "rev"'s previous revision
        self.__rev=rev      # revision
        self.__last=last    # last revision in the chain "rev" belongs

    def _to_xml(self, doc_name):
        # generates document xml corresponding to this revision link
        self.__validate()
        doc_xml="./saros/temp/"+doc_name+"-"+str(self.__rev)+".xml"
        _SarosDB()._doc_xml(doc_name, self.__rev, doc_xml)
        with open(doc_xml, 'r') as reader:
            data=reader.readlines()
        with open(doc_xml, 'w') as writer:
            for line in data:
                line=line.rstrip()
                name, _ = _Element(line)._parse()
                if name == "prev":
                    writer.write(_Attribute((name, self.__prev))._to_xml())
                elif name == "last":
                    writer.write(_Attribute((name, self.__last))._to_xml())
                else:
                    writer.write(line)
                writer.write("\n")
        return doc_xml

    def __validate(self):
        # validates the link
        if self.__rev <= 0 or \
                self.__rev != self.__prev + 1 or \
                self.__last < self.__rev:
            raise RuntimeError("invalid revision link: " + \
                "prev: " + str(self.__prev) + " "  \
                "rev: " + str(self.__rev) + " " \
                "last: " + str(self.__last))

