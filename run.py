#!/usr/bin/python3
# -*- coding: utf-8 -*-

from app import app
app.run(host="localhost", 
	port=5000, 
	debug=True)