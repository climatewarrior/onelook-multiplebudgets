#!/usr/bin/python

from flask import Flask, jsonify, render_template, request
from flask.ext.pymongo import PyMongo
from flask.ext.bootstrap import Bootstrap

import json_app

app = json_app.make_json_app('__main__')
mongo = PyMongo(app)
Bootstrap(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/looks/<int:look_id>/<lookname>')
def get_item(look_id, lookname):
    look = mongo.db.looks.find_one()
    return render_template('look.html', look=look)

if __name__ == '__main__':
    app.run(debug=True)
