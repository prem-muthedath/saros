#!/usr/bin/python

from .database import _SarosDB
from .revisions import _DocRevisionChains

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
#       -> call Saros db query "last_revs()" with a doc "name" -- say, "goo"
#       -> you get [(rev, last)] -- [(1,3),(3,3),(2,3),(5,7),(4,7),(7,7),(6,7)]
#       -> use this unordered data to do 13 (a), (b), & (c)
# 15.  But Saros database has a quirk -- To do 13 (d):
#       --> Saros db has no query to update "prev" & "last"
#       --> instead, you must ask Saros db for a full XML dump of broken "rev"
#       --> you then update the XML with data from 13 (a), (b), & (c)
#       --> send modified XML to Saros db to load
#       --> Saros db then parses XML & loads data
################################################################################

class Saros:
    # this class represents the saros application.
    # 
    # the only public class in this package, it interfaces with Saros database 
    # (the document repository) & other private classes to link unlinked 
    # document revisions (i.e., fix broken revision links) in Saros database.
    # 
    # other classes involved in the work to link doc revisions must not directly 
    # interact with Saros db; instead, they must work with this class. 

    def __init__(self):
        self.__current_name=""  # "name" of document whose revisions are being linked


    def link_revs(self):
        # spins thru all Saros docs & links all unlinked revisions of each doc
        for each in self.__doc_names():
            self.__current_name=each
            _DocRevisionChains()._link(self.__last_revs(), self)

    def to_str(self):
        # string dump of all docs & their `id`s, ordered by `id`
        val=""
        for (_id, _doc) in _SarosDB()._dump():
            val+=_id + ": " + str(_doc) + "\n"
        return val.strip("\n")

    def __doc_names(self):
        # list of all unique doc names
        return _SarosDB()._doc_names()

    def __last_revs(self):
        # gathers "last" for all revisions of doc named `self.__current_name`
        # returns an unordered [ ("rev", "last") ]
        return _SarosDB()._last_revs(self.__current_name)

    def _update_rev_links(self, doc_xmls):
        # updates revision links in the database
        for doc_xml in doc_xmls:
            _SarosDB()._load(doc_xml)

    def _doc_xml(self, rev):
        # xml dump of doc named `self.__current_name`, revision `rev`
        return _SarosDB()._doc_xml(self.__current_name, rev)


