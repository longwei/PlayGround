from unittest import TestCase
from imp_lexer import lex, RESERVED, INT, ID, token_exprs
__author__ = 'longwei'

class TestLex(TestCase):
    def lexer_test(self, code, expected):
        actual = lex(code, token_exprs)
        self.assertEquals(expected, actual)

    def test_empty(self):
        self.lexer_test('', [])

    def test_id(self):
        self.lexer_test('abc', [('abc', ID)])

    def test_keyword_first(self):
        self.lexer_test('if', [('if', RESERVED)])

    def test_int(self):
        self.lexer_test('1', [('1', INT)])

    def test_space(self):
        self.lexer_test('  ', [])

    def test_id_space(self):
        self.lexer_test('abc def', [('abc', ID), ('def', ID)])

if __name__ == "__main__":
    TestCase.main()