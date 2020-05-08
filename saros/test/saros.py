#!/usr/bin/python

import unittest
from ..saros import Saros
from ..database import _SarosDB
from ..xml import _File
from ..document import (_NonPositiveLinkError,
                        _LastBelowRevisionError,
                        _DuplicateLinkError,
                        _DecreasingLastError,
                        _NonConsecutiveRevisionsError,
                        _MissingLinksError,
                        )

class Test(unittest.TestCase):
    # tests linking of broken revision chains in Saros
    def setUp(self):
        self._saros=Saros()
        self._docs=_SarosDB()._dump()
        self._file="test"

    def tearDown(self):
        # reset saros to its original state
        for (_id, doc) in self._docs:
            doc=[("id", _id)] + doc
            _File(self._file)._write(doc)
            _SarosDB._load(self._file)
        self._saros=None
        self_docs=None
        self._file=None

    def runTest(self):
        self._print("BEFORE")
        self._saros.link_revs()
        self._print("AFTER")
        self.assertEqual(self._saros.to_str(), self.__expected_repo())

    def _print(self, _str):
        print("SAROS REPOSITORY STATE " +  _str + ": \n" + self._saros.to_str() + "\n")

    def __expected_repo(self):
        return '\n'.join([
            "JE00-1: [('name', 'JE00'), ('rev', 1), ('prev', 0), ('last', 8), ('content', 'i am JE00-1')]",
            "JE00-2: [('name', 'JE00'), ('rev', 2), ('prev', 1), ('last', 8), ('content', 'i am JE00-2')]",
            "JE00-3: [('name', 'JE00'), ('rev', 3), ('prev', 2), ('last', 8), ('content', 'i am JE00-3')]",
            "JE00-4: [('name', 'JE00'), ('rev', 4), ('prev', 3), ('last', 8), ('content', 'i am JE00-4')]",
            "JE00-5: [('name', 'JE00'), ('rev', 5), ('prev', 4), ('last', 8), ('content', 'i am JE00-5')]",
            "JE00-6: [('name', 'JE00'), ('rev', 6), ('prev', 5), ('last', 8), ('content', 'i am JE00-6')]",
            "JE00-7: [('name', 'JE00'), ('rev', 7), ('prev', 6), ('last', 8), ('content', 'i am JE00-7')]",
            "JE00-8: [('name', 'JE00'), ('rev', 8), ('prev', 7), ('last', 8), ('content', 'i am JE00-8')]",
            "JE01-1: [('name', 'JE01'), ('rev', 1), ('prev', 0), ('last', 2), ('content', 'i am JE01-1')]",
            "JE01-2: [('name', 'JE01'), ('rev', 2), ('prev', 1), ('last', 2), ('content', 'i am JE01-2')]",
            "JE02-1: [('name', 'JE02'), ('rev', 1), ('prev', 0), ('last', 7), ('content', 'i am JE02-1')]",
            "JE02-2: [('name', 'JE02'), ('rev', 2), ('prev', 1), ('last', 7), ('content', 'i am JE02-2')]",
            "JE02-3: [('name', 'JE02'), ('rev', 3), ('prev', 2), ('last', 7), ('content', 'i am JE02-3')]",
            "JE02-4: [('name', 'JE02'), ('rev', 4), ('prev', 3), ('last', 7), ('content', 'i am JE02-4')]",
            "JE02-5: [('name', 'JE02'), ('rev', 5), ('prev', 4), ('last', 7), ('content', 'i am JE02-5')]",
            "JE02-6: [('name', 'JE02'), ('rev', 6), ('prev', 5), ('last', 7), ('content', 'i am JE02-6')]",
            "JE02-7: [('name', 'JE02'), ('rev', 7), ('prev', 6), ('last', 7), ('content', 'i am JE02-7')]",
            "JE03-1: [('name', 'JE03'), ('rev', 1), ('prev', 0), ('last', 1), ('content', 'i am JE03-1')]"
        ])


