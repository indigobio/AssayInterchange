from flask import Flask
from flask_cors import CORS

app = Flask(__name__, static_url_path='')
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


from .routes import *