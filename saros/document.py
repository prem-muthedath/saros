#!/usr/bin/python

from .database.database import _SarosDB
from .xml import _File

# this module contains code to link revisions of a doc having a given name.
# ##############################################################################

class _Document:
    # represents a document, one identified by a given name.
    # this class links all unlinked revisions associated with a document name.
    def __init__(self, name):
        self.__name=name

    def _link_revs(self):
        # links all unlinked revs of `self.__name` to form a single rev chain.
        # index starts @ 0, but we loop from 1, so index refers to previous.
        rev_chain=self.__saros_rev_chain()  # doc's `[(rev, last)]` from db
        for i, (rev, last) in enumerate(rev_chain[1:]):
            prev, plast=rev_chain[i]    # NOTE: `i`, not `i-1`
            linked=last==plast
            if not linked:
                self.__dump_file(rev)._link(prev, _SarosDB())

    def __dump_file(self, rev):
        # returns dump file associated with revision `rev`.
        # dump file holds saros db dump of doc with `self.__name` & `rev`.
        fname=self.__name+"-"+str(rev)      # file name
        _SarosDB()._doc_dump(self.__name, rev, fname)
        return _File(fname)

    def __saros_rev_chain(self):
        # Saros revision chain for doc `self.__name`, sorted by `rev`.
        # revision chain = last_revs = [ (rev, last), .., (rev, last) ]

        # NOTE: last_revs from Saros db are unordered either by `rev` or by 
        # `last`, but this routine sorts them by `rev` in ascending order.
        saros_rev_chain = _SarosDB()._last_revs(self.__name)
        return sorted(saros_rev_chain, key=lambda(rev, last): rev)



