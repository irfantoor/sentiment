#!/usr/bin/python
# -*- coding: utf-8 -*-
# DATE: 2023/02/22
# Author: Irfan TOOR
# file : ui/flask.py

from abc import ABC

import uvicorn
from flask import Flask as RealFlask, request

class Flask(ABC):
    _app = None

    def __init__(self) -> None:
        pass
        self._app = RealFlask(__name__)

    def app(self):
        return self._app

    def request(self):
        return request

    def serve(self, port=8000):
        RealFlask.run(self._app, host='127.0.0.1', port=port)
        #uvicorn.run(self._app, host='127.0.0.1', port=port)
