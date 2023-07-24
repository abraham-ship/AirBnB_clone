#!/usr/bin/python3
import unittest
"""Defines unittests for console.py."""
class HBNBCommand_test(unittest.TestCase):
    """testing the console"""
    def test_prompt(self):
        self.assertEqual("(hbnb) ", HBNBCommand.prompt)
if __name__ == "__main__":
        unittest.main()
