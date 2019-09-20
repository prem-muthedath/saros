#!/usr/bin/python

# Prem: this code, written in python, links document revisions in Saros, a
# fictitious document repository.
#
################################################################################
# NOTE:
# 1. Saros stores documents and their revisions.
# 2. Each document ("doc") has:
#       -> name
#       -> revision number ("rev")
#       -> immediate preceding revision ("prev")
#       -> content
#       -> the latest revision number ("last") ~ total revisions in the chain
# 3. Revision numbers start from 1, & increase by 1.
# 4. Example -- if doc "foo" has been revised 7 times, then its 4th revision:
#       -> name: foo
#       -> rev:  4
#       -> prev: 3
#       -> last: 7
#       -> content: "hey, i am foo"
# 5. For the example in (4), the end cases will be:
#       -> rev=1 => prev=0, last=7
#       -> rev=7 => prev=6, last=7
# 6. In Saros, no 2 docs can have the same "name" & "rev". For example:
#       -> "foo" rev=2 -- possible
#       -> "foo" rev=3 -- possible
#       -> "foo" rev=4 -- possible
#       -> "foo" rev=2 -- repeat NOT possible
# 7. Saros indexes docs:
#       -> using a generated unique document id
#       -> an id refers to a doc with unique combination of "name" & "rev"
# 8. Saros requires that all "rev"s of a doc with the same "name" must have:
#       -> valid & unique "prev"s
#       -> same "last" ~ same total # of revisions in the chain
# 9. Saros, however, is not perfect -- some docs have broken revision links
# 10. Terminology [ see example in (4) ]:
#       -> revision links & revision chains refer to a doc with same "name"
#       -> revision link: ("prev", "rev", "last")  => (3, 4, 7)
#       -> revision chain: linked "rev"s with same "last" => [1,2,3,4,5,6,7]
# 11. A broken revision link is where:
#       -> a "rev" does not have a valid & unique "prev"
#       -> "last" not ~ "last" of other links, so we've > 1 revision chain
# 12. Example -- broken revision link:
#       -> doc "goo" has total 7 revisions
#       -> rev 1 => prev=0, last=3
#       -> rev 2 => prev=1, last=3
#       -> rev 3 => prev=2, last=3
#
#       -> rev 4 => prev=0, last=7  --> broken: prev != 3
#       -> rev 5 => prev=4, last=7
#       -> rev 6 => prev=5, last=7
#       -> rev 7 => prev=6, last=7
#
#       -> links don't have same "last", so we've 2 revision chains:
#           -> for last=3 => [1, 2, 3]
#           -> for last=7 => [4, 5, 6, 7]
# 13. To fix the problem in (12), we must (for a doc with a specific "name"):
#       (a) spot the "rev" with broken link -> rev 4
#       (b) determine its right "prev" value -> "prev"=3
#       (c) determine its right "last" value -> "last"=7
#       (d) update Saros with (a), (b), & (c)
#       (e) after 13(d), Saros sets "last" of all "rev"s whose "last" < 7 to 7.
# 14. To do 13 (a), (b), & (c) [ see example in (12) ]:
#       -> call Saros API "last_revs()" with a doc "name" -- say, "goo"
#       -> you get [(rev, last)] -- [(1,3),(3,3),(2,3),(5,7),(4,7),(7,7),(6,7)]
#       -> use this unordered data to do 13 (a), (b), & (c)
# 15.  But Saros has a quirk -- To do 13 (d):
#       --> Saros has no API to update "prev" & "last"
#       --> instead, you must request Saros for a full XML dump of broken "rev"
#       --> you then update the XML with data from 13 (a), (b), & (c)
#       --> send modified XML to Saros to load
#       --> Saros then parses XML & loads data
################################################################################


