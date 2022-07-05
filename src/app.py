import os

from flask import Flask

import AppFactory
from dotenv import load_dotenv
load_dotenv()

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(ROOT_DIR, 'userFiles')
DATABASE_URL = os.getenv("DB_URL")

app = Flask(__name__)
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PATH_SEPARATOR'] = '/'
app = AppFactory.setup_app(app)

if __name__ == '__main__':
    app.run()
