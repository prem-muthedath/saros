#!/usr/bin/python

from .database import _SarosDB
from .xml import  _File

class _Document:
    # represents a document, one identfied by a given name.
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
            try:
                each._update(self)
            except _RevisionLinkError as e:
                msg=self.__str__() + ", " + e.__str__()
                raise _RevisionLinkError(msg)

    def __str__(self):
        # string representation of _Document
        return "document: " + self.__name

    def _dump_file(self, rev):
        # returns name of dump file -- file containing Saros database dump of 
        # doc named `self.__name` & revision `rev`
        _file=self.__name+"-"+str(rev)      # file name
        _SarosDB()._doc_dump(self.__name, rev, _file)
        return _file


class _RevisionChains:
    # represents revision chains assciated with a _Document.
    # spots unlinked revisions, & generates correct revision links;
    # calls `_Document` to update correct links in Saros.
    def __init__(self, rev_chains):
        # revision chain: 1 or more revisions grouped by their last revision.
        # self.__rev_chains = { last1: [rev, rev, .., rev],
        #                       last2: [rev, rev, .., rev], ... }
        self.__rev_chains = rev_chains

    def _link(self, doc):
        # identifies & links broken revision chains
        #
        # if we've > 1 revision chain, we've broken revision chains.
        if self.__no_broken_links():    # skip if no broken links
            return
        doc._update(self.__correct_rev_links())

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

    def _update(self, doc):
        # update link in Saros
        self.__validate()
        _file=doc._dump_file(self.__rev)
        _File(_file)._update(self.__prev, self.__last)
        _SarosDB()._load(_file)

    def __validate(self):
        # validates the link
        if self.__rev <= 0 or \
                self.__rev != self.__prev + 1 or \
                self.__last < self.__rev:
            msg = self.__str__() + ", " + self.__cause()
            raise _RevisionLinkError(msg)

    def __str__(self):
        # string representation of _RevisionLink
        return "prev: " + str(self.__prev) + ", "  \
                "rev: " + str(self.__rev) + ", " \
                "last: " + str(self.__last)

    def __cause(self):
        # probable cause for invalid link
        return "CAUSE: rev <= 0 or rev != prev + 1 or last < rev"


class _RevisionLinkError(Exception):
    # represents revision link error
    def __init__(self, msg):
        # msg: error message
        self.__msg=msg

    def __str__(self):
        # string representation of _RevisionLinkError
        return self.__msg.__str__()



