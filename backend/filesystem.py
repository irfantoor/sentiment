#!/usr/bin/python
# -*- coding: utf-8 -*-
# DATE: 2023/02/22
# Author: Irfan TOOR
# file : backend/filesystem.py

from abc import ABC
import os
import re
import pickle
from keras.models import load_model

class FileSystem(ABC):
    _root = ''

    def __init__(self, root:os.path=None) -> None:
        if root is not None:
            self.set_root(root)

    def set_root(self, root):
        if not os.path.exists(root):
            raise Exception(f'path : {root}, does not exist')

        self._root = root

    def _normalize(self, path):
        return path.lstrip('/').rstrip('/')

    def ls(self, path='', re_filter=None):
        ls = os.listdir(os.path.join(self._root, self._normalize(path)))
        if re_filter is None:
            return ls

        ll = []
        patern = re.compile(re_filter)
        for item in ls:
            if patern.match(item):
                ll.append(item)

        return ll

    def load(self, model_name:str):
        """ Loads the model from a given pickle file
        """
        model = None
        tokenizer = None
        vectorizer = None

        path = os.path.join(self._root, self._normalize(model_name))
        if not os.path.exists(path):
            raise Exception(f'Model: {model_name}, not found')

        if (model_name.endswith('.b') or model_name.endswith('.pkl')):
            return pickle.load(open(path, "rb"))
        elif (model_name.endswith('.h5')):
            return load_model(path)
        elif (model_name.endswith('.tf')):
            raise Exception('not implemented')
        else:
            raise Exception('extension can only be : .pkl, .b, .h5 or .tf')

    def save(self, model_name:str, model):
        """ Saves the model to a given pickle file
        """
        path = os.path.join(self._root, self._normalize(model_name))
        if os.path.exists(path):
            raise Exception(f'Model: {model_name}, already exists')

        if (model_name.endswith('.h5') or model_name.endswith('.tf')):
            model.save(path)
        elif (model_name.endswith('.tf')):
            model.save(path)
        else:
            pickle.dump(model, path)
