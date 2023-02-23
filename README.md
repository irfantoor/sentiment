# API pour analyser les sentiment d'un tweet

- Basé sur flask ou FastAPI
- Recevoi un tweet et retourne les sentiment
- Des copies écran des commits, du dossier Github (+ lien vers ce dossier)
- Tests unitaires
- Pipeline de déploiment continue


Here is an example of using the sentiment module :

```py
# file : api_run.py

from sentiment import Model
from sentiment.backend import FileSystem
from sentiment.ui import FastApi, Flask
from pydantic import BaseModel

# create the model
model = Model()

# create the backend
fs = FileSystem('data/cleaned')
model.backend(fs)

# list all models
# print(fs.ls('/', '.*\.pkl|.*\.b'))

# load a model
model.load('model_gaussian_nb.b')

# create the ui/FastApi
api = FastApi()
# api = Flask()
model.ui(api)

# data expected through post
class Data(BaseModel):
    phrase: str

# API app
app = api.app()

# API Routes

# get /
@app.get("/")
def read_root():
    return {"message": "The API is working!"}

# post in flask
@app.route('/flask/predict/', methods=['POST'])
def flask_predict():
    request = api.request()
    data = request.get_json(force=True)
    return predict(data['phrase'])

# post in fastapi
@app.post("/fastapi/predict/")
def fastapi_predict(data: Data):
    return predict(data.phrase)

def predict(phrase):
    prediction = model.predict([phrase])

    # adjust it for response
    prediction = [int(x) for x in prediction]
    if len(prediction)==1:
        prediction = prediction[0]

    # return through response
    return {'prediction': prediction}

# serve
model.serve(port=8001)
```

```sh
(.venv) % python api_run.py
```
