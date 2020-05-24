#!/usr/bin/python

# error module -- contains all exceptions classes in saros application.
# ##############################################################################

class _FileParseError(Exception):
    # represents bad doc file -- file nonconformant with db schema -- error.
    def __init__(self, schema, fname, col, doc):
        # `schema`: valid, ordered db schema.
        # `fname`: full name of doc file related to error.
        # `col`: db column related to error.
        # `doc`: parsed data from `fname`, as a [(name, val), ..., (name, val)]
        self._schema=schema
        self._fname=fname
        self._col=col
        self._doc=doc

    def __str__(self):
        # err msg
        return self._header() + \
                self.__fdata() + \
                self.__cdata() + \
                self.__pdata() + \
                self.__sdata()

    def _header(self):
        # error msg header.
        pass

    def __fdata(self):
        # file name, formatted for err msg.
        return "\n => problem file: \n  " + self._fname

    def __cdata(self):
        # db column details, as str.
        return "\n => error @ valid db column " + \
                "(col name, data type, schema-position):\n  " + \
                self._col.__str__()

    def __pdata(self):
        # parsed file data, with additional details, in string format.
        data=[self.__grp(x, y, i) for i, (x, y) in enumerate(self._doc)]
        return "\n => parsed file data as " + \
                "(col name, val, type, position):\n  " + ",\n  ".join(data)

    def __grp(self, x, y, z):
        # `(name, val, data_type, position)` as str.
        grp=(x, y, type(y), z)
        return str(grp)

    def __sdata(self):
        # db schema, in string format.
        return "\n => FYI - valid db schema (col name, type, position):\n  " + \
                ",\n  ".join([i.__str__() for i in self._schema])


class _DuplicateColumnError(_FileParseError):
    def _header(self):
        return "db column '" + self._col.name + "' duplicated in file. " + \
                "file validation aborted. " + \
                "please remove duplicates & re-validate the file."

class _ColumnMismatchError(_FileParseError):
    def _header(self):
        return "db column '" + self._col.name + \
                "' missing or in wrong position in file."

class _BadDataTypeError(_FileParseError):
    def _header(self):
        return "db column '" + self._col.name + \
                "' data type mismatched in file."

class _BadNameError(_FileParseError):
    def _header(self):
        return "doc name is whitespace or empty string in file."

class _BadRevisionError(_FileParseError):
    def _header(self):
        return "doc revision < 1 in file."

class _BadIdError(_FileParseError):
    def _header(self):
        return "doc id does not either start with `name` or end with " + \
                "`rev` (as string) in file -- it must do both, in db format."

class _BadPrevError(_FileParseError):
    def _header(self):
        return "doc's previous revision neither equals 0 nor " + \
                "`rev` - 1 in file."

class _BadLastError(_FileParseError):
    def _header(self):
        return "doc's `last` < `rev` in file."

class _SchemaSizeMismatchError(_FileParseError):
    def _header(self):
        return "the last column '" + self._col.name + \
                "' in db schema is not the last one in file."

class _NoSuchDocId(Exception):
    def __init__(self, doc_id):
        self.__id=doc_id

    def __str__(self):
        return "doc id generated from `name` & `rev` values " + \
                "does not exist in the db." + \
                "\n => doc id: " + self.__id

