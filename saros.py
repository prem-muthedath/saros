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
            "GE01-2": [("name", "GE01"), ("rev", 2), ("prev", 1), ("last", 2), ("content", "i am GE01-2")]
        }

    def link_revs(self):
        for each in self.doc_names():
            Document(each).link_revs(self.last_revs(each), self)
        return self.docs

    def doc_names(self):
        names=[]
        for each in self.docs:
            name=self.docs[each][0][1]
            if name not in names:
                names.append(name)
        return names

    def last_revs(self, doc_name):
        last_revs=[]
        for key in self.docs:
            if doc_name in key:
                doc_rev=self.docs[key][1][1]
                last_rev=self.docs[key][3][1]
                last_revs.append((doc_rev, last_rev))
        return last_revs

    def update_rev_link(self, doc_name, doc_rev, doc):
        doc_id=doc_name + "-" + str(doc_rev)
        doc_xml= [
            "<id>" + doc_id + "</id>",
            "<name>" + self.docs[doc_id][0][1] + "</name>",
            "<rev>" + str(self.docs[doc_id][1][1]) + "</rev>",
            "<prev>" + str(self.docs[doc_id][2][1]) + "</prev>",
            "<last>" + str(self.docs[doc_id][3][1]) + "</last>",
            "<content>" + self.docs[doc_id][4][1] + "</content>"
        ]
        doc.update(doc_xml)
        self.load(doc_xml)
        self.update_last_rev(doc_id)

    def load(self, doc_xml):
        doc_id=""
        vals = []
        for each in doc_xml:
            if each.startswith("<id>"):
                doc_id=self.parse(each, "<id>")
            elif each.startswith("<name>"):
                vals.append(("name", self.parse(each, "<name>")))
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
        name=doc_id.split("-")[0]
        last_rev=self.docs[doc_id][3][1]
        for each in self.docs:
            if each != doc_id and each.startswith(name):
                self.docs[each][3] = ("last", last_rev)

class Document:
    def __init__(self, name):
        self.me = { "name": name, "rev": -1, "prev": -1, "last": -1 } 

    def link_revs(self, last_revs, docs):
        fst, snd = [], []
        last=-1
        for each in last_revs:
            if each[1] > last:
                if last == -1:
                    last=each[1]
                    fst.append(each[0])
                elif last > 0:
                    last=each[1]
                    snd.append(each[0])
            elif each[1] == last:
                if len(snd) == 0:
                    fst.append(each[0])
                else:
                    snd.append(each[0])
        fst.sort(), snd.sort()
        if len(fst) == 0 or len(snd) == 0: return
        if fst[0] < snd[0]:
            self.me["rev"]=snd[0]
            self.me["prev"]=fst[-1]
        elif snd[0] < fst[0]:
            self.me["rev"]=snd[-1]
            self.me["prev"]=fst[0]
        self.me["last"]=last
        docs.update_rev_link(self.me["name"], self.me["rev"], self)

    def update(self, my_xml):
        for index, each in enumerate(my_xml):
            if each.startswith("<rev>"):
                my_xml[index]="<rev>"+str(self.me["rev"])+"</rev>"
            elif each.startswith("<prev>"):
                my_xml[index]="<prev>"+str(self.me["prev"])+"</prev>"
            elif each.startswith("<last>"):
                my_xml[index]="<last>"+str(self.me["last"])+"</last>"



for x, y in Documents().link_revs().items():
    print(x, y)
        
