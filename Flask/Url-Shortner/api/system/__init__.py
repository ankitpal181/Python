#!/usr/bin/env python3

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///url_shortner.db"
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:Ankitpal*1828542146@localhost:3306/url_shortner"
db = SQLAlchemy(app)
# bcrypt = Bcrypt(app)
