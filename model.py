#!/usr/bin/python
# -*- coding: utf-8 -*-
# DATE: 2023/02/08
# Author: Irfan TOOR
# file : model.py

from abc import ABC
import sentiment.backend as Model_Backend
import sentiment.ui as Model_UI
import sentiment.transformer as Model_Transformer
from sentiment.pipeline import Pipeline
from sentiment.text import pad_sequences
import numpy as np

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
    _pipeline = None
    _model = None
    _vectorizer = None
    _tokenizer = None

    # tokenizer
    _max_len = 128
    _num_words = 20000

    # internal
    _prepared = False

    def __init__(self, backend=None, ui=None, transformer=None, pipeline=None):
        if backend is not None:
            self.backend(backend)

        if ui is not None:
            self.ui(ui)

        if transformer is not None:
            self.transformer(transformer)

        if pipeline is not None:
            self.pipeline(pipeline)

    def backend(self, backend:Model_Backend):
        self._backend = backend

    def ui(self, ui:Model_UI):
        self._ui = ui

    def transformer(self, transformer):
        self._transformer = transformer

    def pipeline(self, pipeline:Pipeline):
        self._pipeline = pipeline

    def prepare(self):
        if self._prepared:
            return

        if not self._prepared:
            self._prepared = True
            if self._pipeline is None:
                self._pipeline = Pipeline()
                self._pipeline.build()

    # tood -- all of the seting parts to be done later
    # todo -- num_words, max_len could be loaded through tokenizer

    # def int_tokenizer(self, phrases, num_words:int=20000, max_len:int=128):
    #     from sentiment.text import Tokenizer
    #     self._max_len = max_len
    #     self._num_words = num_words
    #     self._tokenizer = Tokenizer(num_words=num_words)
    #     self._tokenizer.fit_on_texts(phrases)

    def _load(self, name:str):
        if self._backend is None:
            raise Exception("Backend is not defined")

        return self._backend.load(name)

    def load(self, name:str):
        self._model = self._load(name)

    def vectorizer(self, name:str):
        self._vectorizer = self._load(name)

    def tokenizer(self, name:str):
        # todo -- must reload the num_words and max_len etc.
        self._tokenizer = self._load(name)

    def save(self, name:str):
        if self._backend is None:
            raise Exception("Backend is not defined")

        self._backend.save(name)

    def get_backend(self):
        return self._backend

    def get_ui(self):
        return self._ui

    def get_transformer(self):
        return self._transformer

    def get_pipeline(self):
        return self._pipeline

    def get_raw(self):
        return self._model

    def get_vectorizer(self):
        return self._vectorizer

    def get_tokenizer(self):
        return self._tokenizer

    def predict(self, phrases):
        if self._model is None:
            raise Exception("No model has been loaded")

        if not self._prepared:
            self.prepare()

        # pipeline
        data = self._pipeline.process(phrases)

        # vectorize
        if self._vectorizer is not None:
            data = self._vectorizer.transform(data)

        # tokenize
        if self._tokenizer is not None:
            sequences = self._tokenizer.texts_to_sequences(data)
            data = pad_sequences(sequences, maxlen=self._max_len)

        # predict
        # try:
        pred = self._model.predict(data)

        # todo -- adjust for the models requiring DataFrame etc.
        #         ex : Models using vectorizers
        # except:
        #     data = pd.DataFrame(
        #         list(data),
        #         columns = self._model.feature_names_in_
        #     )
        #     pred = self._model.predict(data)

        if isinstance(pred[0], tuple):
            return [x for x in pred]
        else:
            return [self.sentiment(x, y) for x,y in pred]

        # return [ {"sentiment": x, "phrase": y} for x,y in zip(pred, phrases)]

    # 0 -- 0.39 | 0.4 -- 0.6 | 0.61 -- 1
    # negatif   | neutre     | positif
    def sentiment(self, x, y):
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
