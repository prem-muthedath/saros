#!/usr/bin/python

# Prem: this code, written in python, links document revisions in saros, a
# document repository

class Documents:
    def __init__(self):
        self.docs = {
            "JE00-1": [("name", "JE00"), ("rev", 1), ("prev", 0), ("last", 3), ("content", "i am JE00-1")],
            "JE00-2": [("name", "JE00"), ("rev", 2), ("prev", 1), ("last", 3), ("content", "i am JE00-2")],
            "JE00-3": [("name", "JE00"), ("rev", 3), ("prev", 2), ("last", 3), ("content", "i am JE00-3")],
            "JE00-4": [("name", "JE00"), ("rev", 4), ("prev", 0), ("last", 6), ("content", "i am JE00-4")],
            "JE00-5": [("name", "JE00"), ("rev", 5), ("prev", 4), ("last", 6), ("content", "i am JE00-5")],
            "JE00-6": [("name", "JE00"), ("rev", 6), ("prev", 5), ("last", 6), ("content", "i am JE00-6")],
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
        self.doc_name=""

    def link_revs(self):
        for each in self.doc_names():
            self.doc_name=each
            DocRevisionChains().link(self.last_revs(), self)
        return self.to_str()

    def doc_names(self):
        names=[]
        for each in self.docs:
            name=self.docs[each][0][1]
            if name not in names:
                names.append(name)
        return names

    def last_revs(self):
        last_revs=[]
        for key in self.docs:
            if self.doc_name in key:
                doc_rev=self.docs[key][1][1]
                last_rev=self.docs[key][3][1]
                last_revs.append((doc_rev, last_rev))
        return last_revs

    def to_str(self):
        val=""
        for each in sorted(self.docs):
            val+=each + ": " + str(self.docs[each]) + "\n"
        return val

    def update_rev_link(self, doc_rev, doc_rev_chains):
        doc_id=self.doc_name + "-" + str(doc_rev)
        doc_xml= [
            "<id>" + doc_id + "</id>",
            "<name>" + self.doc_name + "</name>",
            "<rev>" + str(self.docs[doc_id][1][1]) + "</rev>",
            "<prev>" + str(self.docs[doc_id][2][1]) + "</prev>",
            "<last>" + str(self.docs[doc_id][3][1]) + "</last>",
            "<content>" + self.docs[doc_id][4][1] + "</content>"
        ]
        doc_rev_chains.update(doc_xml)
        self.load(doc_xml)
        self.update_last_rev(doc_id)

    def load(self, doc_xml):
        doc_id=""
        vals = []
        for each in doc_xml:
            if each.startswith("<id>"):
                doc_id=self.parse(each, "<id>")
            elif each.startswith("<name>"):
                vals.append(("name", self.doc_name))
            elif each.startswith("<rev>"):
                vals.append(("rev", int(self.parse(each, "<rev>"))))
            elif each.startswith("<prev>"):
                vals.append(("prev", int(self.parse(each, "<prev>"))))
            elif each.startswith("<last>"):
                vals.append(("last", int(self.parse(each, "<last>"))))
            elif each.startswith("<content>"):
                vals.append(("content", self.parse(each, "<content>")))
        self.docs.pop(doc_id)
        self.docs[doc_id]=vals

    def parse(self, xml_str, xml_tag):
        start=len(xml_tag)
        end=len(xml_str)-(start+1)
        return xml_str[start:end]

    def update_last_rev(self, doc_id):
        last_rev=self.docs[doc_id][3][1]
        for each in self.docs:
            if each != doc_id and each.startswith(self.doc_name):
                self.docs[each][3] = ("last", last_rev)


class DocRevisionChains:
    def __init__(self):
        self.me = { "rev": -1, "prev": -1, "last": -1 }

    def link(self, last_revs, docs):
        # last_revs = [ (rev, last), .., (rev, last) ]
        # rev_chains = { last1: [rev, rev, .., rev],
        #                last2: [rev, rev, .., rev] }
        # algorithm groups revisions by the last revision they point to
        rev_chains={}
        for each in last_revs:
            if each[1] not in rev_chains:
                rev_chains[each[1]]=[each[0]]
            else:
                rev_chains[each[1]].append(each[0])
        if len(rev_chains) > 2:
            raise RuntimeError("> 2 rev chains found")
        if len(rev_chains) < 2:
            return    # no broken links, so skip
        lasts=sorted(rev_chains)
        for last in lasts:
            rev_chains[last].sort()
        self.me["rev"]=rev_chains[lasts[1]][0]
        self.me["prev"]=rev_chains[lasts[0]][-1]
        self.me["last"]=lasts[1]
        docs.update_rev_link(self.me["rev"], self)

    def update(self, my_xml):
        for index, each in enumerate(my_xml):
            if each.startswith("<rev>"):
                my_xml[index]="<rev>"+str(self.me["rev"])+"</rev>"
            elif each.startswith("<prev>"):
                my_xml[index]="<prev>"+str(self.me["prev"])+"</prev>"
            elif each.startswith("<last>"):
                my_xml[index]="<last>"+str(self.me["last"])+"</last>"



print(Documents().link_revs())
 

