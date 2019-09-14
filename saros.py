#!/usr/bin/python

# Prem: this code, written in python, links document revisions in saros, a
# document repository

class Documents:
    def __init__(self):
        self.docs = {
            "GE00-1": [("name", "GE00"), ("rev", 1), ("prev", 0), ("last", 3), ("content", "i am GE00-1")],
            "GE00-2": [("name", "GE00"), ("rev", 2), ("prev", 1), ("last", 3), ("content", "i am GE00-2")],
            "GE00-3": [("name", "GE00"), ("rev", 3), ("prev", 2), ("last", 3), ("content", "i am GE00-3")],
            "GE00-4": [("name", "GE00"), ("rev", 4), ("prev", 0), ("last", 6), ("content", "i am GE00-4")],
            "GE00-5": [("name", "GE00"), ("rev", 5), ("prev", 4), ("last", 6), ("content", "i am GE00-5")],
            "GE00-6": [("name", "GE00"), ("rev", 6), ("prev", 5), ("last", 6), ("content", "i am GE00-6")],
            "GE01-1": [("name", "GE01"), ("rev", 1), ("prev", 0), ("last", 2), ("content", "i am GE01-1")],
            "GE01-2": [("name", "GE01"), ("rev", 2), ("prev", 1), ("last", 2), ("content", "i am GE01-2")],
            "GE02-1": [("name", "GE02"), ("rev", 1), ("prev", 0), ("last", 4), ("content", "i am GE02-1")],
            "GE02-2": [("name", "GE02"), ("rev", 2), ("prev", 1), ("last", 4), ("content", "i am GE02-2")],
            "GE02-3": [("name", "GE02"), ("rev", 3), ("prev", 2), ("last", 4), ("content", "i am GE02-3")],
            "GE02-4": [("name", "GE02"), ("rev", 4), ("prev", 3), ("last", 4), ("content", "i am GE02-4")],
            "GE02-5": [("name", "GE02"), ("rev", 5), ("prev", 0), ("last", 7), ("content", "i am GE02-5")],
            "GE02-6": [("name", "GE02"), ("rev", 6), ("prev", 5), ("last", 7), ("content", "i am GE02-6")],
            "GE02-7": [("name", "GE02"), ("rev", 7), ("prev", 6), ("last", 7), ("content", "i am GE02-7")],
            "GE03-1": [("name", "GE03"), ("rev", 1), ("prev", 0), ("last", 1), ("content", "i am GE03-1")]
        }
        self.doc_name=""

    def link_revs(self):
        for each in self.doc_names():
            self.doc_name=each
            DocRevisions().link(self.last_revs(), self)
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

    def update_rev_link(self, doc_rev, doc_revs):
        doc_id=self.doc_name + "-" + str(doc_rev)
        doc_xml= [
            "<id>" + doc_id + "</id>",
            "<name>" + self.doc_name + "</name>",
            "<rev>" + str(self.docs[doc_id][1][1]) + "</rev>",
            "<prev>" + str(self.docs[doc_id][2][1]) + "</prev>",
            "<last>" + str(self.docs[doc_id][3][1]) + "</last>",
            "<content>" + self.docs[doc_id][4][1] + "</content>"
        ]
        doc_revs.update(doc_xml)
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


class DocRevisions:
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
        keys=rev_chains.keys()
        for key in keys:
            rev_chains[key].sort()
        if rev_chains[keys[0]] < rev_chains[keys[1]]:
            self.me["rev"]=rev_chains[keys[1]][0]
            self.me["prev"]=rev_chains[keys[0]][-1]
            self.me["last"]=keys[1]
        elif rev_chains[keys[1]] < rev_chains[keys[0]]:
            self.me["rev"]=rev_chains[keys[1]][-1]
            self.me["prev"]=rev_chains[keys[0]][0]
            self.me["last"]=keys[0]
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
 

