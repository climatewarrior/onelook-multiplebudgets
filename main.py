#!/usr/bin/python
from flask import Flask, jsonify, render_template, request
import json_app

app = json_app.make_json_app('__main__')

@app.route('/')
def index():
    return "Hello World!"

if __name__ == '__main__':
    app.run(debug=True)
