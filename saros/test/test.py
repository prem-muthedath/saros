#!/usr/bin/python

import unittest
from ..saros import Saros
from ..database import _SarosDB
from ..xml import _File
from . import data
from ..error import (_NonPositiveRevisionError,
                    _LastBelowRevisionError,
                    _DuplicateRevisionsError,
                    _DecreasingLastError,
                    _NonConsecutiveRevisionsError,
                    _MissingLinksError,
                    )

# test module -- contains all unit tests for saros application
# ##############################################################################

class Test(unittest.TestCase):
    # tests linking of broken revision chains in Saros
    def setUp(self):
        self._saros=Saros()
        self._docs=_SarosDB()._dump()
        self._file="test"

    def tearDown(self):
        self._reset()
        self._saros=None
        self_docs=None
        self._file=None

    def runTest(self):
        self._header()
        self._verify()
        self._setUp()
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
        self.assertEqual(self._saros.to_str(), data._orig_repo())

    def _setUp(self):
        # set up test data, in addition to Test.setUp()
        pass

    def _assert(self):
        # assert expected result
        self._print("BEFORE")
        self._saros.link_revs()
        self._print("AFTER")
        self.assertEqual(self._saros.to_str(), data._expected_repo())

    def _print(self, _str):
        # formats & prints saros db state as a string.
        print("SAROS REPOSITORY STATE " +  _str + ": \n" + \
                self._saros.to_str() + "\n")

    def _reset(self):
        # reset saros db to its original state
        for (_id, doc) in self._docs:
            doc=[("id", _id)] + doc
            _File(self._file)._write(doc)
            self._load()

    def _load(self):
        # load doc data in file to saros db, without linking
        _SarosDB()._load(self._file, False)


class TestError(Test):
    # base class for error tests
    def _setUp(self):
        # set up test data, in addition to Test.setUp()
        # super().setUp() doesn't work because we del(TestError) -- see below
        # test setup may involve multiple changes, including > 1 row, to db.
        for (name, rev, field, val) in self._data():
            self._dump(name, rev)
            self._modify(field, val)
            self._load()

    def _data(self):
        # test data: [(name, rev, field, val)]
        pass

    def _dump(self, name, rev):
        # saros doc dump
        _SarosDB()._doc_dump(name, rev, self._file)

    def _modify(self, field, val):
        # set value of doc data `field` to `val`
        f=_File(self._file)
        doc=f._read()
        mdoc=[(x, val) if x==field else (x, y) for (x, y) in doc]
        f._write(mdoc)

    def _assert(self):
        # assert expected error
        pass

    def _assert_with(self, exception):
        # assert with expected error
        # REF: https://docs.python.org/2/library/unittest.html
        with self.assertRaises(exception) as cn:
            self._saros.link_revs()
        print "exception: ", cn.exception.__class__.__name__, \
                "| msg => ", cn.exception


class TestRevNotPositive(TestError):
    # tests rev <=0
    def _data(self):
        return [("JE00", 1, "rev", -1)]

    def _assert(self):
        self._assert_with(_NonPositiveRevisionError)

class TestLastNotPositive(TestError):
    # tests last <= 0
    def _data(self):
        return [("JE00", 2, "last", -10)]

    def _assert(self):
        self._assert_with(_LastBelowRevisionError)

class TestLastBelowRev(TestError):
    # tests last < rev
    def _data(self):
        return [("JE00", 3, "last", 1)]

    def _assert(self):
        self._assert_with(_LastBelowRevisionError)

class TestDuplicate(TestError):
    # tests duplicates
    def _data(self):
        return [("JE02", 5, "rev", 4)]

    def _assert(self):
        self._assert_with(_DuplicateRevisionsError)

class TestDecLast(TestError):
    # tests decreasing last
    def _data(self):
        return [("JE02", 6, "last", 6)]

    def _assert(self):
        self._assert_with(_DecreasingLastError)

class TestNonConsec(TestError):
    # tests non-consecutive revs
    def _data(self):
        return [("JE00", 5, "rev", 6)]

    def _assert(self):
        self._assert_with(_NonConsecutiveRevisionsError)

class TestPrevMissing(TestError):
    # tests missing links in previous chain
    def _data(self):
        return [
                ("JE00", 1, "last", 5),
                ("JE00", 2, "last", 5),
                ("JE00", 3, "last", 5)
            ]

    def _assert(self):
        self._assert_with(_MissingLinksError)

class TestEndMissing(TestError):
    # tests missing links @ end
    def _data(self):
        return [("JE03", 1, "last", 8)]

    def _assert(self):
        self._assert_with(_MissingLinksError)


# `TestError` deleted; else, unittest will run it.
# `TestError` is a base class, & doesn't test anything, so no need to run it.
# for del(TestError) trick, see /u/ Wojciech B @ https://tinyurl.com/yb58qtae
del(TestError)

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


