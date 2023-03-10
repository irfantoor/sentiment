# API for analysing the sentiments of a tweet

A small framework to manage processing of models for the sentiment analysis.

It consists of the following components:

- With the operational backends:
    - Filesystem
    - MLFlow
    - AWS (in progress)
    - Azure (in progress)

- UI Connectivity :
    - Flask
    - FastAPI
- Pipeline
- Transformer (in progress)
- Unit-Testing (in progress)
- CI (connectivity with heroku is prevu, in progress)

Here is an example of using the sentiment framework :

```py
# file : model_api.py

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
```

```sh
(.venv) % python model_api.py
```
