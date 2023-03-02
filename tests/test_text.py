#!/usr/bin/python
# -*- coding: utf-8 -*-
# DATE: 2023/03/02
# Author: Irfan TOOR
# file : tests/test_ui.py

import unittest
from sentiment.text import Tokenizer, pad_sequences

lines = [['Hello', 'World'], ['Its', 'a', 'test']]

class UiTest(unittest.TestCase):

    def test_tokenizer(self):
        tokenizer = Tokenizer(num_words=10)
        self.assertIsInstance(tokenizer, Tokenizer)

        # these are just to make sure that keras has been loaded
        tokenizer.fit_on_texts(lines)
        result = tokenizer.texts_to_sequences(lines)
        self.assertEqual(result, [[1, 2], [3, 4, 5]])


    def test_pad_sequence(self):
        tokenizer = Tokenizer(num_words=10)
        tokenizer.fit_on_texts(lines)
        sequences = tokenizer.texts_to_sequences(lines)
        result = pad_sequences(sequences, maxlen=10)
        expected = [[0, 0, 0, 0, 0, 0, 0, 0, 1, 2], [0, 0, 0, 0, 0, 0, 0, 3, 4, 5]]
        for r, e in zip(result, expected):
            for rr, ee in zip(r, e):
                self.assertEqual(rr, ee)
