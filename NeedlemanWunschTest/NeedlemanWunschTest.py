__author__ = 'Konrad Kopciuch'

from unittest import TestCase

from NeedlemanWunsch.NeedlemanWunsch import NeedlemanWunsch
from Utils.Alignment import Alignment


#dane do testow: https://blast.ncbi.nlm.nih.gov/Blast.cgi?PAGE_TYPE=BlastSearch&PROG_DEF=blastn&BLAST_PROG_DEF=blastn&BLAST_SPEC=GlobalAln&LINK_LOC=BlastHomeLink
class NeedlemanWunschTest(TestCase):

    def test_not_string_sequence(self):
        subject = 1
        query = "adsad"
        self.assertRaises(AssertionError, NeedlemanWunsch, query, subject)
        self.assertRaises(AssertionError, NeedlemanWunsch, subject, query)

    def test_get_score_before_align(self):
        s = "a"
        q = "b"
        nw = NeedlemanWunsch(s,q)
        self.assertRaises(RuntimeError, nw.get_score)

    def test_alignment_score(self):
        subject = "UGGAGAGUUUGAUCCUGGCUCAGGGUGAACGCUGGCGGCGUGCCUAAGACAUGCAAGUCGUGCGGGCCGCGGGGUUUUACUCCGUGGUCAGCGGCGGACGGGUGAGUAACGCGUGGGUGACCUACCCGGAAGAGGGGGACAACCCGGGGAAACUCGGGCUAAUCCCCCAUGUGGACCCGCCCCUUGGGGUGUGUCCAAAGGGCUUUGCCCGCUUCCGGAUGGGCCCGCGUCCCAUCAGCUAGUUGGUGGGGUAAUGGCCCACCAAGGCGACGACGGGUAGCCGGUCUGAGAGGAUGGCCGGCCACAGGGGCACUGAGACACGGGCCCCACUCCUACGGGAGGCAGCAGUUAGGAAUCUUCCGCAAUGGGCGCAAGCCUGACGGAGCGACGCCGCUUGGAGGAAGAAGCCCUUCGGGGUGUAAACUCCUGAACCCGGGACGAAACCCCCGACGAGGGGACUGACGGUACCGGGGUAAUAGCGCCGGCCAACUCCGUGCCAGCAGCCGCGGUAAUACGGAGGGCGCGAGCGUUACCCGGAUUCACUGGGCGUAAAGGGCGUGUAGGCGGCCUGGGGCGUCCCAUGUGAAAGACCACGGCUCAACCGUGGGGGAGCGUGGGAUACGCUCAGGCUAGACGGUGGGAGAGGGUGGUGGAAUUCCCGGAGUAGCGGUGAAAUGCGCAGAUACCGGGAGGAACGCCGAUGGCGAAGGCAGCCACCUGGUCCACCCGUGACGCUGAGGCGCGAAAGCGUGGGGAGCAAACCGGAUUAGAUACCCGGGUAGUCCACGCCCUAAACGAUGCGCGCUAGGUCUCUGGGUCUCCUGGGGGCCGAAGCUAACGCGUUAAGCGCGCCGCCUGGGGAGUACGGCCGCAAGGCUGAAACUCAAAGGAAUUGACGGGGGCCCGCACAAGCGGUGGAGCAUGUGGUUUAAUUCGAAGCAACGCGAAGAACCUUACCAGGCCUUGACAUGCUAGGGAACCCGGGUGAAAGCCUGGGGUGCCCCGCGAGGGGAGCCCUAGCACAGGUGCUGCAUGGCCGUCGUCAGCUCGUGCCGUGAGGUGUUGGGUUAAGUCCCGCAACGAGCGCAACCCCCGCCGUUAGUUGCCAGCGGUUCGGCCGGGCACUCUAACGGGACUGCCCGCGAAAGCGGGAGGAAGGAGGGGACGACGUCUGGUCAGCAUGGCCCUUACGGCCUGGGCGACACACGUGCUACAAUGCCCACUACAAAGCGAUGCCACCCGGCAACGGGGAGCUAAUCGCAAAAAGGUGGGCCCAGUUCGGAUUGGGGUCUGCAACCCGACCCCAUGAAGCCGGAAUCGCUAGUAAUCGCGGAUCAGCCAUGCCGCGGUGAAUACGUUCCCGGGCCUUGUACACACCGCCCGUCACGCCAUGGGAGCGGGCUCUACCCGAAGUCGCCGGGAGCCUACGGGCAGGCGCCGAGGGUAGGGCCCGUGACUGGGGCGAAGUCGUAACAAGGUAGCUGUACCGGAAGGUGCGGCUGGAUCA"
        query = "GAAUUGCGGGAAAGGGGUCAACAGCCGUUCAGUACCAAGUCUCAGGGGAAACUUUGAGAUGGCCUUGCAAAGGGUAUGGUAAUAAGCUGACGGACAUGGUCCUAACCACGCAGCCAAGUCCUAAGUCAACAGAUCUUCUGUUGAUAUGGAUGCAGUUC"
        expected_score = -2617
        nw = NeedlemanWunsch(subject, query)
        nw.set_points(2, -3, -5, -2)
        nw.align()
        score = nw.get_score()
        self.assertEqual(expected_score, score)

    def test_alignment_score_2(self):
        subject = "GGCGCGUUAACAAAGCGGUUAUGUAGCGGAUUGCAAAUCCGUCUAGUCCGGUUCGACUCCGGAACGCGCCUCCA"
        query = "CUCUGUUUACCAGGUCAGGUCCGGAAGGAAGCAGCCAAGGCAGAG"
        expected_score = -83
        nw = NeedlemanWunsch(subject, query)
        nw.set_points(2, -3, -5, -2)
        nw.align()
        score = nw.get_score()
        self.assertEqual(expected_score, score)

    def test_alignment_score_2_different_parameters(self):
        subject = "GGCGCGUUAACAAAGCGGUUAUGUAGCGGAUUGCAAAUCCGUCUAGUCCGGUUCGACUCCGGAACGCGCCUCCA"
        query = "CUCUGUUUACCAGGUCAGGUCCGGAAGGAAGCAGCCAAGGCAGAG"
        expected_score = -148
        nw = NeedlemanWunsch(subject, query)
        nw.set_points(4, -5, -6, -5)
        nw.align()
        score = nw.get_score()
        self.assertEqual(expected_score, score)

    def test_alignment_score_3(self):
        subject = "GGGAAA"
        query = "GGG"
        expected_score = -5
        nw = NeedlemanWunsch(subject, query)
        nw.set_points(2, -3, -5, -2)
        nw.align()
        score = nw.get_score()
        self.assertEqual(expected_score, score)

    def test_alignment(self):
        subject = "GGCGCGUUAACAAAGCGGUUAUGUAGCGGAUUGCAAAUCCGUCUAGUCCGGUUCGACUCCGGAACGCGCCUCCA"
        query = "CUCUGUUUACCAGGUCAGGUCCGGAAGGAAGCAGCCAAGGCAGAG"
        nw = NeedlemanWunsch(subject, query)
        nw.set_points(2,-3,-5,-2)
        nw.align()
        alingment = nw.get_alignment()

        expected_subject_alignment = "GGCGCGUUAACAAAGCGGUUAUGUAGCGGAUUGCAAAUCCGUCUAGUCCGGUUCGACUCCGGAACGCGCCUCCA"
        expected_query_alignment =   "CUCUGUUUACCA----GGUCAGGUC-CGGAAGG--AAGCAGCCAAGGCAGAG----------------------"
        expected_alignment = Alignment(expected_subject_alignment,expected_query_alignment)

        self.assertEqual(alingment.get_identity_percent(), expected_alignment.get_identity_percent())

