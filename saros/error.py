#!/usr/bin/python

# error module -- contains all exceptions classes in saros application.
# ##############################################################################

class _FileSchemaError(Exception):
    # represents error when doc file schema is nonconformant with db schema.
    def __init__(self, header, col):
        # `header`: error headline.
        # `col`: `_Schema` member (i.e., db column) related to error.
        self.__header=header
        self.__col=col

    def __str__(self):
        # err msg.
        return self.__header + self.__sdata()

    def __sdata(self):
        # db schema, in string format.
        return "\n => FYI - valid db schema (col name, type):\n  " + \
                ",\n  ".join([i.__str__() for i in self.__col.__class__])

################################################################################

class _FileDataError(Exception):
    # error when doc file data are nonconformant with db schema constraints.
    def __init__(self, header):
        # `header`: error headline.
        self.__header=header

    def __str__(self):
        # err msg.
        return self.__header

################################################################################

class _NoSuchDocIdError(Exception):
    # represents error when doc id does not exist in saros db.
    def __init__(self, doc_id):
        self.__id=doc_id

    def __str__(self):
        # err msg.
        return "doc id '" + self.__id + "', generated from `name` & `rev` " + \
                "values, does not exist in the db."

################################################################################

class _NoSuchColumnError(Exception):
    # represents error when column does not exist in saros db.
    def __init__(self, doc_id, col):
        # `col`: `_Schema` member (i.e., db column) related to error.
        self.__id=doc_id
        self.__col=col

    def __str__(self):
        # err msg.
        return "no such column '" + self.__col.name + "' exists in db " + \
                "for doc id: '" + self.__id + "'"

################################################################################

class _FileError(Exception):
    # represents error when file or directory doesn't exist.
    def __init__(self, msg):
        # msg: err message
        self.__msg=msg

    def __str__(self):
        return self.__msg

################################################################################


