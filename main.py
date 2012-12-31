#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2012 Gabriel J. Pérez Irizarry and Andrea Del Risco
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License, version 3,
# as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from flask import Flask, render_template, request, flash, redirect, url_for
from flask.ext.pymongo import PyMongo

from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form, TextField, HiddenField, FileField, \
     ValidationError, Required, RecaptchaField, validators
from flask.ext.uploads import UploadSet, configure_uploads, IMAGES

from bson.objectid import ObjectId
import json_app

app = json_app.make_json_app('__main__')
mongo = PyMongo(app)
Bootstrap(app)

# defaults

app.config['SECRET_KEY'] = 'devkey'
app.config['RECAPTCHA_PUBLIC_KEY'] = '6Lfol9cSAAAAADAkodaYl9wvQCwBMr3qGR_PPHcw'
app.config['UPLOADED_PHOTOS_DEST'] = '/tmp/photolog'

# uploads

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

class LookForm(Form):
    title = TextField('Look Name', description='This is field one.')
    description = TextField('Description', description='This is field two.',
                       validators=[Required()])
    image  = FileField(u'Image File', [validators.regexp(u'.*.jpg')])

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
    looks = mongo.db.looks.find().limit(10)

    return render_template('index.html', looks = looks)

@app.route('/submit_new_look/', methods=('GET', 'POST'))
def submit_new_look():
    form = LookForm()
    if request.method == "POST":
        look_id = str(add_look(form))
        flash("Sucess " + look_id)
        return redirect(url_for("index"))

    return render_template('submit_new_look.html', form=form)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    # for property, value in vars(request).iteritems():
    #     print property, ": ", value
    if request.method == 'POST' and 'file' in request.files:
        filename = photos.save(request.files['file'])
        flash("Photo saved.")
        return redirect(url_for("index"))
    return "Uploaded"

@app.route('/looks/<look_id>/<lookname>')
def get_look(look_id, lookname):
    look = mongo.db.looks.find_one({"_id": ObjectId(look_id)})
    return render_template('look.html', look=look)

if __name__ == '__main__':
    app.run(debug=True)
