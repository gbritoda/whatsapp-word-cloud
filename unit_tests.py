""" Simple unit testing

Run with

    python -m unittest unit_tests.py
"""

from unittest import TestCase

import main

class TestStopWords(TestCase):
    def test_remove_stopwords(self):
        res = main.remove_stopwords("je ne te le dirai pas", "french")
        assert res == "dirai", res
