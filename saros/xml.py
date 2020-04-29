#!/usr/bin/python

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
        self.__name = name

    def _write(self, doc):
        # writes `doc` as an xml.  `doc` represents a document as an array of 
        # attributes = [(name, val), ..., (name, val)]
        with open(self.__name, 'w') as writer:
            for each in doc:
                writer.write(_Attribute(each)._to_xml())
                writer.write("\n")

    def _read(self):
        # reads xml file, returning document as an array of attributes
        # `doc` = array of document attributes = [(name, val), ..., (name, val)]
        doc=[]
        with open(self.__name, 'r') as reader:
            for line in reader:
                line=line.rstrip()
                doc.append(_Element(line)._parse())
        return doc

    def _update(self, prev, last):
        # updates `prev` & `last` values in xml file
        doc=[]
        for (name, val) in self._read():
            if name == "prev":
                val=prev
            elif name == "last":
                val=last
            doc.append((name, val))
        self._write(doc)


