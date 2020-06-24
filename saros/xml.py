#!/usr/bin/python

import os
from collections import OrderedDict

from .database.schema import _Schema
from .error import _FileSchemaError

# this module contains private classes that do back-and-forth conversion between 
# (name, value) pairs & its XML element representation -- <name>value</name>
################################################################################

class _Attributes:
    # represents [_Attribute]
    def __init__(self, attrs):
        # `attrs` = [_Attribute]
        self.__attrs=attrs

    def _write(self, xml):
        # writes xml representation of `self.__attrs` to file.
        xml._write(self.__to_xml())

    def __to_xml(self):
        # returns xml = ['<xml>', '<name>value</name>', ..., '</xml>']
        # for `join()` trick, see /u/ RiaD @ https://tinyurl.com/y8ypjowj
        elems=[each._to_xml() for each in self.__attrs]
        xml='\n'.join([''] + elems + [''])
        return _Attribute(('xml', xml))._to_xml().split('\n')

################################################################################

class _Attribute:
    # represents a (name, value) pair -- i.e., an xml attribute
    def __init__(self, (name, val)):
        self.__name, self.__val=(name, val)

    def _to_xml(self):
        # returns an xml element "<name>value</name>"
        return "<" + self.__name + ">" + \
                self.__good_val() + "</" + self.__name + ">"

    def __good_val(self):
        # converts int to str
        if isinstance(self.__val, int):
            return str(self.__val)
        return self.__val

################################################################################

class _Xml:
    # represents xml conetent of file named `ffname`
    def __init__(self, ffname):
        # `ffname`: full file name = path + name + extn
        self.__ffname=ffname

    def _parse(self):
        # parses xml file, returning document as a list of attributes
        # document attributes list = [(name, val), ..., (name, val)]
        xml=[]
        with open(self.__ffname, 'r') as reader:
            xml=[line.rstrip() for line in reader]
        return [_Element(i)._parse() for i in xml[1:-1]] # skip 'xml' hdr, ftr

    def _write(self, xml):
        # writes `xml` to file named `self.__ffname`
        # `xml` = ['<xml>', '<name>value</name>', ..., '</xml>']
        with open(self.__ffname, 'w') as writer:
            for each in xml:
                writer.write(each)
                writer.write("\n")

    def _schema_map(self):
        # constrained-checked schema map of xml.
        # map: ord dict with `_Schema` members as keys.
        doc=self.__map(self._parse())
        _Schema._check(doc, self)
        return doc

    def __map(self, fdoc):
        # maps `fdoc` -- parsed xml data -- to schema.
        # returns an ord dict (i.e., the map) with `_Schema` members as keys.
        # throws `_FileSchemaError` under schema violation.
        doc=OrderedDict()
        for col in _Schema:
            positions=[i for i, (x, _) in enumerate(fdoc) if x==col.name]
            if len(positions)==1:
                doc[col]=fdoc.pop(positions[0])[1]
            if len(positions) == 0:
                hdr=self._hdr("schema column '"+ col.name + "' missing")
                raise _FileSchemaError(hdr, col)
            if len(positions) > 1:
                hdr=self._hdr("schema column '"+ col.name + "' duplicated")
                raise _FileSchemaError(hdr, col)
            if type(doc[col]) != col._type:
                typstr="data type != '" + col._type.__name__ + "'"
                hdr=self._hdr("schema column '"+ col.name + "' " + typstr)
                raise _FileSchemaError(hdr, col)
            if col == list(_Schema)[-1] and len(fdoc) > 0:
                rogues=", ".join([x for (x, _) in fdoc])
                hdr=self._hdr("non-schema columns '" + rogues + "'")
                raise _FileSchemaError(hdr, col)
        return doc

    def _hdr(self, errhdr):
        # appends file name part to `errhdr` (i.e., error header)
        return errhdr + " in '" + self.__ffname + "'"

################################################################################

class _Element:
    # represents an xml element -- from start-to-end tag
    def __init__(self, element):
        # element = "<name>value</name>"
        self.__element=element

    def _parse(self):
        # extracts (name, val)
        self.__validate();
        return (self.__name(), self.__good_val())

    def __validate(self):
        if not ( self.__element.startswith("<") and \
                 self.__element.endswith(">") ):
            raise RuntimeError("invalid xml element: '" + self.__element + \
                    "' does not begin/end with '<', '>'")

    def __name(self):
        # "<" is the first one, so we skip it & get substring from 1:
        return self.__element[1:self.__fst_close()]

    def __fst_close(self):
        # index of first occurence of close tag symbol ">"
        return self.__element.index(">")

    def __good_val(self):
        # we extract substring after ">", so add 1 to __fst_close()
        val=self.__element[self.__fst_close()+1:self.__snd_open()]
        return self.__num(val)

    def __snd_open(self):
        # index of second occurence of open tag symbol "<" -- which is "</"
        return self.__element.index("</")

    def __num(self, val):
        if ' ' in val: return val   # fix for bug, such as  " -4"
        try:
            return int(val)
        except ValueError:
            return val

################################################################################

class _File:
    # represents an xml file, one identified by a given name.
    # file holds a saros doc as an xml.
    def __init__(self, name):
        # `name` is name of xml file
        # NOTE: `name` does NOT include file path and file extension
        self.__name = name
        self.__extn = ".xml"    # xml file extension
        self.__dir = "temp"     # directory containing the xml file

    def _write(self, doc):
        # writes `doc` as an xml.  `doc` represents a document as an array of 
        # attributes = [(name, val), ..., (name, val)]
        _Attributes([_Attribute(attr) for attr in doc])._write(self.__xml())

    def __xml(self):
        # returns an instance of `_Xml`
        return _Xml(self.__full_name())

    def __full_name(self):
        # returns full name of xml file: full path + file name + extension
        # example: '~/../saros/saros/temp/doc.xml'
        return self.__path() + self.__name + self.__extn

    def __path(self):
        # returns full path to the xml file.
        # example: '~/../saros/saros/temp/'
        return os.path.dirname(os.path.realpath(__file__)) + \
                "/" + self.__dir + "/"

    def _link(self, prev, db):
        # link doc, represented by file's content, to previous revision `prev`
        self._write(self.__doc(_Schema.prev.name, prev))
        db._load(self.__name)

    def __doc(self, name, value):
        # returns `doc` info, i.e., `[(name, val)]`, updated with `value`.
        xml=self.__xml()
        return [(name, value) if i == name else (i, j) for (i, j) in xml._parse()]

    def _schema_map(self):
        # valid schema map (ord dict with schema items as keys) of contents.
        return self.__xml()._schema_map()

################################################################################

