__author__ = 'Konrad Kopciuch'

from unittest import TestCase
from SCFG.SecondaryStructureParser import SecondaryStructureParser

class SecondaryStructureParserTest(TestCase):

    def test_number_of_states_test1(self):
        expected_number_of_states = 13

        ss, sq = ".()", "AAA"
        parser = SecondaryStructureParser()
        tree = parser.get_tree(ss, sq)
        self.assertEqual(expected_number_of_states, tree.get_number_of_states())

    def test_number_of_states_test2(self):
        expected_number_of_states = 24

        ss, sq = ".()()", "AAAAA"
        parser = SecondaryStructureParser()
        tree = parser.get_tree(ss, sq)
        self.assertEqual(expected_number_of_states, tree.get_number_of_states())

    def test_number_of_states_test3(self):
        expected_number_of_states = 81

        ss, sq = "..(((....).)).((.(...)))", "ACGUACGUACGUACGUACGUACGU"
        parser = SecondaryStructureParser()
        tree = parser.get_tree(ss, sq)
        self.assertEqual(expected_number_of_states, tree.get_number_of_states())