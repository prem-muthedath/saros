#!/usr/bin/python

from .xml import _Attribute, _XmlElement

class _SarosDB:
    # this private class models Saros database -- the document repository.  it 
    # offers methods for typical database operations -- queries & updates.
    #
    # only Saros -- the only public class in saros package -- should invoke 
    # methods of this class. no one else should.
    # 
    # NOTE:
    # there is no API, however, to link doc revisions; instead, clients must:
    # 1. request XML dump of a specific doc revision (i.e., doc name & revision)
    # 2. update XML with revision link info, & send it to SarosDB to load
    # 3. SarosDB then parses XML, & loads data
    # 4. After load, SarosDB updates "last" of all revisions of the doc whose 
    #    "last" < "last" of the just updated link.
    #
    # SCHEMA:
    # 1. each row represents a doc with a unique combination of "name" & "rev"
    # 2. doc_id -- unique combination of "name" & "rev" -- indexes each row
    # 3. a doc with same "name" may have >1 revision; each form a seperate row
    # 4. "name"     -> doc's name
    #    "rev"      -> doc's revision number (starts from 1, increase by 1)
    #    "prev"     -> "rev" of immediate predecessor; for "rev"=1, "prev"=0
    #    "Last"     -> last "rev" in the chain "rev" belongs ~ total revisions
    #    "content"  -> doc's content
    # 5. each row must have valid "prev" & "last" values 
    
    def __init__(self):
        # self_docs = { doc_id: [ ("name", val), ("rev", val), ("prev", val), ("last", val), ("content", val) ] }
        self.__docs = { # represents the database
            "JE00-1": [("name", "JE00"), ("rev", 1), ("prev", 0), ("last", 3), ("content", "i am JE00-1")],
            "JE00-2": [("name", "JE00"), ("rev", 2), ("prev", 1), ("last", 3), ("content", "i am JE00-2")],
            "JE00-3": [("name", "JE00"), ("rev", 3), ("prev", 2), ("last", 3), ("content", "i am JE00-3")],
            "JE00-4": [("name", "JE00"), ("rev", 4), ("prev", 0), ("last", 6), ("content", "i am JE00-4")],
            "JE00-5": [("name", "JE00"), ("rev", 5), ("prev", 4), ("last", 6), ("content", "i am JE00-5")],
            "JE00-6": [("name", "JE00"), ("rev", 6), ("prev", 5), ("last", 6), ("content", "i am JE00-6")],
            "JE00-7": [("name", "JE00"), ("rev", 7), ("prev", 0), ("last", 8), ("content", "i am JE00-7")],
            "JE00-8": [("name", "JE00"), ("rev", 8), ("prev", 7), ("last", 8), ("content", "i am JE00-8")],
            "JE01-1": [("name", "JE01"), ("rev", 1), ("prev", 0), ("last", 2), ("content", "i am JE01-1")],
            "JE01-2": [("name", "JE01"), ("rev", 2), ("prev", 1), ("last", 2), ("content", "i am JE01-2")],
            "JE02-1": [("name", "JE02"), ("rev", 1), ("prev", 0), ("last", 4), ("content", "i am JE02-1")],
            "JE02-2": [("name", "JE02"), ("rev", 2), ("prev", 1), ("last", 4), ("content", "i am JE02-2")],
            "JE02-3": [("name", "JE02"), ("rev", 3), ("prev", 2), ("last", 4), ("content", "i am JE02-3")],
            "JE02-4": [("name", "JE02"), ("rev", 4), ("prev", 3), ("last", 4), ("content", "i am JE02-4")],
            "JE02-5": [("name", "JE02"), ("rev", 5), ("prev", 0), ("last", 7), ("content", "i am JE02-5")],
            "JE02-6": [("name", "JE02"), ("rev", 6), ("prev", 5), ("last", 7), ("content", "i am JE02-6")],
            "JE02-7": [("name", "JE02"), ("rev", 7), ("prev", 6), ("last", 7), ("content", "i am JE02-7")],
            "JE03-1": [("name", "JE03"), ("rev", 1), ("prev", 0), ("last", 1), ("content", "i am JE03-1")]
        }

    def _dump(self):
        # dump of all docs & their `id`s, sorted by `id`
        dump=[]
        for each in sorted(self.__docs):
            dump.append((each, self.__docs[each]))
        return dump 

    def _doc_names(self):
        # list of all unique doc names
        names=[]
        for doc_id in self.__docs:
            name=self.__fetch(doc_id, "name")
            if name not in names:
                names.append(name)
        return names

    def _last_revs(self, name):
        # gathers "last" for all revisions of doc named `name`
        # returns an unordered [ ("rev", "last") ]
        last_revs=[]
        for doc_id in self.__docs:
            if name in doc_id:
                rev=self.__fetch(doc_id, "rev")
                last=self.__fetch(doc_id, "last")
                last_revs.append((rev, last))
        return last_revs

    def _doc_xml(self, name, rev):
        # xml dump of doc named `name`, revision `rev`
        doc_id=self.__doc_id(name, rev)
        doc_xml=[ _Attribute(("id", doc_id))._to_xml() ]
        for each in self.__docs[doc_id]:
            doc_xml.append(_Attribute(each)._to_xml())
        return doc_xml

    def _load(self, doc_xml):
        # loads doc defined by `doc_xml` into the database
        doc_id=""
        vals=[]
        for each in doc_xml:
            name, val=_XmlElement(each)._parse()
            if name=="id":
                doc_id=val
            else:
                vals.append((name,val))
        self.__docs.pop(doc_id)
        self.__docs[doc_id]=vals
        self.__update_last(doc_id)

    def __update_last(self, doc_id):
        # doc_id -> id of doc whose revision link has just been updated.
        # for all revs of doc whose name `name` ~ as `name` of doc associated 
        # with doc_id & whose "last" < "last" of doc associated with doc_id, 
        # replace "last" with "last" of the just updated link.
        last=self.__fetch(doc_id, "last")
        name=self.__fetch(doc_id, "name")
        for (_rev, _last) in self._last_revs(name):
            _id=self.__doc_id(name, _rev)
            if _last < last and _id != doc_id:
                self.__put(_id, "last", last)

    def __doc_id(self, name, rev):
        # returns id of doc named `name`, revision `rev`
        return name + "-" + str(rev)

    def __fetch(self, doc_id, col):
        # given a doc_id & col (i.e., attribute name), returns the value
        doc=self.__docs[doc_id]
        for (_col, _val) in doc:
            if _col == col: return _val
        raise RuntimeError("fetch failure for doc_id: " + \
                            doc_id + " col: " + col + " not found")

    def __put(self, doc_id, col, val):
        # updates col (i.e., attribute name) value of doc referred by `doc_id`
        doc=self.__docs[doc_id]
        for index, (_col, _val) in enumerate(doc):
            if _col == col:
                doc[index]=(col, val)
                return
        raise RuntimeError("put failure for doc_id: " + doc_id + \
                " col: " + col + " not found")