class Saros:
    # this class models Saros document repository.  the only public class in 
    # this module, it works with private classes to link document revisions.
    def __init__(self):
        # self_docs = { doc_id: [ ("name", val), ("rev", val), ("prev", val), ("last", val), ("content", val) ] }
        self.__docs = {
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
        self.__current_name=""  # "name" of document whose revisions are being linked


    def link_revs(self):
        # spins thru all docs & links all unlinked revisions of each doc
        for each in self.__doc_names():
            self.__current_name=each
            _DocRevisionChains()._link(self.__last_revs(), self)

    def to_str(self):
        # string dump of all docs & their `id`s
        val=""
        for each in sorted(self.__docs):
            val+=each + ": " + str(self.__docs[each]) + "\n"
        return val

    def __doc_names(self):
        # list of all unique doc names
        names=[]
        for doc_id in self.__docs:
            name=self.__fetch(doc_id, "name")
            if name not in names:
                names.append(name)
        return names

    def __last_revs(self):
        # gathers "last" for all revisions of doc `self.__current_name`
        # returns an unordered [ ("rev", "last") ]
        last_revs=[]
        for doc_id in self.__docs:
            if self.__current_name in doc_id:
                rev=self.__fetch(doc_id, "rev")
                last=self.__fetch(doc_id, "last")
                last_revs.append((rev, last))
        return last_revs

    def _update_rev_links(self, rev_links):
        # updates revision links in the database
        doc_xmls=[]
        for rev_link in rev_links:
            doc_xmls.append(rev_link._to_xml(self))
        for doc_xml in doc_xmls:
            doc_id=self.__load(doc_xml)
            self.__update_last(doc_id)

    def _doc_xml(self, rev):
        # xml dump of doc named `self.__current_name`, revision `rev`
        doc_id=self.__current_doc_id(rev)
        xml=[ _Attribute(("id", doc_id))._to_xml() ]
        for each in self.__docs[doc_id]:
            xml.append(_Attribute(each)._to_xml())
        return xml

    def __load(self, doc_xml):
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
        return doc_id

    def __update_last(self, doc_id):
        # for all revs of doc named `self.__current_name` whose "last" < "last" 
        # of just updated link, replaces "last" with "last" of updated link.
        # doc_id -> id of doc whose revision link has just been updated.
        last=self.__fetch(doc_id, "last")
        for (_rev, _last) in self.__last_revs():
            _id=self.__current_doc_id(_rev)
            if _last < last and _id != doc_id:
                self.__put(_id, "last", last)

    def __current_doc_id(self, rev):
        # returns id of doc named `self.__current_name`, revision `rev`
        return self.__current_name + "-" + str(rev)

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


class _DocRevisionChains:
    # builds doc revision chains, spots unlinked revisions, & works with Saros 
    # to link them.
    def __init__(self):
        # self.__rev_chains = { last: [rev, rev, ..., rev ] }
        self.__rev_chains = {}

    def _link(self, last_revs, saros):
        # identifies & links broken revision chains
        #
        # last_revs = [ (rev, last), .., (rev, last) ]
        # rev_chains = { last1: [rev, rev, .., rev],
        #                last2: [rev, rev, .., rev] }
        # NOTE: last_revs is unordered either by rev or by last
        #
        # algorithm groups revisions by their last revision.  Each group is a 
        # revision chain, & if we've > 1, we've broken revision chains.
        for (rev, last) in last_revs:
            if last not in self.__rev_chains:
                self.__rev_chains[last]=[rev]
            else:
               self.__rev_chains[last].append(rev)
        if self.__no_broken_links():    # skip if no broken links
            return
        rev_links=self.__correct_rev_links()
        saros._update_rev_links(rev_links)

    def __correct_rev_links(self):
        # returns correct revision links to fix broken revision chains
        rev_links=[]
        lasts=sorted(self.__rev_chains)
        for each in lasts:
            self.__rev_chains[each].sort()
        for index, each in enumerate(lasts[1:]):
            # scan all rev chains for broken rev links & return corrected links.
            # broken rev link is where a rev is without a valid prev.
            # 1st rev in a rev chain is a broken link, because it has no prev.
            # skip first rev chain, however, as its 1st rev can not have a prev.
            # the 1st rev in all other rev chains is a broken rev link.
            # index starts @ 0, but we loop from [1:], so index -> prev item.
            prev_last=lasts[index]
            prev=self.__rev_chains[prev_last][-1]
            rev=self.__rev_chains[each][0]
            rev_links.append(_RevisionLink(prev, rev, each))
        return rev_links

    def __no_broken_links(self):
        # if we've broken revision links, we'll have > 1 rev chain
        return len(self.__rev_chains) < 2


class _RevisionLink:
    # represents a revision link
    def __init__(self, prev, rev, last):
        self.__prev=prev    # "rev"'s previous revision
        self.__rev=rev      # revision
        self.__last=last    # last revision in the chain "rev" belongs

    def _to_xml(self, saros):
        # returns xml dump of current doc with right revision link info
        xml=saros._doc_xml(self.__rev)
        return self.__update(xml)

    def __update(self, xml):
        for index, each in enumerate(xml):
            name, _ = _XmlElement(each)._parse()
            if name == "prev":
                xml[index]=_Attribute((name, self.__prev))._to_xml()
            elif name == "last":
                xml[index]=_Attribute((name, self.__last))._to_xml()
        return xml


class _Attribute:
    # represents a (name, value) pair
    def __init__(self, (name, val)):
        self.__name, self.__val=(name, val)

    def _to_xml(self):
        # returns an xml element
        return "<" + self.__name + ">" + self.__good_val() + "</" + self.__name + ">"

    def __good_val(self):
        # converts int to str
        if isinstance(self.__val, int):
            return str(self.__val)
        return self.__val


class _XmlElement:
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


if __name__ == "__main__":
    saros=Saros()
    print("SAROS REPOSITORY STATE BEFORE: \n" + saros.to_str())
    saros.link_revs()
    print("SAROS REPOSITORY STATE AFTER: \n" + saros.to_str())


