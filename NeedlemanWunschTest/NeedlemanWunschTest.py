__author__ = 'Konrad Kopciuch'

from unittest import TestCase

from NeedlemanWunsch.NeedlemanWunsch import NeedlemanWunsch
from Utils.Alignment import Alignment

'''
dane do testow pochodza z implementacj algorytmu N-W w BLAST:
https://blast.ncbi.nlm.nih.gov/Blast.cgi?PAGE_TYPE=BlastSearch&PROG_DEF=blastn&BLAST_PROG_DEF=blastn&BLAST_SPEC=GlobalAln&LINK_LOC=BlastHomeLink
'''
class NeedlemanWunschTest(TestCase):

    def test_not_string_sequence(self):
        template = 1
        query = "adsad"

        self.assertRaises(AssertionError, NeedlemanWunsch, query, template)
        self.assertRaises(AssertionError, NeedlemanWunsch, template, query)

    def test_get_score_before_align(self):
        s = "a"
        q = "b"
        nw = NeedlemanWunsch(s,q)

        self.assertRaises(RuntimeError, nw.get_score)

    def test_alignment_score(self):
        template = "UGGAGAGUUUGAUCCUGGCUCAGGGUGAACGCUGGCGGCGUGCCUAAGACAUGCAAGUCGUGCGGGCCGCGGGGUUUUACUCCGUGGUCAGCGGCGGACGGGUGAGUAACGCGUGGGUGACCUACCCGGAAGAGGGGGACAACCCGGGGAAACUCGGGCUAAUCCCCCAUGUGGACCCGCCCCUUGGGGUGUGUCCAAAGGGCUUUGCCCGCUUCCGGAUGGGCCCGCGUCCCAUCAGCUAGUUGGUGGGGUAAUGGCCCACCAAGGCGACGACGGGUAGCCGGUCUGAGAGGAUGGCCGGCCACAGGGGCACUGAGACACGGGCCCCACUCCUACGGGAGGCAGCAGUUAGGAAUCUUCCGCAAUGGGCGCAAGCCUGACGGAGCGACGCCGCUUGGAGGAAGAAGCCCUUCGGGGUGUAAACUCCUGAACCCGGGACGAAACCCCCGACGAGGGGACUGACGGUACCGGGGUAAUAGCGCCGGCCAACUCCGUGCCAGCAGCCGCGGUAAUACGGAGGGCGCGAGCGUUACCCGGAUUCACUGGGCGUAAAGGGCGUGUAGGCGGCCUGGGGCGUCCCAUGUGAAAGACCACGGCUCAACCGUGGGGGAGCGUGGGAUACGCUCAGGCUAGACGGUGGGAGAGGGUGGUGGAAUUCCCGGAGUAGCGGUGAAAUGCGCAGAUACCGGGAGGAACGCCGAUGGCGAAGGCAGCCACCUGGUCCACCCGUGACGCUGAGGCGCGAAAGCGUGGGGAGCAAACCGGAUUAGAUACCCGGGUAGUCCACGCCCUAAACGAUGCGCGCUAGGUCUCUGGGUCUCCUGGGGGCCGAAGCUAACGCGUUAAGCGCGCCGCCUGGGGAGUACGGCCGCAAGGCUGAAACUCAAAGGAAUUGACGGGGGCCCGCACAAGCGGUGGAGCAUGUGGUUUAAUUCGAAGCAACGCGAAGAACCUUACCAGGCCUUGACAUGCUAGGGAACCCGGGUGAAAGCCUGGGGUGCCCCGCGAGGGGAGCCCUAGCACAGGUGCUGCAUGGCCGUCGUCAGCUCGUGCCGUGAGGUGUUGGGUUAAGUCCCGCAACGAGCGCAACCCCCGCCGUUAGUUGCCAGCGGUUCGGCCGGGCACUCUAACGGGACUGCCCGCGAAAGCGGGAGGAAGGAGGGGACGACGUCUGGUCAGCAUGGCCCUUACGGCCUGGGCGACACACGUGCUACAAUGCCCACUACAAAGCGAUGCCACCCGGCAACGGGGAGCUAAUCGCAAAAAGGUGGGCCCAGUUCGGAUUGGGGUCUGCAACCCGACCCCAUGAAGCCGGAAUCGCUAGUAAUCGCGGAUCAGCCAUGCCGCGGUGAAUACGUUCCCGGGCCUUGUACACACCGCCCGUCACGCCAUGGGAGCGGGCUCUACCCGAAGUCGCCGGGAGCCUACGGGCAGGCGCCGAGGGUAGGGCCCGUGACUGGGGCGAAGUCGUAACAAGGUAGCUGUACCGGAAGGUGCGGCUGGAUCA"
        query = "GAAUUGCGGGAAAGGGGUCAACAGCCGUUCAGUACCAAGUCUCAGGGGAAACUUUGAGAUGGCCUUGCAAAGGGUAUGGUAAUAAGCUGACGGACAUGGUCCUAACCACGCAGCCAAGUCCUAAGUCAACAGAUCUUCUGUUGAUAUGGAUGCAGUUC"
        expected_score = -2617

        nw = NeedlemanWunsch(template, query)
        nw.set_points(2, -3, -5, -2)
        nw.align()
        score = nw.get_score()

        self.assertEqual(expected_score, score)

    def test_alignment_score_2(self):
        template = "GGCGCGUUAACAAAGCGGUUAUGUAGCGGAUUGCAAAUCCGUCUAGUCCGGUUCGACUCCGGAACGCGCCUCCA"
        query = "CUCUGUUUACCAGGUCAGGUCCGGAAGGAAGCAGCCAAGGCAGAG"
        expected_score = -83

        nw = NeedlemanWunsch(template, query)
        nw.set_points(2, -3, -5, -2)
        nw.align()
        score = nw.get_score()

        self.assertEqual(expected_score, score)

    def test_alignment_score_2_different_parameters(self):
        template = "GGCGCGUUAACAAAGCGGUUAUGUAGCGGAUUGCAAAUCCGUCUAGUCCGGUUCGACUCCGGAACGCGCCUCCA"
        query = "CUCUGUUUACCAGGUCAGGUCCGGAAGGAAGCAGCCAAGGCAGAG"
        expected_score = -148

        nw = NeedlemanWunsch(template, query)
        nw.set_points(4, -5, -6, -5)
        nw.align()
        score = nw.get_score()

        self.assertEqual(expected_score, score)

    def test_alignment_score_3(self):
        template = "GGGAAA"
        query = "GGG"
        expected_score = -5

        nw = NeedlemanWunsch(template, query)
        nw.set_points(2, -3, -5, -2)
        nw.align()
        score = nw.get_score()

        self.assertEqual(expected_score, score)

    def test_alignment(self):
        template = "GGCGCGUUAACAAAGCGGUUAUGUAGCGGAUUGCAAAUCCGUCUAGUCCGGUUCGACUCCGGAACGCGCCUCCA"
        query = "CUCUGUUUACCAGGUCAGGUCCGGAAGGAAGCAGCCAAGGCAGAG"

        nw = NeedlemanWunsch(template, query)
        nw.set_points(2,-3,-5,-2)
        nw.align()
        alingment = nw.get_alignment()

        expected_template_alignment = "GGCGCGUUAACAAAGCGGUUAUGUAGCGGAUUGCAAAUCCGUCUAGUCCGGUUCGACUCCGGAACGCGCCUCCA"
        expected_query_alignment = "CUCUGUUUACCA----GGUCAGGUC-CGGAAGG--AAGCAGCCAAGGCAGAG----------------------"
        expected_alignment = Alignment(expected_template_alignment,expected_query_alignment)

        self.assertEqual(alingment.get_identity_percent(), expected_alignment.get_identity_percent())

