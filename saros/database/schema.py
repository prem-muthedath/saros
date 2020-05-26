#!/usr/bin/python

from aenum import Enum, NoAlias
from collections import OrderedDict

from ..error import (_MissingColumnError,
                        _DuplicateColumnError,
                        _ColumnIndexMismatchError,
                        _BadDataTypeError,
                        _BadNameError,
                        _BadRevisionError,
                        _BadIdError,
                        _BadPrevError,
                        _BadLastError,
                        _SchemaSizeMismatchError,
                    )

# this module defines the database schema.
# ##############################################################################

class _Schema(Enum):
    # represents db schema.
    # all saros doc dump files have to conform to the schema defined here.
    # class design idea from /u/ ethan furman @ https://tinyurl.com/ycacxytx

    # schema definitions (see below) -- col names, order, & data types.
    # "no-alias" settings from /u/ ethan furman @ https://tinyurl.com/yb2ofxvd
    _order_ = 'id name rev prev last content'
    _settings_ = NoAlias

    id=(str, 0)         # id column
    name=(str, 1)       # name column
    rev=(int, 2)        # revision column
    prev=(int, 3)       # previous revision column
    last=(int, 4)       # last revision column
    content=(str, 5)    # content column

    def __init__(self, _type, index):
        # `_type`: data type defined for the column in schema.
        # `index`: column position in the schema.
        self._type=_type
        self._index=index

    def _validate(self, _doc, fname):
        # checks if `doc` is invalid, per schema; if so, raises an exception.
        # `_doc`: content of file `fname` as a list of (name, value) pairs.
        # `fname`: full name of file.
        doc=OrderedDict(_doc)   # dict allows easy lookup.
        pos=[i for i, (x, y) in enumerate(_doc) if x==self.name]
        if self in _Schema:
            if len(pos) == 0:
                raise _MissingColumnError(_Schema, fname, self, _doc)
            if len(pos) > 1:
                raise _DuplicateColumnError(_Schema, fname, self, _doc)
            if self._index!=pos[0]:
                raise _ColumnIndexMismatchError(_Schema, fname, self, _doc)
            if type(doc[self.name])!=self._type:
                raise _BadDataTypeError(_Schema, fname, self, _doc)
        if self==_Schema.name:
            if not doc[self.name] or doc[self.name].isspace():
                raise _BadNameError(_Schema, fname, self, _doc)
        if self==_Schema.rev:
            if doc[self.name] < 1:
                raise _BadRevisionError(_Schema, fname, self, _doc)
        if self==_Schema.id:
            _name, _rev=(doc[_Schema.name.name], doc[_Schema.rev.name])
            if not doc[self.name].startswith(_name) or \
                    not doc[self.name].endswith(str(_rev)) or \
                    len(doc[self.name]) < len(_name) + len(str(_rev)):
                raise _BadIdError(_Schema, fname, self, _doc)
        if self==_Schema.prev:
            if not (doc[self.name] == 0 or \
                    doc[self.name] == doc[_Schema.rev.name] - 1):
                raise _BadPrevError(_Schema, fname, self, _doc)
        if self==_Schema.last:
            if doc[self.name] < doc[_Schema.rev.name]:
                raise _BadLastError(_Schema, fname, self, _doc)
        if self==_Schema.content:
            if pos[0]!=len(_doc)-1:
                raise _SchemaSizeMismatchError(_Schema, fname, self, _doc)

    def __str__(self):
        # enum field as string.
        return str((self.name, self._type, self._index))


def _file_load_schema():
    # schema for file validation.
    # we want to validate `name` & `rev` before `id`.
    norm=[]     # items in normal order, as defined in `_Schema`.
    pref=[]     # items in preferred order for validation.
    for i in _Schema:
        if i in [_Schema.name, _Schema.rev]:
            pref.append(i)
        else:
            norm.append(i)
    return pref+norm



