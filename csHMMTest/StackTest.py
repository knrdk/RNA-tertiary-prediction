__author__ = 'Konrad Kopciuch'

from unittest import TestCase
from csHMM.Stack import Stack

class StackTest(TestCase):

    def test_push_one_pop_one(self):
        original_value = 4

        stack = Stack()
        stack.push(original_value)
        value = stack.pop()
        self.assertEqual(value, original_value)

    def test_push_two_pop_one(self):
        first_value = 1
        second_value = 2

        stack = Stack()
        stack.push(first_value)
        stack.push(second_value)

        value = stack.pop()
        self.assertEqual(second_value, value)
        value = stack.pop()
        self.assertEqual(first_value, value)

    def test_pop_from_empty(self):
        stack = Stack()
        self.assertRaises(IndexError, stack.pop)

    def test_is_empty(self):
        stack = Stack()
        self.assertTrue(stack.is_empty())

    def test_is_empty_after_push(self):
        stack = Stack()
        stack.push(0)
        self.assertFalse(stack.is_empty())

    def test_is_empty_after_pop(self):
        stack = Stack()
        stack.push(0)
        stack.pop()
        self.assertTrue(stack.is_empty())
