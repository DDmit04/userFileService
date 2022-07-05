import os

from flask import Flask

import AppFactory

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(ROOT_DIR, 'userFiles')
DATABASE_URL = 'postgresql://postgres:ps@localhost:5432/file_database'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PATH_SEPARATOR'] = '/'
app = AppFactory.setup_app(app)

if __name__ == '__main__':
    app.run()
