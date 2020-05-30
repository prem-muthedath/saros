#!/usr/bin/python

import unittest

from ..saros import Saros
from ..database.database import _SarosDB
from ..database.schema import _Schema
from ..xml import _File
from ..error import (_FileSchemaError, _FileDataError, _NoSuchDocIdError,)
from . import repo

# test module -- contains all unit tests for saros application.
# ##############################################################################

class Test(unittest.TestCase):
    # tests linking of broken revision chains in Saros
    def setUp(self):
        self._saros=Saros()
        self._docs=_SarosDB()._dump()
        self._fname="test"   # file name

    def tearDown(self):
        self._reset()
        self._saros=None
        self_docs=None
        self._fname=None

    def runTest(self):
        self._header()
        self._verify()
        self._assert()

    def _header(self):
        # print test header
        print " ".join([
                        "\n",
                        "--------------------",
                        "TEST NAME:",
                        self.__class__.__name__,
                        "--------------------"
                    ])

    def _verify(self):
        # verify that saros db is in it's original state
        self.assertEqual(self._saros.to_str(), repo._orig())

    def _assert(self):
        # assert expected result
        self._print("BEFORE")
        self._saros.link_revs()
        self._print("AFTER")
        self.assertEqual(self._saros.to_str(), repo._expected())

    def _print(self, _str):
        # formats & prints saros db state as a string.
        print("SAROS REPOSITORY STATE " +  _str + ": \n" + \
                self._saros.to_str() + "\n")

    def _reset(self):
        # reset saros db to its original state
        for (_id, doc) in self._docs:
            doc=[("id", _id)] + doc
            _File(self._fname)._write(doc)
            self._load()

    def _load(self):
        # load doc data in file to saros db, without linking
        _SarosDB()._load(self._fname, False)

##############################################################################

class TestFileLoad(Test):
    # base class for file load tests
    def _assert(self):
        # assert expected error
        pass

    def _assert_with(self, exception):
        # assert with expected error, expected repo after error.
        # REF: https://docs.python.org/2/library/unittest.html
        with self.assertRaises(exception) as cn:
            self._run()
        print "exception: ", cn.exception.__class__.__name__, \
                "| msg => ", cn.exception
        self.assertEqual(self._saros.to_str(), repo._orig())

    def _run(self):
        # generic `run` method for all tests.
        self._dump()
        self._modify()
        self._load()

    def _data(self):
        # returns (name, rev, field, val)
        pass

    def _dump(self, ):
        # saros doc dump
        name, rev, _, _  = self._data()
        _SarosDB()._doc_dump(name, rev, self._fname)

    def _modify(self):
        # modify doc dump.
        f=_File(self._fname)
        doc=f._read()
        mdoc=self._modify_doc(doc)
        f._write(mdoc)

    def _modify_doc(self, doc):
        # default implementation.
        # set value of doc data `field` to `val`
        _, _, field, val = self._data()
        return [(x, val) if x==field.name else (x, y) for (x, y) in doc]

##############################################################################

class TestEmptyFile(TestFileLoad):
    def _data(self):
        return ("JE00", 4, None, None)

    def _modify_doc(self, doc):
        return []

    def _assert(self):
        self._assert_with(_FileSchemaError)

class TestMissingColumn(TestFileLoad):
    def _data(self):
        return ("JE00", 4, None, None)

    def _modify_doc(self, doc):
        return [(x, y) for i, (x, y) in enumerate(doc) if i != 3]

    def _assert(self):
        self._assert_with(_FileSchemaError)

class TestDuplicate(TestFileLoad):
    def _data(self):
        return ("JE00", 2, None, None)

    def _modify_doc(self, doc):
        doc.append((_Schema.last.name, 15))
        return doc

    def _assert(self):
        self._assert_with(_FileSchemaError)

class TestConsecDuplicate(TestFileLoad):
    def _data(self):
        return ("JE00", 2, None, None)

    def _modify_doc(self, doc):
        doc=[(_Schema.id.name, "JE00-2")] + doc[:-1]
        return doc

    def _assert(self):
        self._assert_with(_FileSchemaError)

class TestBadType(TestFileLoad):
    def _data(self):
        return ("JE00", 4, _Schema.rev, "prem")

    def _assert(self):
        self._assert_with(_FileSchemaError)

class TestSizeMismatch(TestFileLoad):
    def _data(self):
        return ("JE00", 2, None, None)

    def _modify_doc(self, doc):
        doc.append(("silly-me", "problem!"))
        doc.insert(3, ("useless-me", "problem!"))
        return doc

    def _assert(self):
        self._assert_with(_FileSchemaError)

##############################################################################

class TestBadName(TestFileLoad):
    def _data(self):
        return ("JE00", 4, _Schema.name, " ")

    def _assert(self):
        self._assert_with(_FileDataError)

class TestBadRevision(TestFileLoad):
    def _data(self):
        return ("JE00", 4, _Schema.rev, 0)

    def _assert(self):
        self._assert_with(_FileDataError)

class TestBadId(TestFileLoad):
    def _data(self):
        return ("JE02", 2, _Schema.id, "JE02")

    def _assert(self):
        self._assert_with(_FileDataError)

class TestBadPrev(TestFileLoad):
    def _data(self):
        return ("JE02", 2, _Schema.prev, 3)

    def _assert(self):
        self._assert_with(_FileDataError)

class TestBadLast(TestFileLoad):
    def _data(self):
        return ("JE04", 2, _Schema.last, 1)

    def _assert(self):
        self._assert_with(_FileDataError)

##############################################################################

class TestReverseFieldOrder(TestFileLoad):
    def _data(self):
        return ("JE00", 4, None, None)

    def _modify_doc(self, doc):
        return doc[::-1]    # reversed doc contents

    def _assert(self):
        self._run()
        self.__print()
        self.assertEqual(self._saros.to_str(), repo._orig())

    def __print(self):
        print "=> file data:\n  " + ",\n  ".join(self.__fdata())

    def __fdata(self):
        return [str((x, y)) for (x, y) in _File(self._fname)._read()]

##############################################################################

class TestNoSuchId(TestFileLoad):
    def _data(self):
        return ("JE04", 2, None, None)

    def _modify_doc(self, doc):
        data=[(_Schema.id, "JE04-4"),
                (_Schema.rev, 4),
                (_Schema.prev, 3),
                (_Schema.last, 4)
            ]
        for (x, y) in data:
            doc=[(a, y) if a==x.name else (a, b) for (a, b) in doc]
        return doc

    def _assert(self):
        self._assert_with(_NoSuchDocIdError)

##############################################################################

# `TestFileLoad` deleted; else, unittest will run it.
# `TestFileLoad` is a base class, & doesn't test anything, so no need to run it.
# for del(TestFileLoad) trick, see /u/ Wojciech B @ https://tinyurl.com/yb58qtae
del(TestFileLoad)

def main():
    # calls unittest.main() to run tests.
    # to use:
    #   1. call this method in saros.__main__.py
    #   2. then run `python -m saros` to execute runTest()
    #   3. ref: https://docs.python.org/2/library/unittest.html#unittest.main
    unittest.main(module='saros.test.test')

def suite():
    # runs tests as test suite.
    # to use:
    #   1. call this method in saros.__main__.py;
    #   2. to execute runTest(), run `python -m saros` in the commandline.
    suite=unittest.TestSuite()
    suite.addTest(Test())   # we're using runTest(), so need not pass test method name to Test()
    unittest.TextTestRunner().run(suite)


