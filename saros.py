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
#       -> the latest revision number ("last") ~ total # of revisions
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
#       -> same "last" ~ same total # of revisions
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
#           -> for last=7 => [4, 5, 6]
# 13. To fix the problem in (12), we must:
#       (a) spot the "rev" with broken link -> rev 4
#       (b) determine its right "prev" value -> "prev"=3
#       (c) determine its right "last" value -> "last"=7
#       (d) update Saros with (a), (b), & (c)
#       (e) Saros will then update all "rev"s "last" to same value -> "last"=7
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
    # this class models Saros document repository.  it is the only public class 
    # in this module. it works with a private class to link document revisions.
    def __init__(self):
        # self_docs = { doc_id: [ ("name", val), ("rev", val), ("prev", val), ("content", val) ] }
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
        self.__doc_name=""  # current document whose revisions are being linked


    def link_revs(self):
        for each in self.__doc_names():
            self.__doc_name=each
            _DocRevisionChains()._link(self.__last_revs(), self)

    def to_str(self):
        val=""
        for each in sorted(self.__docs):
            val+=each + ": " + str(self.__docs[each]) + "\n"
        return val

    def __doc_names(self):
        names=[]
        for doc_id in self.__docs:
            name=self.__fetch(doc_id, "name")
            if name not in names:
                names.append(name)
        return names

    def __last_revs(self):
        # returns an unordered [ ("rev", "last") ]
        last_revs=[]
        for doc_id in self.__docs:
            if self.__doc_name in doc_id:
                doc_rev=self.__fetch(doc_id, "rev")
                last_rev=self.__fetch(doc_id, "last")
                last_revs.append((doc_rev, last_rev))
        return last_revs

    def _update_rev_links(self, doc_revs, doc_rev_chains):
        doc_id=""
        doc_xmls=[]
        for doc_rev in doc_revs:
            doc_id=self.__doc_name + "-" + str(doc_rev)
            doc_xmls.append(self.__doc_xml(doc_id))
        doc_rev_chains._update(doc_xmls)
        for doc_xml in doc_xmls:
            self.__load(doc_xml)
        self.__update_last_rev(doc_id)

    def __doc_xml(self, doc_id):
        return [
            "<id>" + doc_id + "</id>",
            "<name>" + self.__doc_name + "</name>",
            "<rev>" + str(self.__fetch(doc_id, "rev")) + "</rev>",
            "<prev>" + str(self.__fetch(doc_id, "prev")) + "</prev>",
            "<last>" + str(self.__fetch(doc_id, "last")) + "</last>",
            "<content>" + self.__fetch(doc_id, "content") + "</content>"
        ]

    def __load(self, doc_xml):
        doc_id=""
        vals = []
        for each in doc_xml:
            if each.startswith("<id>"):
                doc_id=self.__parse(each, "<id>")
            elif each.startswith("<name>"):
                vals.append(("name", self.__doc_name))
            elif each.startswith("<rev>"):
                vals.append(("rev", int(self.__parse(each, "<rev>"))))
            elif each.startswith("<prev>"):
                vals.append(("prev", int(self.__parse(each, "<prev>"))))
            elif each.startswith("<last>"):
                vals.append(("last", int(self.__parse(each, "<last>"))))
            elif each.startswith("<content>"):
                vals.append(("content", self.__parse(each, "<content>")))
        self.__docs.pop(doc_id)
        self.__docs[doc_id]=vals

    def __parse(self, xml_str, xml_tag):
        start=len(xml_tag)
        end=len(xml_str)-(start+1)
        return xml_str[start:end]

    def __update_last_rev(self, doc_id):
        last_rev=self.__fetch(doc_id, "last")
        for _id in self.__docs:
            if _id!= doc_id and _id.startswith(self.__doc_name):
                self.__put(_id, "last", last_rev)

    def __fetch(self, doc_id, col):
        doc=self.__docs[doc_id]
        for (_col, _val) in doc:
            if _col == col: return _val
        raise RuntimeError("fetch failure for doc_id: " + \
                            doc_id + " col: " + col + " not found")

    def __put(self, doc_id, col, val):
        doc=self.__docs[doc_id]
        for index, (_col, _val) in enumerate(doc):
            if _col == col:
                doc[index]=(col, val)
                return
        raise RuntimeError("put failure for doc_id: " + doc_id + \
                " col: " + col + " not found")


class _DocRevisionChains:
    # builds doc revision chains, spots broken revision links, & works with 
    # Saros to link them.
    def __init__(self):
        # self.__broken_links = { rev: (prev, last) }
        self.__broken_links = {}

    def _link(self, last_revs, saros):
        # last_revs = [ (rev, last), .., (rev, last) ]
        # rev_chains = { last1: [rev, rev, .., rev],
        #                last2: [rev, rev, .., rev] }
        # algorithm groups revisions by their last revision.  Each group is a 
        # revision chain, & if we've > 1, we've broken revision links.
        rev_chains={}
        for (rev, last) in last_revs:
            if last not in rev_chains:
                rev_chains[last]=[rev]
            else:
                rev_chains[last].append(rev)
        if len(rev_chains) < 2:
            return    # no broken links, so skip
        self.__extract_broken_links(rev_chains)
        saros._update_rev_links(sorted(self.__broken_links), self)

    def __extract_broken_links(self, rev_chains):
        lasts=sorted(rev_chains)
        last=lasts[-1]
        for each in lasts:
            rev_chains[each].sort()
        for index, each in enumerate(lasts[1:]):
            # scan all rev chains for broken rev links; gather & link them.
            # broken rev link is where a rev is without a valid prev.
            # 1st rev in a rev chain is a broken link, because it has no prev.
            # skip first rev chain, however, as its 1st rev can not have a prev.
            # the 1st rev in all other rev chains is a broken rev link.
            # index starts @ 0, but we loop from [1:], so index -> prev item.
            prev_last=lasts[index]
            rev=rev_chains[each][0]
            prev=rev_chains[prev_last][-1]
            self.__broken_links[rev]=(prev, last)

    def _update(self, xmls):
        revs=sorted(self.__broken_links)
        for rev, xml in zip(revs, xmls):
            self.__update_link(rev, xml)

    def __update_link(self, rev, xml):
        prev,last=self.__fetch(rev)
        for index, each in enumerate(xml):
            if each.startswith("<prev>"):
                xml[index]="<prev>"+str(prev)+"</prev>"
            elif each.startswith("<last>"):
                xml[index]="<last>"+str(last)+"</last>"

    def __fetch(self, rev):
        return self.__broken_links[rev]


if __name__ == "__main__":
    saros=Saros()
    print("SAROS REPOSITORY STATE BEFORE: \n" + saros.to_str())
    saros.link_revs()
    print("SAROS REPOSITORY STATE AFTER: \n" + saros.to_str())


