__author__ = 'rna'

from NeedlemanWunsch.Alignment import Alingment
from unittest import TestCase

class AlignmentTest(TestCase):

    def test_get_x(self):
        algn = Alingment("A-CGU-", "-A--CA")
        x = algn.get_sequence_x()
        self.assertEqual("ACGU", x)

    def test_change_x(self):
        algn = Alingment("ACGU-", "-A-C-")
        algn.change_sequence_x("UGCA")
        x = algn.get_sequence_x()
        self.assertEqual("UGCA", x)


