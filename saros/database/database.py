from collections import OrderedDict

from ..xml import _File
from .schema import (_Schema, _file_load_schema,)
from ..error import (_NoSuchDocIdError, _NoSuchColumnError,)

# this module contains the saros db class.
# ##############################################################################

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
    # 3. saros db maintains good data, with the exception that revisions may be 
    #    unlinked.  good data means that data have right types; revisions 
    #    consecutive; `id`, `name`, `last`, `prev`, & `content` values proper.
    # 4. saros has no api to add a document. the only way to update data in 
    #    saros is through a file upload. so based on (3), the `schema` module 
    #    offers a basic schema validation for file data.  and saros app fixes 
    #    any broken links.  so with those 2 things, saros db should be fine.

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
            name=cls.__fetch(doc_id, _Schema.name)
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
                rev=cls.__fetch(doc_id, _Schema.rev)
                last=cls.__fetch(doc_id, _Schema.last)
                last_revs.append((rev, last))
        return last_revs

    @classmethod
    def _doc_dump(cls, name, rev, fname):
        # dumps doc named `name`, revision `rev` as xml into file named `fname`
        doc_id=cls.__doc_id(name, rev)
        data=cls.__doc_data(doc_id)    # fixed to avoid nasty bugs
        doc=[(_Schema.id.name, doc_id)] + data
        _File(fname)._write(doc)

    @classmethod
    def _load(cls, fname, link=True):
        # loads xml doc info contained in file named `fname` into the database.
        # by default (i.e., `link`=True), updates `last` of upstream revs.
        doc=OrderedDict(_File(fname)._parse(_file_load_schema()))
        name, rev=(doc[_Schema.name.name], doc[_Schema.rev.name])
        doc_id=cls.__doc_id(name, rev)
        doc.pop(_Schema.id.name)            # pop the doc id
        cls.__put(doc_id, doc.items())
        if link:
            cls.__update_links(doc_id)

    @classmethod
    def __doc_data(cls, doc_id):
        # returns doc data, as a new list, for `doc_id`.
        # new list reqd; otherwise, any local changes, made either by clients or 
        # by saros, will be reflected everywhere, creating nasty bugs.
        if not cls.__docs.has_key(doc_id):
            raise _NoSuchDocIdError(doc_id)
        return [item for item in cls.__docs[doc_id]]

    @classmethod
    def __doc_id(cls, name, rev):
        # returns id of doc named `name`, revision `rev`
        return name + "-" + str(rev)

    @classmethod
    def __update_links(cls, doc_id):
        # doc_id -> id of doc whose revision link has just been updated.
        # name -> name associated with `doc_id`
        # rev -> revision associated with `doc_id`
        # last -> last associated with `doc_id`
        #
        # for all revs `_rev` of doc named `name`, update links -- i.e., `last` 
        # values -- if `_rev` < `rev`.
        last=cls.__fetch(doc_id, _Schema.last)
        name=cls.__fetch(doc_id, _Schema.name)
        rev=cls.__fetch(doc_id, _Schema.rev)
        for (_rev, _) in cls._last_revs(name):
            if _rev < rev:    # fix for a nasty bug
                _id=cls.__doc_id(name, _rev)
                data=[(_Schema.last.name, last)]
                cls.__put(_id, data)

    @classmethod
    def __fetch(cls, doc_id, col):
        # given a doc_id & col (i.e., attribute), returns the value
        doc=cls.__doc_data_dict(doc_id)
        if doc.has_key(col.name):
            return doc[col.name]
        raise _NoSuchColumnError(doc_id, col.name)

    @classmethod
    def __put(cls, doc_id, data):
        # updates data -- [(col_name, val)] -- of doc referred by `doc_id`
        doc=cls.__doc_data_dict(doc_id)
        for (col_name, val) in data:
            if not doc.has_key(col_name):
                raise _NoSuchColumnError(doc_id, col_name)
            doc[col_name]=val
        cls.__docs[doc_id]=doc.items()

    @classmethod
    def __doc_data_dict(cls, doc_id):
        # returns an ord dict of doc data, allowing easy lookup.
        return OrderedDict(cls.__doc_data(doc_id))




