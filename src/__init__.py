from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

from flask_uploads import IMAGES, UploadSet , configure_uploads 

import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = '82821'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['UPLOADED_PHOTOS_DEST']= os.path.join(basedir, 'static/images')
photos = UploadSet("photos", IMAGES)
configure_uploads(app, photos)


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from src.admin import routes
from src.products import routes
