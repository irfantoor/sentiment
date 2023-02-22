#!/usr/bin/python
# -*- coding: utf-8 -*-
# DATE: 2023/02/08
# Author: Irfan TOOR
# file : model.py

from abc import ABC
import sentiment.backend as Model_Backend
import sentiment.ui as Model_UI
import sentiment.transformer as Model_Transformer

class Model(ABC):
    """
    Model class to facilitate loading of the vectorizer and the models from
    Filesystem or MLFlow

    eg:
        model = Model()
        model.load('some/model.b')
        y_pred = model.predict(X_test)
        ...
    """

    _backend = None
    _ui = None
    _transformer = None

    def __init__(self, backend=None, ui=None, transformer=None):
        pass

    def backend(self, backend:Model_Backend):
        self._backend = backend

    def ui(self, ui:Model_UI):
        self._ui = ui

    def transformer(self, transformer:Model_Transformer):
        self._transformer = transformer

    def load(self, model_name:str):
        pass

    def save(self, model_name:str):
        pass

    def predict(self, y_test):
        pass

    def serve(self):
        pass