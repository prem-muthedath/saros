#!/usr/bin/python

import unittest

from ..saros import Saros
from ..database.database import _SarosDB
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
        self._setup()
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

    def _setup(self):
        # set up data in addition to `setUp()`
        pass

    def _assert(self):
        # assert expected result
        self._print("BEFORE")
        self._saros.link_revs()
        self._print("AFTER")
        self.assertEqual(self._saros.to_str(), repo._expected())

    def _print(self, _str=""):
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
        # assert expected value
        pass

    def _assert_with(self, exception, msg):
        # assert with expected error, expected repo after error.
        # REF: https://docs.python.org/2/library/unittest.html
        with self.assertRaises(exception) as cn:
            self._load()
        print "exception: ", cn.exception.__class__.__name__, \
                "| msg => ", cn.exception
        self._print()
        self.assertEqual(self._saros.to_str(), repo._orig())
        self.assertTrue(cn.exception.__str__().startswith(msg))

    def _setup(self):
        doc=self._doc()
        _File(self._fname)._write(doc)

    def _doc(self):
        # returns test doc data = [(name, value), ..., (name, value)]
        pass

    def _print(self, _str=""):
        print "=> file data:\n  " + ",\n  ".join(self.__fdata())

    def __fdata(self):
        return [str((x, y)) for (x, y) in self._doc()]

##############################################################################

class TestEmptyFile(TestFileLoad):
    def _doc(self):
        return []

    def _assert(self):
        msg="schema column 'id' missing"
        self._assert_with(_FileSchemaError, msg)

class TestMissingColumn(TestFileLoad):
    def _doc(self):
        return [
                ("id", "J00-4"),
                ("name", "JE00"),
                ("rev", 4),
                ("last", 6),
                ("content", "i am JE00-4")
            ]

    def _assert(self):
        msg="schema column 'prev' missing"
        self._assert_with(_FileSchemaError, msg)

class TestDuplicate(TestFileLoad):
    def _doc(self):
        return [
                ("id", "JE00-2"),
                ("name", "JE00"),
                ("rev", 2),
                ("prev", 1),
                ("last", 3),
                ("content", "i am JE00-2"),
                ("last", 3),
            ]

    def _assert(self):
        msg="schema column 'last' duplicated"
        self._assert_with(_FileSchemaError, msg)

class TestConsecDuplicate(TestFileLoad):
    def _doc(self):
        return [
                ("id", "JE00-2"),
                ("id", "JE00-2"),
                ("name", "JE00"),
                ("rev", 2),
                ("prev", 1),
                ("last", 3)
            ]

    def _assert(self):
        msg="schema column 'id' duplicated"
        self._assert_with(_FileSchemaError, msg)

class TestBadType(TestFileLoad):
    def _doc(self):
        return [
                ("id", "J00-4"),
                ("name", "JE00"),
                ("rev", "prem"),
                ("prev", 0),
                ("last", 6),
                ("content", "i am JE00-4")
            ]

    def _assert(self):
        msg="schema column 'rev' data type != 'int'"
        self._assert_with(_FileSchemaError, msg)

class TestBadIdType(TestFileLoad):
    # happens when `name` is empty.
    def _doc(self):
        return [
                ("id", "-4"),
                ("name", ""),
                ("rev", 4),
                ("prev", 3),
                ("last", 6),
                ("content", "i am -4")
            ]

    def _assert(self):
        msg="schema column 'id' data type != 'str'"
        self._assert_with(_FileSchemaError, msg)

class TestSizeMismatch(TestFileLoad):
    def _doc(self):
        return [
                ("id", "JE00-2"),
                ("name", "JE00"),
                ("rev", 2),
                ("useless-me", "problem!"),
                ("prev", 1),
                ("last", 3),
                ("content", "i am JE00-2"),
                ("silly-me", "problem!")
            ]

    def _assert(self):
        msg="non-schema columns 'useless-me, silly-me'"
        self._assert_with(_FileSchemaError, msg)

##############################################################################

class TestBadName(TestFileLoad):
    def _doc(self):
        return [
                ("id", " -4"),
                ("name", " "),
                ("rev", 4),
                ("prev", 0),
                ("last", 6),
                ("content", "i am  -4")
            ]

    def _assert(self):
        msg="doc 'name' is empty or whitespace"
        self._assert_with(_FileDataError, msg)

class TestBadRevision(TestFileLoad):
    def _doc(self):
        return [
                ("id", "J00-0"),
                ("name", "JE00"),
                ("rev", 0),
                ("prev", 0),
                ("last", 6),
                ("content", "i am JE00-0")
            ]

    def _assert(self):
        msg="doc revision < 1"
        self._assert_with(_FileDataError, msg)

class TestBadId(TestFileLoad):
    def _doc(self):
        return [
                ("id", "JE02"),
                ("name", "JE02"),
                ("rev", 2),
                ("prev", 1),
                ("last", 4),
                ("content", "i am JE02-2")
            ]

    def _assert(self):
        msg="doc id not equal to 'JE02-2'"
        self._assert_with(_FileDataError, msg)

class TestBadPrev(TestFileLoad):
    def _doc(self):
        return [
                ("id", "JE02-2"),
                ("name", "JE02"),
                ("rev", 2),
                ("prev", 3),
                ("last", 4),
                ("content", "i am JE02-2")
            ]

    def _assert(self):
        msg="doc's 'prev' neither 0 nor 'rev' - 1"
        self._assert_with(_FileDataError, msg)

class TestBadLast(TestFileLoad):
    def _doc(self):
        return [
                ("id", "JE04-2"),
                ("name", "JE04"),
                ("rev", 2),
                ("prev", 0),
                ("last", 1),
                ("content", "i am JE04-2")
            ]

    def _assert(self):
        msg="doc's 'last' <  'rev'"
        self._assert_with(_FileDataError, msg)

##############################################################################

class TestReverseFieldOrder(TestFileLoad):
    def _doc(self):
        return [
                ("content", "i am JE00-4"),
                ("last", 6),
                ("prev", 0),
                ("rev", 4),
                ("name", "JE00"),
                ("id", "JE00-4")
            ]

    def _assert(self):
        self._load()
        self._print()
        self.assertEqual(self._saros.to_str(), repo._orig())

##############################################################################

class TestNoSuchId(TestFileLoad):
    def _doc(self):
        return [
                ("id", "JE04-4"),
                ("name", "JE04"),
                ("rev", 4),
                ("prev", 3),
                ("last", 4),
                ("content", "i am JE04-4")
            ]

    def _assert(self):
        msg="doc id 'JE04-4', generated from `name` & `rev` values, " + \
                "does not exist in the db."
        self._assert_with(_NoSuchDocIdError, msg)

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


