#!/usr/bin/python
# -*- coding: utf-8 -*-
# DATE: 2023/02/22
# Author: Irfan TOOR
# file : backend/filesystem.py

from abc import ABC
import os
import re
import pickle

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
        path = os.path.join(self._root, self._normalize(model_name))
        if not os.path.exists(path):
            raise Exception(f'Model: {model_name}, not found')

        return pickle.load(open(path, "rb"))

    def save(self, model_name:str, model):
        """ Saves the model to a given pickle file
        """
        path = os.path.join(self._root, self._normalize(model_name))
        if os.path.exists(path):
            raise Exception(f'Model: {model_name}, already exists')

        pickle.dump(model, path)