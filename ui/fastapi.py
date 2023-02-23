#!/usr/bin/python
# -*- coding: utf-8 -*-
# DATE: 2023/02/22
# Author: Irfan TOOR
# file : ui/fastapi.py

from abc import ABC

import uvicorn
from fastapi import FastAPI

class FastApi(ABC):
    _app = None

    def __init__(self) -> None:
        self._app = FastAPI()

    def app(self):
        return self._app

    def serve(self, port=8000):
        uvicorn.run(self._app, host='127.0.0.1', port=port)
