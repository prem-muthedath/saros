#!/usr/bin/python

from aenum import Enum, NoAlias

from ..error import (_FileSchemaError, _FileDataError, _NoSuchDocIdError,)

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

    def _associated_value(self, fdoc, ffname):
        # `fdoc`: doc data from file named `ffname` = [(name, value)].
        # `ffname`: full name (path & extn) of file -- source of `fdoc`.
        #
        # returns unique value associated with `self.name` from `fdoc` if data 
        # index & type match those of `self`; throws exception otherwise.
        positions=[i for i, (x, _) in enumerate(fdoc) if x==self.name]
        if len(positions) == 0:
            hdr="db column '"+ self.name + "' missing in " + ffname
            raise _FileSchemaError(hdr, self, fdoc)
        if len(positions) > 1:
            hdr="db column '"+ self.name + "' duplicated in " + ffname
            raise _FileSchemaError(hdr, self, fdoc)
        if positions[0] != self._index:
            hdr="db column '"+ self.name + "' in wrong order in " + ffname
            raise _FileSchemaError(hdr, self, fdoc)
        if positions[0] == len(_Schema) - 1 and len(fdoc) != len(_Schema):
            hdr="the last column is not '" + self.name + "' in " + ffname
            raise _FileSchemaError(hdr, self, fdoc)
        if type(fdoc[self._index][1]) != self._type:
            hdr="db column '"+ self.name + "' data type wrong in " + ffname
            raise _FileSchemaError(hdr, self, fdoc)
        return fdoc[self._index][1]

    def __str__(self):
        # enum field as string.
        return str((self.name, self._type, self._index))




