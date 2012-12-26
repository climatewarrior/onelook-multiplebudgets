#!/usr/bin/python

from flask import Flask, render_template, request, flash, redirect, url_for
from flask.ext.pymongo import PyMongo
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form, TextField, HiddenField, ValidationError,\
                          Required, RecaptchaField

from bson.objectid import ObjectId
import json_app

app = json_app.make_json_app('__main__')
mongo = PyMongo(app)
Bootstrap(app)

app.config['SECRET_KEY'] = 'devkey'
app.config['RECAPTCHA_PUBLIC_KEY'] = '6Lfol9cSAAAAADAkodaYl9wvQCwBMr3qGR_PPHcw'

class LookForm(Form):
    title = TextField('Look Name', description='This is field one.')
    description = TextField('Description', description='This is field two.',
                       validators=[Required()])
    hidden_field = HiddenField('You cannot see this', description='Nope')
    #recaptcha = RecaptchaField('A sample recaptcha field')

    def validate_hidden_field(form, field):
        pass

def add_look(form):

    item1 = {"name":"Clark's Dessert Boots",
             "price":110.00,
             "type":"boot",
             "screenshot":"blah.jpg",
             "link":"http://google.com/"}

    item0 = {"name":"Levi's 511",
             "price":37.00,
             "type":"denim",
             "screenshot":"blah.jpg",
             "link":"http://google.com/"}

    items = [item0, item1]

    look = {"title": form.title.data,
            "text": form.description.data,
            "tags": ["casual", "hawt", "reddit"],
            "screenshot": str(url_for('static', filename='looks_imgs/4e4ng.jpg')),
            "items": items}

    return mongo.db.looks.insert(look)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_new_look/', methods=('GET', 'POST'))
def submit_new_look():
    form = LookForm()
    if request.method == "POST":
        look_id = str(add_look(form))
        flash("Sucess " + look_id)
        return redirect(url_for("index"))

    return render_template('submit_new_look.html', form=form)

@app.route('/looks/<look_id>/<lookname>')
def get_look(look_id, lookname):
    look = mongo.db.looks.find_one({"_id": ObjectId(look_id)})
    return render_template('look.html', look=look)

if __name__ == '__main__':
    app.run(debug=True)
