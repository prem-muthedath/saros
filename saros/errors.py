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

class _NonPositiveRevisionError(_LinkError):
    # represents `rev` <= 0 in `(rev, last)` error.
    pass

class _LastBelowRevisionError(_LinkError):
    # represents `last` < `rev` in `(rev, last)` error.
    pass

class _DuplicateRevisionsError(_LinkError):
    # represents `prev`=`rev` in `[(prev, plast), (rev, last)]` error.
    pass

class _DecreasingLastError(_LinkError):
    # represents `last` < `plast` in `[(prev, plast), (rev, last)]` error.
    pass

class _NonConsecutiveRevisionsError(_LinkError):
    # represents `rev` != `prev` + 1 in `[(prev, plast), (rev, last)]` error.
    pass

class _MissingLinksError(_LinkError):
    # represents missing links `[(rev, last)]` error.
    pass


