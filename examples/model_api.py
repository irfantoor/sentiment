#!/usr/bin/python
# -*- coding: utf-8 -*-
# DATE: 2023/02/08
# Author: Irfan TOOR <email@irfantoor.com>
# file : examples/model_api.py

# Note : It is an example file
#        Copy this file to your virtualenv root folder

"""
# --------------------------------------------------------
# copy to virtualenv root folder:
% cp sentiment/examples/model_api.py .

# --------------------------------------------------------
# lanch the api:

% pipenv run python model_api.py

or

% pipenv shell
(venv ...) % python model_api.py

# --------------------------------------------------------
# through console:
curl -X POST localhost:8001/predict/ \
-H 'Content-Type: application/json' \
-d '{"phrases": ["I love the world", ",but I am tired"]}'

# --------------------------------------------------------
# progamatically:
import requests
import json

phrases = [
    "I love this world",
    "Destiny of human is doomed!"
]

for phrase in phrases:
    response = requests.post(
        'http://localhost:8001/predict/',
        data=json.dumps({'phrase': phrase})
        )
    pred = json.loads(response.text)
    print(pred)
"""

from sentiment import Model
from sentiment.backend import FileSystem
from sentiment.ui import Flask, FastApi
from sentiment.pipeline import Pipeline

# init model
model = Model(
    backend=FileSystem('data/cleaned/'),
    ui=Flask(),
    pipeline=Pipeline(add_to_stopwords=['--'], use_nlp=True)
)

# load a model / tokenizer
model.load('model_avance.h5')
model.tokenizer('model_avance.h5.tk.pkl')

# Flask API structure
ui = model.get_ui()
app = ui.app()

@app.route('/')
def home():
    return {"message": "The API is working!"}

@app.route('/predict/', methods=['POST'])
def flask_predict():
    data = ui.request().get_json(force=True)
    phrases = None
    if 'phrase' in data:
        phrases = data['phrase']
    elif 'phrases' in data:
        phrases = data['phrases']
    else:
        return {"error", "phrase or phrases must be provided"}

    if isinstance(phrases, str):
        phrases = [phrases]

    return model.predict(phrases)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    msg = f'no route defined for: %s' % path
    return {"error": msg}, 404

# serve the model
model.serve(port=8001)
