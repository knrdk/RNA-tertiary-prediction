__author__ = 'rna'

from unittest import TestCase

from Utils.Alignment import Alingment


class AlignmentTest(TestCase):

    def test_get_x(self):
        algn = Alingment("A-CGU-", "-A--CA")
        x = algn.get_template_sequence()
        self.assertEqual("ACGU", x)

    def test_change_x(self):
        algn = Alingment("ACGU-", "-A-C-")
        algn.change_template_sequence("UGCA")
        x = algn.get_template_sequence()
        self.assertEqual("UGCA", x)


