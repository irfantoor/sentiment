#!/usr/bin/python
# -*- coding: utf-8 -*-
# DATE: 2023/02/22
# Author: Irfan TOOR
# file : tests/test_model.py

import unittest
from unittest.mock import Mock, create_autospec, patch
from sentiment import Model

class ModelTest(unittest.TestCase):

    def test_assert(self):
        self.assertTrue(True)

    def test_model_instance(self):
        model = Model()
        self.assertIsInstance(model, Model)
