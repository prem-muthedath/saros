#!/usr/bin/python

from .database import _SarosDB
from .xml import  _File
from .errors import (_LinkError,
                        _NonPositiveLinkError,
                        _LastBelowRevisionError,
                        _DuplicateLinkError,
                        _DecreasingLastError,
                        _NonConsecutiveRevisionsError,
                        _MissingLinksError,
                        )

# document module contains classes to link revisions of a doc with a given name
# ##############################################################################

class _Document:
    # represents a document, one identified by a given name.
    # this class links all unlinked revisions associated with a document name.
    def __init__(self, name):
        self.__name=name

    def _link_revs(self):
        # links all unlinked revs of `self.__name` to form a single rev chain.
        # it spins through the revision chain, setting up objects to link 
        # revision pairs, and invoking `_link()` on them.
        # `_EndLink` handles checks @ end of rev chain that `_Link` can't.
        rev_chain=self.__saros_rev_chain()  # doc's `[(rev, last)]` from db
        dummy=(0,0)                         # dummy
        end=len(rev_chain)-1                # end index
        for i, this in enumerate(rev_chain):
            try:
                prev=dummy if i==0 else rev_chain[i-1]
                link=_EndLink(prev, this) if i==end else _Link(prev, this)
                link._link(self)
            except _LinkError as e:
                e._add_header(self.__err_str())
                raise e

    def _dump_file(self, rev):
        # `_file`: name of file.
        # `_file` holds saros db dump of doc with `self.__name` & `rev`.
        _file=self.__name+"-"+str(rev)          # file name
        _SarosDB()._doc_dump(self.__name, rev, _file)
        return _file

    def __saros_rev_chain(self):
        # Saros revision chain for doc `self.__name`, sorted by `rev`.
        # revision chain = last_revs = [ (rev, last), .., (rev, last) ]

        # NOTE: last_revs from Saros db are unordered either by `rev` or by 
        # `last`, but this routine sorts them by `rev` in ascending order.
        saros_rev_chain = _SarosDB()._last_revs(self.__name)
        return sorted(saros_rev_chain, key=lambda(rev, last): rev)

    def __err_str(self):
        # doc string for error message
        return "document: " + self.__name


class _Link:
    # represents a revision link -- `[(prev, plast), (rev, last)]`
    def __init__(self, (prev, plast), (rev, last)):
        # _prev: previous revision
        # _plast: `last` associated with `_prev`
        # _rev: this or current revision
        # _last: `last` associated with `_rev`
        self._prev, self._plast=(prev, plast)
        self._rev, self._last=(rev, last)

    def _link(self, doc):
        # if unlinked -- i.e., broken -- then links itself.
        # revisions are linked if their `last` is same as their prev's `last`.
        # this routine links `self._rev` to `self_prev`
        # doc revisions start from 1, so we only link when `_self._rev` > 1.
        self._validate()
        if self._rev <= 1: return
        linked = self._last == self._plast
        if not linked:
            _file=doc._dump_file(self._rev)         # file name
            _File(_file)._update(self._prev)        # update prev value
            _SarosDB()._load(_file)

    def _validate(self):
        # validates this link's (self._rev, self._last).
        if self._rev <= 0 or self._last <= 0:
            raise _NonPositiveLinkError(self.__err_data())
        if self._last < self._rev:
            raise _LastBelowRevisionError(self.__err_data())
        if self._rev == self._prev:
            raise _DuplicateLinkError(self.__err_data())
        if self._rev != self._prev + 1:
            raise _NonConsecutiveRevisionsError(self.__err_data())
        if self._last < self._plast:
            raise _DecreasingLastError(self.__err_data())
        if self._incomplete_prev():
            raise _MissingLinksError(self._missing_prev())
        if self._incomplete_end():
            raise _MissingLinksError(self._missing_end())

    def _incomplete_prev(self):
        # checks if link's (self._prev, self._plast)` chain is incomplete.
        # this happens when a broken link's `self._prev` < `self._plast`.
        if self._plast < self._last:
            return len(self._missing_prev()) > 0
        return False

    def _incomplete_end(self):
        # checks if end-link's (self._rev, self._last)` chain is incomplete.
        # this happens when end-link's `self._rev` <  `self._last`.
        # `_Link` objects are never the end link, so returns `False`.
        return False

    def __err_data(self):
        # link's data as a list for error message
        if self._prev == 0:         # don't report the dummy (0, 0)
            return [(self._rev, self._last)]
        return [(self._prev, self._plast), (self._rev, self._last)]

    def _missing_prev(self):
        # missing `[(rev, last)]` between `self._prev` & `self._plast`.
        return [(x, self._plast) for x in range(self._prev+1, self._plast+1)]

    def _missing_end(self):
        # end-link's missing `[(rev, last)]` between `self._rev` & `self._last`
        # `_Link` objects are never the end link, so returns [].
        return []


class _EndLink(_Link):
    # represents the `_Link` @ end of a document's revision chain
    # `_EndLink`, by definition, has no next link

    def _incomplete_end(self):
        # checks if end-link's (self._rev, self._last)` chain is incomplete.
        # this happens when end-link's  `self._rev` <  `self._last`.
        # `_EndLink` is always @ end of chain, so it does this check.
        return len(self._missing_end()) > 0

    def _missing_end(self):
        # end-link's missing `[(rev, last)]` between `self._rev` & `self._last`
        return [(x, self._last) for x in range(self._rev+1, self._last+1)]

