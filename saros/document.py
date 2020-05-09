#!/usr/bin/python

from .database import _SarosDB
from .xml import  _File
from .errors import (_NonPositiveLinkError,
                        _LastBelowRevisionError,
                        _DuplicateLinkError,
                        _DecreasingLastError,
                        _NonConsecutiveRevisionsError,
                        _MissingLinksError,
                        )

# module has claases involved in linking revisions of a doc with a given name
# ##############################################################################

class _Document:
    # represents a document, one identified by a given name.
    # this class links all unlinked revisions associated with a document name.
    def __init__(self, name):
        self.__name=name

    def _link_revs(self):
        # links all unlinked revs of `self.__name` to form a single rev chain.
        # `_EndLink` handles checks @ end of rev chain that `_Link` can't.
        links=self.__saros_links()  # `[(rev, last)]` from db for this doc
        dummy=_Link((0,0))          # dummy link
        end=len(links)-1            # end index
        for i, link in enumerate(links):
            prev=dummy if i==0 else _Link(links[i-1])
            this=_EndLink(link) if i==end else _Link(link)
            this._validate(prev, self._str())   # validate `this` link
            prev._link(this, self)              # link `prev` & `this`

    def _link(self, prev, this):
        # links `prev` link with `this` link.
        # `_file`: name of file.
        # `_file` holds saros db dump of doc with `self.__name` & `rev`.
        rev=prev._next_rev()
        _file=self.__name+"-"+str(rev)      # file name
        _SarosDB()._doc_dump(self.__name, rev, _file)
        this._update(_file)

    def __saros_links(self):
        # Saros revision links for doc `self.__name`, sorted by `rev`.
        # revision links = links = last_revs = [ (rev, last), .., (rev, last) ]

        # NOTE: last_revs from Saros db are unordered either by `rev` or by 
        # `last`, but this routine sorts them by `rev` in ascending order.
        saros_links = _SarosDB()._last_revs(self.__name)
        return sorted(saros_links, key=lambda(rev, last): rev)

    def _str(self):
        # string representation of _Document
        return "document: " + self.__name


class _Link:
    # represents a revision link -- `(rev, last)`
    def __init__(self, (rev, last)):
        self._rev=rev
        self._last=last

    def _link(self, _next, doc):
        # if unlinked to it's next, then links itself to next
        # links are connected if their `last` is same as their next's `last`.
        # valid links have revisions >=1, so we only link these.
        # NOTE: before calling this method, `_next` should be validated.
        if self._rev < 1: return
        linked = self._last == _next._last
        if not linked:
            doc._link(self, _next)

    def _update(self, _file):
        # updates this link in saros db.
        # _file`: name of saros db dump file of doc whose rev = `self._rev`
        _File(_file)._update(self._rev-1)      # update prev value
        _SarosDB()._load(_file)

    def _validate(self, prev, doc_str):
        # validates this link.
        # `prev`: this link's immediate predecessor.
        # `doc_str`: str() of `_Document` instance this link belongs to.
        # `p_missing`: missing links in the rev chain `prev` belongs to.
        p_missing=prev._missing_broken(self)
        if self._rev <= 0 or self._last <= 0:
            raise _NonPositiveLinkError(doc_str, [self])
        if self._last < self._rev:
            raise _LastBelowRevisionError(doc_str, [self])
        if self == prev:
            raise _DuplicateLinkError(doc_str, [prev, self])
        if self._rev != prev._rev + 1:
            raise _NonConsecutiveRevisionsError(doc_str, [prev, self])
        if self._last < prev._last:
            raise _DecreasingLastError(doc_str, [prev, self])
        if len(p_missing) > 0:
            raise _MissingLinksError(doc_str, p_missing)
        if self._incomplete_end():
            raise _MissingLinksError(doc_str, self._missing_links())

    def _next_rev(self):
        # immediate successor revision
        return self._rev+1

    def __eq__(self, other):
        # tests equality
        return ((isinstance(other, _Link) or isinstance(other, _EndLink))
                and (self._rev==other._rev and self._last==other._last))

    def __ne__(self, other):
        # ne test
        return not self.__eq__(other)

    def _missing_broken(self, _next):
        # missing links in this link's rev chain when this link is broken
        if self._last < _next._last:
            return self._missing_links()
        return []

    def _incomplete_end(self):
        # checks if the end link is not the true end link.
        # this happens when end link's `rev` < it's `last`.
        # `_Link` objects are never the end link, so returns `False`.
        return False

    def _str(self):
        # link's string representation
        return str((self._rev, self._last))

    def _missing_links(self):
        # missing links
        return [_Link((x, self._last)) for x in range(self._rev+1, self._last+1)]


class _EndLink(_Link):
    # represents the `_Link` @ end of a document's revision chain
    # `_EndLink`, by definition, has no next link
    def _link(self, _next, doc):
        # invalid operation for end link
        raise RuntimeError(self.__errmsg())

    def _incomplete_end(self):
        # checks if the end link is not the true end link.
        # this happens when end link's `rev` < it's `last`.
        # `_EndLink` is always @ end of chain, so it does this check.
        return len(self._missing_links()) > 0

    def _next_rev(self):
        # invalid operation for end link
        raise RuntimeError(self.__errmsg())

    def _missing_broken(self, _next):
        # invalid operation for end link
        raise RuntimeError(self.__errmsg())

    def __errmsg(self):
        return "Invalid operation: `EndLink` object, by definition, has no next link"


