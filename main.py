#!/usr/bin/python
from flask import Flask, jsonify, render_template, request
from flask.ext.pymongo import PyMongo
import json_app

app = json_app.make_json_app('__main__')
mongo = PyMongo(app)

@app.route('/')
def index():
    return "Hello World!"

if __name__ == '__main__':
    app.run(debug=True)
