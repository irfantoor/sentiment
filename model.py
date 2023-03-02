#!/usr/bin/python
# -*- coding: utf-8 -*-
# DATE: 2023/02/08
# Author: Irfan TOOR
# file : model.py

from abc import ABC
import sentiment.backend as Model_Backend
import sentiment.ui as Model_UI
import sentiment.transformer as Model_Transformer
from sentiment.text import Tokenizer
from sentiment.text import pad_sequences

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
    _tokenizer = None

    # tokenizer
    _max_len = 100
    _num_words = 20000

    def __init__(self, backend=None, ui=None, transformer=None):
        return

    def backend(self, backend:Model_Backend):
        self._backend = backend

    def ui(self, ui:Model_UI):
        self._ui = ui

    def transformer(self, transformer:Model_Transformer):
        self._transformer = transformer

    def int_tokenizer(self, phrases, num_words:int=20000, max_len:int=100):
        self._max_len = max_len
        self._num_words = num_words
        self._tokenizer = Tokenizer(num_words=num_words)
        self._tokenizer.fit_on_texts(phrases)

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

    def get_backend(self):
        return self._backend

    def get_ui(self):
        return self._ui

    def get_transformer(self):
        return self._transformer

    def get_model(self):
        return self._model

    def get_vectorizer(self):
        return self._vectorizer

    def get_tokenizer(self):
        return self._tokenizer

    def predict(self, phrases):
        if self._model is None:
            raise Exception("No model has been loaded")

        if isinstance(phrases, str):
            phrases = [phrases]

        # pipeline
        data = [self.pipeline(phrase) for phrase in phrases]

        # vectorize
        if self._vectorizer is not None:
            data = self._vectorizer.transform(data)

        # tokenize
        if self._tokenizer is not None:
            sequences = self._tokenizer.texts_to_sequences(data)
            data = pad_sequences(sequences, maxlen=self._max_len)

        # predict
        try:
            pred = self._model.predict(data)
        except:
            data = pd.DataFrame(
                data.toarray(),
                columns = self._model.feature_names_in_
            )
            pred = self._model.predict(data)

        if isinstance(pred[0], tuple):
            return [x for x in pred]
        else:
            return [self.sentiment(x, y) for x,y in pred]

        # return [ {"sentiment": x, "phrase": y} for x,y in zip(pred, phrases)]

    # 0 -- 0.39 | 0.4 -- 0.6 | 0.61 -- 1
    # negatif   | neutre     | positif
    def sentiment(x, y):
        if np.abs(x-y) <= .2:
            return 'Neutral'
        elif x>y:
            return 'Negative'
        else:
            return 'Positive'

    def serve(self, port=8000):
        if self._ui is None:
            raise Exception("UI is not defined")

        self._ui.serve(port)
