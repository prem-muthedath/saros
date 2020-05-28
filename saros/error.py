#!/usr/bin/python

# error module -- contains all exceptions classes in saros application.
# ##############################################################################

class _FileSchemaError(Exception):
    # represents error when doc file schema is nonconformant with db schema.
    def __init__(self, header, col, fdoc):
        # `header`: error headline.
        # `col`: db column related to error.
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
                "(col name, data type, schema-position):\n  " + \
                self.__col.__str__()

    def __pdata(self):
        # parsed file data, with additional details, in string format.
        data=[self.__grp(x, y, i) for i, (x, y) in enumerate(self.__fdoc)]
        return "\n => parsed file data as " + \
                "(col name, val, type, position):\n  " + ",\n  ".join(data)

    def __grp(self, x, y, z):
        # `(name, val, data_type, position)` as str.
        grp=(x, y, type(y), z)
        return str(grp)

    def __sdata(self):
        # db schema, in string format.
        return "\n => FYI - valid db schema (col name, type, position):\n  " + \
                ",\n  ".join([i.__str__() for i in self.__col.__class__])


class _FileDataError(Exception):
    # represents error when doc file data is nonconformant with saros db.
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


class _NoSuchDocIdError(Exception):
    # represents error when doc id does not exist in saros db.
    def __init__(self, doc_id):
        self.__id=doc_id

    def __str__(self):
        # err msg.
        return "doc id generated from `name` & `rev` values " + \
                "does not exist in the db." + \
                "\n => doc id: '" + self.__id + "'"


class _NoSuchColumnError(Exception):
    # represents error when column does not exist in saros db.
    def __init__(self, doc_id, col):
        self.__id=doc_id
        self.__col=col

    def __str__(self):
        # err msg.
        return "No such column '" + self.__col + "' exists in db " + \
                "for doc id: '" + self.__id + "'"


