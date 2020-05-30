#!/usr/bin/python

# error module -- contains all exceptions classes in saros application.
# ##############################################################################

class _FileSchemaError(Exception):
    # represents error when doc file schema is nonconformant with db schema.
    def __init__(self, header, col, fdoc):
        # `header`: error headline.
        # `col`: `_Schema` member (i.e., db column) related to error.
        # `fdoc`: parsed doc data from file = [(name, val), ..., (name, val)]
        self.__header=header
        self.__col=col
        self.__fdoc=fdoc

    def __str__(self):
        # err msg.
        return self.__header + \
                self.__cdata() + \
                self.__pdata() + \
                self.__sdata()

    def __cdata(self):
        # db column details, as str.
        return "\n => error @ valid db column " + \
                "(col name, data type):\n  " + \
                self.__col.__str__()

    def __pdata(self):
        # parsed file data, with additional details, in string format.
        data=[self.__grp(x, y) for (x, y) in self.__fdoc]
        return "\n => parsed file data as " + \
                "(col name, val, type):\n  " + ",\n  ".join(data)

    def __grp(self, x, y):
        # `(name, val, data_type)` as str.
        grp=(x, y, type(y))
        return str(grp)

    def __sdata(self):
        # db schema, in string format.
        return "\n => FYI - valid db schema (col name, type):\n  " + \
                ",\n  ".join([i.__str__() for i in self.__col.__class__])

################################################################################

class _FileDataError(Exception):
    # error when doc file data are nonconformant with db schema constraints.
    def __init__(self, header, fdoc):
        # `header`: error headline.
        # `fdoc`: parsed data from file = [(_Schema.member, value), ..., ]
        self.__header=header
        self.__fdoc=fdoc

    def __str__(self):
        # err msg.
        return self.__header + self.__pdata()

    def __pdata(self):
        # parsed file data as str.
        return "\n => file data:\n  " + \
                ",\n  ". join([str((i.name, j)) for (i, j) in self.__fdoc])

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
        return "No such column '" + self.__col.name + "' exists in db " + \
                "for doc id: '" + self.__id + "'"

################################################################################

