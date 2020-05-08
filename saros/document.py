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
        for i, link in enumerate(links[1:]):
            prev=_Link(links[i])
            _Link(link)._linkTo(prev, self)

    def _dump_file(self, rev):
        # name of file holding Saros dump of doc having `self.__name` & `rev`
        _file=self.__name+"-"+str(rev)      # file name
        _SarosDB()._doc_dump(self.__name, rev, _file)
        return _file

    def __valid_links(self):
        # validated revision links associated with `self.__name`
        links=self.__saros_links()
        for i, (rev, last) in enumerate(links):
            prev, plast=(0,0) if i==0 else links[i-1]
            data=links[i:i+1] if i==0 else links[i-1:i+1]
            if rev <= 0 or last <= 0:
                raise _NonPositiveLinkError(self, data)
            if last < rev:
                raise _LastBelowRevisionError(self, data)
            if (prev, plast) == links[i]:
                raise _DuplicateLinkError(self, data)
            if last < plast:
                raise _DecreasingLastError(self, data)
            if rev != prev + 1:
                raise _NonConsecutiveRevisionsError(self, data)
            data=self.__missing_links(prev, plast)
            if plast < last and len(data) > 0:
                raise _MissingLinksError(self, data)
            data=self.__missing_links(rev, last)
            if i==len(links)-1 and len(data) > 0:
                raise _MissingLinksError(self, data)
        return links

    def __saros_links(self):
        # Saros revision links for doc `self.__name`, sorted by `rev`.
        # revision links = links = last_revs = [ (rev, last), .., (rev, last) ]

        # NOTE: last_revs from Saros db are unordered either by `rev` or by 
        # `last`, but this routine sorts them by `rev` in ascending order.
        saros_links = _SarosDB()._last_revs(self.__name)
        return sorted(saros_links, key=lambda(rev, last): rev)

    def __missing_links(self, rev, last):
        # missing links
        return [(x, last) for x in range(rev+1, last+1)]

    def _str(self):
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
        linked=self.__rev > 1 and self.__last==prev.__last
        if not linked:
            _file=doc._dump_file(self.__rev)
            _File(_file)._update(self.__rev-1)      # update prev value
            _SarosDB()._load(_file)


class _LinkError(Exception):
    # represents link error
    def __init__(self, doc, data):
        # doc: _Document object
        # data: `[(rev, last)]` related to error
        self.__doc=doc
        self.__data=data

    def __str__(self):
        # err msg
        return self.__doc._str() + ", " + "[(rev, last)] -> " + str(self.__data)

class _NonPositiveLinkError(_LinkError):
    # represents `rev` <= 0 or `last` <= 0 in `(rev, last)` error.
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

class _MissingLinksError(_LinkError):
    # represents missing links `[(rev, last)]` error.
    pass

