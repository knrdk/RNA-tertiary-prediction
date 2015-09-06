__author__ = 'rna'

from unittest import TestCase

from SCFG.SecondaryStructureToSCFGParser import SecondaryStructureToSCFGParser
from SCFG.ScoringMatrix import get_scoring_matrices


class SecondaryStructureToSCFGParserTest(TestCase):

    def test_short_sequences_1(self):
        expected_score = 7.39
        ss, sq = ".()", "AGC"
        single_matrix, double_matrix = get_scoring_matrices()
        parser = SecondaryStructureToSCFGParser(single_matrix, double_matrix)
        scfg = parser.get_SCFG(ss, sq)
        sequence = "AGC"
        scfg.align(sequence)
        score = scfg.get_score()
        self.assertEqual(expected_score, score)

    def test_short_sequences_2(self):
        expected_score = -0.9700000000000002
        ss, sq = ".()", "AGC"
        single_matrix, double_matrix = get_scoring_matrices()
        parser = SecondaryStructureToSCFGParser(single_matrix, double_matrix)
        scfg = parser.get_SCFG(ss, sq)
        sequence = "AAC"
        scfg.align(sequence)
        score = scfg.get_score()
        self.assertEqual(expected_score, score)

    def test_medium_sequences_1(self):
        expected_score = 89.57
        ss, sq = "((((........))))......(((((....)))))...............", \
                 "GGCGAUGAGGCCCGCCCAAACUGCCCUGAAAAGGGCUGAUGGCCUCUACUG"
        single_matrix, double_matrix = get_scoring_matrices()
        parser = SecondaryStructureToSCFGParser(single_matrix, double_matrix)
        scfg = parser.get_SCFG(ss, sq)
        sequence = "GGCGAUGAGGCCCGCCCAAACUGCCCUGAAAAGGGCUGAUGGCCUCUACUG"
        scfg.align(sequence)
        score = scfg.get_score()
        self.assertEqual(expected_score, score)