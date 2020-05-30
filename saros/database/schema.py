#!/usr/bin/python

from aenum import Enum, NoAlias
from collections import OrderedDict

from ..error import (_FileSchemaError, _FileDataError,)

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

    id=str         # id column
    name=str       # name column
    rev=int        # revision column
    prev=int       # previous revision column
    last=int       # last revision column
    content=str    # content column

    def __init__(self, _type):
        # `_type`: data type defined for the column in schema.
        self._type=_type

    @classmethod
    def _map(cls, _file):
        # maps file contents to schema, returning a constraint-checked map -- an 
        # ord dict with `_Schema` items as keys.
        doc=_file._schema_map()         # map file contents to schema
        cls.__check(doc, str(_file))    # check schema constraints
        return doc

    @classmethod
    def _map_doc(cls, fdoc, fstr):
        # map `fdoc` -- doc data from file -- to schema.
        # `fdoc`: [(name, value), ..., (name, value)]
        # `fstr`: str representation of file -- source of `fdoc`.
        # returns an ord dict (i.e., the map) with `_Schema` members as keys.
        cpy=fdoc[:]         # keep copy for error report
        doc=OrderedDict()
        for col in _Schema:
            positions=[i for i, (x, _) in enumerate(fdoc) if x==col.name]
            if len(positions)==1:
                doc[col]=fdoc.pop(positions[0])[1]
            if len(positions) == 0:
                hdr="db column '"+ col.name + "' missing in " + fstr
                raise _FileSchemaError(hdr, col, cpy)
            if len(positions) > 1:
                hdr="db column '"+ col.name + "' duplicated in " + fstr
                raise _FileSchemaError(hdr, col, cpy)
            if type(doc[col]) != col._type:
                hdr="db column '"+ col.name + "' data type wrong in " + fstr
                raise _FileSchemaError(hdr, col, cpy)
            if col == list(_Schema)[-1] and len(fdoc) > 0:
                rogues=[x for (x, _) in fdoc]
                hdr="non-schema columns '" + ", ".join(rogues) + "' in " + fstr
                raise _FileSchemaError(hdr, col, cpy)
        return doc

    @classmethod
    def __check(cls, doc, fstr):
        # check schema constraints
        doc_id=cls._doc_id(doc[_Schema.name], doc[_Schema.rev])
        if not doc[_Schema.name] or doc[_Schema.name].isspace():
            header="doc 'name' is empty or whitespace in " + fstr
            raise _FileDataError(header, doc.items())
        if doc[_Schema.rev] < 1:
            header="doc revision < 1 in " + fstr
            raise _FileDataError(header, doc.items())
        if doc[_Schema.id] != doc_id:
            header="doc id not equal to '" + doc_id + "' in " + fstr
            raise _FileDataError(header, doc.items())
        if doc[_Schema.prev] not in [0, doc[_Schema.rev] - 1]:
            header="doc's 'prev' neither 0 nor 'rev' - 1 in " + fstr
            raise _FileDataError(header, doc.items())
        if doc[_Schema.last] < doc[_Schema.rev]:
            header="doc's 'last' <  'rev' in " + fstr
            raise _FileDataError(header, doc.items())

    @classmethod
    def _doc_id(cls, name, rev):
        # returns id, the primary key, of doc named `name`, revision `rev`
        return name + "-" + str(rev)

    def __str__(self):
        # enum member as string.
        return str((self.name, self._type))




