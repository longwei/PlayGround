__author__ = 'longwei'


import sys
import unittest

if __name__ == '__main__':
    test_names = ['test_lex', 'test_combinators', 'test_parser']
    suite = unittest.defaultTestLoader.loadTestsFromNames(test_names)
    result = unittest.TextTestRunner().run(suite)