#!/usr/bin/python
# -*- coding: utf-8 -*-
# DATE: 2023/02/08
# Author: Irfan TOOR
# file : model.py

from abc import ABC
import sentiment.backend as Model_Backend
import sentiment.ui as Model_UI
import sentiment.transformer as Model_Transformer
import pandas as pd

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
    _model = None
    _vectorizer = None

    def __init__(self, backend=None, ui=None, transformer=None):
        pass

    def backend(self, backend:Model_Backend):
        self._backend = backend

    def ui(self, ui:Model_UI):
        self._ui = ui

    def transformer(self, transformer:Model_Transformer):
        self._transformer = transformer

    def load(self, model_name:str):
        if self._backend is None:
            raise Exception("Backend is not defined")

        result = self._backend.load(model_name)
        if isinstance(result, tuple):
            self._vectorizer, self._model = result
        else:
            self._model = result

    def save(self, model_name:str):
        if self._backend is None:
            raise Exception("Backend is not defined")

        self._backend.save(model_name)

    def predict(self, X_test):
        if self._model is None:
            raise Exception("No model has been loaded")

        if self._vectorizer is not None:
            vector = self._vectorizer.transform(X_test)
            df = pd.DataFrame(
                vector.toarray(),
                columns = self._model.feature_names_in_
            )
        else:
            if isinstance(X_test, pd.DataFrame):
                df = X_test
            else:
                df = pd.DataFrame(
                    X_test,
                    columns = self._model.feature_names_in_
                )

        return self._model.predict(df)

    def serve(self, port=8000):
        if self._ui is None:
            raise Exception("UI is not defined")

        self._ui.serve(port)
