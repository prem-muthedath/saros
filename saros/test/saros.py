#!/usr/bin/python

import unittest
from ..saros import Saros

class Test(unittest.TestCase):
    # tests linking of broken revision chains in Saros
    def setUp(self):
        self.__saros=Saros()

    def tearDown(self):
        self.__saros=None

    def runTest(self):
        self.__print("BEFORE")
        self.__saros.link_revs()
        self.__print("AFTER")
        self.assertEqual(self.__saros.to_str(), self.__expected_repo())

    def __print(self, _str):
        print("SAROS REPOSITORY STATE " +  _str + ": \n" + self.__saros.to_str() + "\n")

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

def run():
    suite=unittest.TestSuite()
    suite.addTest(Test())   # we're using runTest(), so need not pass test method name to Test()
    unittest.TextTestRunner().run(suite)

