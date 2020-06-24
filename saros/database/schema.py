#!/usr/bin/python

from aenum import Enum, NoAlias

from ..error import _FileDataError

# this module defines the database schema.
################################################################################

class _Schema(Enum):
    # represents db schema.
    # all saros doc dump files have to conform to the schema defined here.
    # class design idea from /u/ ethan furman @ https://tinyurl.com/ycacxytx

    # schema definition (see below) -- members (i.e., columns) & their order.
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
        # `_type`: data type defined for the member (i.e., column) in schema.
        self._type=_type

    @classmethod
    def _check(cls, doc, xml):
        # check `doc` against schema constraints.
        # `doc`: ord dict with `_Schema` items as keys; represents a saros doc.
        # `xml`: instance of `_Xml`.
        # throws `_FileDataError` if `doc` invalid.
        doc_id=cls._doc_id(doc[_Schema.name], doc[_Schema.rev])
        if not doc[_Schema.name] or doc[_Schema.name].isspace():
            header=xml._hdr("doc 'name' is empty or whitespace")
            raise _FileDataError(header)
        if doc[_Schema.rev] < 1:
            header=xml._hdr("doc revision < 1")
            raise _FileDataError(header)
        if doc[_Schema.id] != doc_id:
            header=xml._hdr("doc id not equal to '" + doc_id + "'")
            raise _FileDataError(header)
        if doc[_Schema.prev] not in [0, doc[_Schema.rev] - 1]:
            header=xml._hdr("doc's 'prev' neither 0 nor 'rev' - 1")
            raise _FileDataError(header)
        if doc[_Schema.last] < doc[_Schema.rev]:
            header=xml._hdr("doc's 'last' <  'rev'")
            raise _FileDataError(header)

    @classmethod
    def _doc_id(cls, name, rev):
        # returns id, the primary key, of doc named `name`, revision `rev`
        return name + "-" + str(rev)

    def __str__(self):
        # enum member as string.
        return str((self.name, self._type))