class TestError(Test):
    # base class for error tests
    def runTest(self):
        self._setUp()
        self._assert()

    def _setUp(self):
        # set up test data, in addition to Test.setUp()
        # super().setUp() doesn't work because we del(TestError) -- see below
        self._doc_dump()
        f=_File(self._file)
        doc=f._read()
        mdoc=self._modified_doc(doc)
        f._write(mdoc)
        _SarosDB()._load(self._file)

    def _doc_dump(self):
        # saros doc dump
        pass

    def _modified_doc(self, doc):
        # doc with data modified for test
        pass

    def _assert(self):
        # assert expected error
        pass

class TestRevNotPositive(TestError):
    # tests rev <=0
    def _doc_dump(self):
        _SarosDB()._doc_dump("JE00", 1, self._file)

    def _modified_doc(self, doc):
        return [(x, -1) if x=="rev" else (x, y) for (x, y) in doc]

    def _assert(self):
        self.assertRaises(_NonPositiveLinkError, self._saros.link_revs)

class TestLastNotPositive(TestError):
    # tests last <= 0
    def _doc_dump(self):
        _SarosDB()._doc_dump("JE00", 2, self._file)

    def _modified_doc(self, doc):
        return [(x, -10) if x=="last" else (x, y) for (x, y) in doc]

    def _assert(self):
        self.assertRaises(_NonPositiveLinkError, self._saros.link_revs)

class TestLastBelowRev(TestError):
    # tests last < rev
    def _doc_dump(self):
        _SarosDB()._doc_dump("JE00", 3, self._file)

    def _modified_doc(self, doc):
        return [(x, 1) if x=="last" else (x, y) for (x, y) in doc]

    def _assert(self):
        self.assertRaises(_LastBelowRevisionError, self._saros.link_revs)

class TestDuplicate(TestError):
    # tests duplicates
    def _doc_dump(self):
        _SarosDB()._doc_dump("JE02", 7, self._file)

    def _modified_doc(self, doc):
        return [(x, 6) if x=="rev" else (x, y) for (x, y) in doc]

    def _assert(self):
        self.assertRaises(_DuplicateLinkError, self._saros.link_revs)

class TestDecLast(TestError):
    # tests decreasing last
    def _doc_dump(self):
        _SarosDB()._doc_dump("JE02", 6, self._file)

    def _modified_doc(self, doc):
        return [(x, 6) if x=="last" else (x, y) for (x, y) in doc]

    def _assert(self):
        self.assertRaises(_DecreasingLastError, self._saros.link_revs)

class TestNonConsec(TestError):
    # tests non-consecutive revs
    def _doc_dump(self):
        _SarosDB()._doc_dump("JE00", 5, self._file)

    def _modified_doc(self, doc):
        return [(x, 6) if x=="rev" else (x, y) for (x, y) in doc]

    def _assert(self):
        self.assertRaises(_NonConsecutiveRevisionsError, self._saros.link_revs)

class TestMidMissing(TestError):
    # tests missing links in middle
    def _doc_dump(self):
        _SarosDB()._doc_dump("JE02", 6, self._file)

    def _modified_doc(self, doc):
        return [(x, 8) if x=="last" else (x, y) for (x, y) in doc]

    def _assert(self):
        self.assertRaises(_MissingLinksError, self._saros.link_revs)

class TestEndMissing(TestError):
    # tests missing links @ end
    def _doc_dump(self):
        _SarosDB()._doc_dump("JE03", 1, self._file)

    def _modified_doc(self, doc):
        return [(x, 8) if x=="last" else (x, y) for (x, y) in doc]

    def _assert(self):
        self.assertRaises(_MissingLinksError, self._saros.link_revs)


# `TestError` deleted; else, unittest will run it, & abstract methods will fail.
# for del(TestError) trick, see /u/ Wojciech B @ https://tinyurl.com/yb58qtae
del(TestError)

def main():
    # calls unittest.main() to run tests.
    # to use:
    #   1. call this method in saros.__main__.py
    #   2. then run `python -m saros` to execute runTest()
    #   3. ref: https://docs.python.org/2/library/unittest.html#unittest.main
    unittest.main(module='saros.test.saros')

def suite():
    # runs tests as test suite.
    # to use:
    #   1. call this method in saros.__main__.py;
    #   2. to execute runTest(), run `python -m saros` in the commandline.
    suite=unittest.TestSuite()
    suite.addTest(Test())   # we're using runTest(), so need not pass test method name to Test()
    unittest.TextTestRunner().run(suite)


