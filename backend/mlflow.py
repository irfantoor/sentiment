#!/usr/bin/python
# -*- coding: utf-8 -*-
# DATE: 2023/02/22
# Author: Irfan TOOR
# file : backend/mlflow.py

from abc import ABC
import os
import pickle
import mlflow
import requests

class MLFlow(ABC):

    _tracking_uri = ''
    _client = None

    def __init__(self, tracking_uri) -> None:
        if (
            tracking_uri.startswith('http://')
            or tracking_uri.startswith('https://')
            ):
            try:
                response = requests.head(tracking_uri)
            except:
                error = f'Error connecting Tracking server at {tracking_uri}'
                print(error)
                print('vous pouvez executer un serveur local:')
                print('% mlflow server -p 8000')
                raise Exception(error)

        self._tracking_uri = tracking_uri
        self._client = mlflow.MlflowClient(tracking_uri=self._tracking_uri)

    def client(self):
        return self._client

    def load(self, run_id:str):
        """ Loads the model from mlflow
        """
        if self._client is None:
            raise Exception('mlflow not initialized, use connect_mlflow')

        run = self._client.get_run(run_id)
        a_uri = run.info.artifact_uri
        path = a_uri.replace('mlflow-artifacts:', 'mlartifacts')
        # file = os.path.join(file, 'model/model.pkl')
        path = os.path.join(path, 'best_estimator/model.pkl')

        if not os.path.exists(path):
            raise Exception(f'Model: {run_id}, not found')

        return pickle.load(open(path, "rb"))

    def update(self, run_id:str, model):
        """ Updates the model to mlflow
        """
        raise Exception('Not implemented')