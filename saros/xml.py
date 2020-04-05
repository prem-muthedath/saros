#!/usr/bin/python

# this module contains private classes that do back-and-forth conversion between 
# a (name, value) pair & its XML element representation -- <name>value</name>
################################################################################

class _Attribute:
    # represents a (name, value) pair -- i.e., an xml attribute
    def __init__(self, (name, val)):
        self.__name, self.__val=(name, val)

    def _element(self):
        # converts this _Attribute to an _Element
        _str = "<" + self.__name + ">" + self.__good_val() + "</" + self.__name + ">"
        return _Element(_str)

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

    def _update(self, prev, last):
        # returns an updated copy if this _Element represents
        # either a "<prev>value</prev>" or a "<last>value</last>";
        # otherwise, returns self, unchanged.
        name, _ = self._parse()
        if name == "prev":
            return _Attribute((name, prev))._element()
        elif name == "last":
            return _Attribute((name, last))._element()
        else:
            return self

    def _parse(self):
        # extracts (name, val)
        self.__validate();
        return (self.__name(), self.__good_val())

    def __validate(self):
        if not ( self.__element.startswith("<") and \
                 self.__element.endswith(">") ):
            raise RuntimeError("invalid xml element: < or > missing")

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

