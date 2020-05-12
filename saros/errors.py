#!/usr/bin/python

# error module -- contains all exceptions classes in saros application
# ##############################################################################

class _LinkError(Exception):
    # represents link error
    def __init__(self, data):
        # self.__data: `[(rev, last)]` related to error.
        # self.__header: error message header
        self.__header=""
        self.__data=data

    def _add_header(self, header):
        # header str for error msg
        self.__header=header

    def __str__(self):
        # err msg
        return self.__header +  ", " + "[(rev, last)] -> " + str(self.__data)

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


