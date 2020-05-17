#!/usr/bin/python

from .xml import _File

class _SarosDB:
    # this private class models Saros database -- the document repository.  it 
    # offers methods for typical database operations -- queries & updates.
    #
    # NOTE:
    # there is no API, however, to link doc revisions; instead, clients must:
    # 1. request XML dump of a specific doc revision (i.e., doc name & revision)
    # 2. update XML with valid revision link info, & send it to SarosDB to load
    # 3. SarosDB then parses XML, & loads data
    # 4. After load, by default, SarosDB updates "last" of all revisions of the 
    #    doc whose "last" < "last" of the just updated link.
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
    # 5. each row should have valid "prev" & "last" values; if not, we'll have 
    #    broken revision chains.  Saros database, however, does not enforce this 
    #    rule, so any broken revision links must be fixed thru a data update.
    #
    # DESIGN:
    # 1. the database -- __docs (see below) -- is modeled as a class variable, 
    #    so that all _SarosDB instances share the same data, & database updates 
    #    from any _SarosDB instance are available to all _SarosDB instances.
    # 2. to make (1) work, all methods are class methods, but you can still use 
    #    _SarosDB().method().  ref: https://pythonbasics.org/classmethod/

    # __docs = { doc_id: [ ("name", val), ("rev", val), ("prev", val), ("last", val), ("content", val) ] }
    __docs = { # represents the database
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
        "JE03-1": [("name", "JE03"), ("rev", 1), ("prev", 0), ("last", 1), ("content", "i am JE03-1")],
        "JE04-1": [("name", "JE04"), ("rev", 1), ("prev", 0), ("last", 1), ("content", "i am JE04-1")],
        "JE04-2": [("name", "JE04"), ("rev", 2), ("prev", 0), ("last", 2), ("content", "i am JE04-2")]
    }

    @classmethod
    def _dump(cls):
        # dump of all docs & their `id`s, sorted by `id`
        # returns [(doc_id, doc_data)], where doc_data=[(column, value)]
        dump=[]
        for _id in sorted(cls.__docs):
            data=cls.__doc_data(_id)    # fix for a nasty bug
            dump.append((_id, data))
        return dump

    @classmethod
    def _doc_names(cls):
        # list of all unique doc names, sorted by name
        names=[]
        for doc_id in cls.__docs:
            name=cls.__fetch(doc_id, "name")
            if name not in names:
                names.append(name)
        return sorted(names)

    @classmethod
    def _last_revs(cls, name):
        # gathers "last" for all revisions of doc named `name`
        # returns an unordered [ ("rev", "last") ]
        last_revs=[]
        for doc_id in cls.__docs:
            if name in doc_id:
                rev=cls.__fetch(doc_id, "rev")
                last=cls.__fetch(doc_id, "last")
                last_revs.append((rev, last))
        return last_revs

    @classmethod
    def _doc_dump(cls, name, rev, fname):
        # dumps doc named `name`, revision `rev` as xml into file named `fname`
        doc_id=cls.__doc_id(name, rev)
        data=cls.__doc_data(doc_id)    # fixed to avoid potential nasty bugs
        doc=[("id", doc_id)] + data
        _File(fname)._write(doc)

    @classmethod
    def _load(cls, fname, link=True):
        # loads xml doc info contained in file named `fname` into the database.
        # by default (i.e., `link`=True), updates `last` of upstream revs.
        doc_id=""
        vals=[]
        for (name, val) in _File(fname)._read():
            if name=="id":
                 doc_id=val
            else:
                vals.append((name,val))
        cls.__docs.pop(doc_id)
        cls.__docs[doc_id]=vals
        if link:
            cls.__update_last(doc_id)

    @classmethod
    def __doc_data(cls, doc_id):
        # returns doc data, as a new list, for a given `doc_id`
        # new list reqd; otherwise, any local changes, made either by clients or 
        # by saros, will be reflected everywhere, creating nasty bugs.
        return [item for item in cls.__docs[doc_id]]

    @classmethod
    def __update_last(cls, doc_id):
        # doc_id -> id of doc whose revision link has just been updated.
        # name -> name associated with `doc_id`
        # rev -> revision associated with `doc_id`
        # last -> last associated with `doc_id`
        #
        # for all revs of doc named `name`, update `last` if `_rev` < `rev`
        last=cls.__fetch(doc_id, "last")
        name=cls.__fetch(doc_id, "name")
        rev=cls.__fetch(doc_id, "rev")
        for (_rev, _) in cls._last_revs(name):
            if _rev >= rev: continue    # fix for a nasty bug
            _id=cls.__doc_id(name, _rev)
            cls.__put(_id, "last", last)

    @classmethod
    def __doc_id(cls, name, rev):
        # returns id of doc named `name`, revision `rev`
        return name + "-" + str(rev)

    @classmethod
    def __fetch(cls, doc_id, col):
        # given a doc_id & col (i.e., attribute name), returns the value
        doc=cls.__docs[doc_id]
        for (_col, _val) in doc:
            if _col == col: return _val
        raise RuntimeError("fetch failure for doc_id: " + \
                            doc_id + " col: " + col + " not found")

    @classmethod
    def __put(cls, doc_id, col, val):
        # updates col (i.e., attribute name) value of doc referred by `doc_id`
        doc=cls.__docs[doc_id]
        for index, (_col, _val) in enumerate(doc):
            if _col == col:
                doc[index]=(col, val)
                return
        raise RuntimeError("put failure for doc_id: " + doc_id + \
                " col: " + col + " not found")


