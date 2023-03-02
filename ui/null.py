#!/usr/bin/python
# -*- coding: utf-8 -*-
# DATE: 2023/02/22
# Author: Irfan TOOR
# file : ui/flask.py

from abc import ABC

class Null(ABC):
    _app = None

    def __init__(self) -> None:
        pass
        self._app = {}

    def app(self):
        return None

    def request(self):
        return None

    def serve(self, port=8000):
        import uvicorn
        uvicorn.run(self._app, host='127.0.0.1', port=port)
