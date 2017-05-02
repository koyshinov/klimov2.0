# -*- coding: utf-8 -*-

from flask import Flask
from app import localconfig as lconf


app = Flask(__name__)
app.config["SECRET_KEY"] = lconf.app_secret_key

from app import views