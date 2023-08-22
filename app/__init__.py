from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] ='SECRET_KEY'
app.config['SQLALCHEMY_DATABASE_URI'] =  'sqlite:///db.sqlite3'

db = SQLAlchemy(app)

from . import models, views

db.create_all()
