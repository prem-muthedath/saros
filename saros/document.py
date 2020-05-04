#!/usr/bin/python

from .database import _SarosDB
from .xml import  _File

class _Document:
    # represents a document, one identified by a given name.
    # this class links all unlinked revisions associated with a document name.
    def __init__(self, name):
        self.__name=name

    def _link_revs(self):
        # links all unlinked revs of `self.__name` to form a single rev chain.
        links=self.__valid_links()
        # broken rev link is where a rev is without a valid prev.
        # skip first link, however, as its rev can not have a prev.
        # so we loop from [1:], but index starts @ 0, so index -> prev item.
        for index, link in enumerate(links[1:]):
            prev=links[index]
            link._linkTo(prev, self)

    def _dump_file(self, rev):
        # name of file holding Saros dump of doc having `self.__name` & `rev`
        _file=self.__name+"-"+str(rev)      # file name
        _SarosDB()._doc_dump(self.__name, rev, _file)
        return _file

    def __valid_links(self):
        # validated revision links associated with `self.__name`
        valid_links=[]
        for index, link in enumerate(self.__saros_links()):
            rev, last = link
            if rev <= 0 or last <= 0:
                raise _NonPositiveLinkError(self.__msg(link))
            if last < rev:
                raise _LastBelowRevisionError(self.__msg(link))
            if index > 0 and link == prev_link:
                raise _DuplicateLinkError(self.__msg(link, prev_link))
            if index > 0 and last < prev_link[1]:
                raise _DecreasingLastError(self.__msg(link, prev_link))
            if index > 0 and rev != prev_link[0] + 1:
                raise _NonConsecutiveRevisionsError(self.__msg(link, prev_link))
            prev_link=link
            valid_links.append(_Link(link))
        return valid_links

    def __saros_links(self):
        # Saros revision links for doc `self.__name`, sorted by `rev`.
        # revision links = links = last_revs = [ (rev, last), .., (rev, last) ]

        # NOTE: last_revs from Saros db are unordered either by `rev` or by 
        # `last`, but this routine sorts them by `rev` in ascending order.
        saros_links = _SarosDB()._last_revs(self.__name)
        return sorted(saros_links, key=lambda(rev, last): rev)

    def __msg(self, this, prev=None):
        # error meesage
        if prev:
            return ", ".join([self.__str(),
                            "prev (rev, last): " + str(prev),
                            "this (rev, last): " + str(this)])
        return ", ". join([self.__str(), "(rev, last): " + str(this)])

    def __str(self):
        # string representation of _Document
        return "document: " + self.__name


class _Link:
    # represents a revision link -- `(rev, last)`
    # it links a broken revision link in Saros.
    def __init__(self, (rev, last)):
        self.__rev=rev
        self.__last=last

    def _linkTo(self, prev, doc):
        # if unlinked, links itself to its previous revision in Saros.
        linked=self.__last==prev.__last
        if not linked:
            _file=doc._dump_file(self.__rev)
            _File(_file)._update(self.__rev-1, self.__last)
            _SarosDB()._load(_file)


class _LinkError(Exception):
    # represents link error
    def __init__(self, msg):
        # msg: error message
        self.__msg=msg

    def __str__(self):
        # string representation of _LinkError
        return self.__msg.__str__()

class _NonPositiveLinkError(_LinkError):
    # represents `rev` < 0 or `last` < 0 in `(rev, last)` error.
    pass

class _LastBelowRevisionError(_LinkError):
    # represents `last` < `rev` in `(rev, last)` error.
    pass

class _DuplicateLinkError(_LinkError):
    # represents duplicate `(rev, last)` error.
    pass

class _DecreasingLastError(_LinkError):
    # represents `last2` < `last1` in `[(rev1, last1), (rev2, last2)]` error.
    pass

class _NonConsecutiveRevisionsError(_LinkError):
    # represents `rev2` != `rev1` + 1 in `[(rev1, last1), (rev2, last2)]` error.
    pass


