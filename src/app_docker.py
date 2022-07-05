import os

from flask import Flask

import AppFactory

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(ROOT_DIR, os.environ['UPLOAD_DIR_NAME'])
DATABASE_URL = os.environ['DB_URL']
SEPARATOR = os.environ['SEPARATOR']


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PATH_SEPARATOR'] = SEPARATOR
app = AppFactory.setup_app(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0')