#!/usr/bin/python

import os

# this module contains private classes that do back-and-forth conversion between 
# a (name, value) pair & its XML element representation -- <name>value</name>
################################################################################

class _Attribute:
    # represents a (name, value) pair -- i.e., an xml attribute
    def __init__(self, (name, val)):
        self.__name, self.__val=(name, val)

    def _to_xml(self):
        # returns an xml element "<name>value</name>"
        return "<" + self.__name + ">" + self.__good_val() + "</" + self.__name + ">"

    def __good_val(self):
        # converts int to str
        if isinstance(self.__val, int):
            return str(self.__val)
        return self.__val


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
            raise RuntimeError("invalid xml element: not begin/end with <, > => " + self.__element)

    def __name(self):
        # "<" is the first one, so we skip it & get substring from 1:
        return self.__element[1:self.__fst_close()]

    def __good_val(self):
        # we extract substring after ">", so add 1 to __fst_close()
        val=self.__element[self.__fst_close()+1:self.__snd_open()]
        return self.__num(val)

    def __fst_close(self):
        # index of first occurence of close tag symbol ">"
        return self.__element.index(">")

    def __snd_open(self):
        # index of second occurence of open tag symbol "<" -- which is "</"
        return self.__element.index("</")

    def __num(self, val):
        try:
            return int(val)
        except ValueError:
            return val


class _File:
    # represents an xml file that has complete info about a document
    def __init__(self, name):
        # `name` is name of xml file
        # NOTE: `name` does NOT include file path and file extension
        self.__name = name

    def _write(self, doc):
        # writes `doc` as an xml.  `doc` represents a document as an array of 
        # attributes = [(name, val), ..., (name, val)]
        with open(self.__full_name(), 'w') as writer:
            for each in doc:
                writer.write(_Attribute(each)._to_xml())
                writer.write("\n")

    def _read(self):
        # reads xml file, returning document as an array of attributes
        # `doc` = array of document attributes = [(name, val), ..., (name, val)]
        doc=[]
        with open(self.__full_name(), 'r') as reader:
            for line in reader:
                line=line.rstrip()
                doc.append(_Element(line)._parse())
        return doc

    def __full_name(self):
        # returns full name of xml file: full path + file name + extension
        # example: ~/../saros/saros/temp/doc.xml
        return self.___path()+self.__name+self.__type()

    def ___path(self):
        # returns full path to the xml file
        return os.path.dirname(os.path.realpath(__file__))+ \
                "/"+self.__directory()+"/"

    def __directory(self):
        # directory containing the xml file
        return "temp"

    def __type(self):
        # xml file extension
        return ".xml"

    def _link(self, prev, db):
        # link doc represented by this file to `prev`
        self.__update(prev)
        db._load(self.__name)

    def __update(self, prev):
        # updates `prev` value in xml file
        doc=[]
        for (name, val) in self._read():
            if name == "prev":
                val=prev
            doc.append((name, val))
        self._write(doc)


