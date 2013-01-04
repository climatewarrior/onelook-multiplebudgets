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
from flask.ext.wtf import (Form, TextField, HiddenField, BooleanField,
     PasswordField, SubmitField, ValidationError, Required, RecaptchaField, validators)
from flask.ext.uploads import (UploadSet, configure_uploads, IMAGES)
from flask.ext.login import (LoginManager, login_user, logout_user,
                             login_required, UserMixin, current_user)

from bson.objectid import ObjectId
import json_app

app = json_app.make_json_app('__main__')

login_manager = LoginManager()
login_manager.setup_app(app)
Bootstrap(app)

mongo = PyMongo(app)

# defaults

app.config['SECRET_KEY'] = 'devkey'
app.config['RECAPTCHA_PUBLIC_KEY'] = '6Lfol9cSAAAAADAkodaYl9wvQCwBMr3qGR_PPHcw'
app.config['UPLOADED_PHOTOS_DEST'] = 'static/looks_imgs/'

# uploads

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

class User(UserMixin):
    def __init__(self, user_dict):
        print user_dict
        self.id = str(user_dict['_id'])
        self.username = user_dict['username']
        self.email = user_dict['email']
        self.current_upload = user_dict['current_upload']

class RegistrationForm(Form):
    email = TextField('Email Address', [validators.Length(min=6, max=35)])
    username = TextField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password')
    accept_rules = BooleanField('I accept the site rules', validators=[Required()])

class LoginForm(Form):
    username = TextField('Username')
    password = PasswordField('Password')
    remember_me = BooleanField('Remember me')

class LookForm(Form):
    title = TextField('Look Name', description='This is field one.')
    description = TextField('Description', description='This is field two.',
                       validators=[Required()])

    hidden_field = HiddenField('You cannot see this', description='Nope')
    #recaptcha = RecaptchaField('A sample recaptcha field')

    def validate_hidden_field(form, field):
        pass

@login_manager.user_loader
def load_user(user_id):
    return User(mongo.db.users.find_one({"_id": ObjectId(user_id)}))

def add_look(form):

    filename = current_user.current_upload

    look = {"title": form.title.data,
            "text": form.description.data,
            "user": "",
            "tags": ["casual", "hawt", "reddit"],
            "screenshot": str(url_for('static', filename='looks_imgs/' + filename)),
            "items": []}

    return mongo.db.looks.insert(look)

@app.route('/')
def index():
    looks = mongo.db.looks.find().limit(10)

    return render_template('index.html', looks = looks)

@app.route('/register/', methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    if request.method == 'POST' and form.validate():
        user = {'username': form.username.data,
                'email': form.email.data,
                'password': form.password.data,
                'current_upload': ''}

        mongo.db.users.insert(user)

        redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST" and form.validate():
        user = mongo.db.users.find_one({"username": form.username.data})
        if user != None:
            if login_user(User(user), remember=form.remember_me.data):
                flash("Logged in!")
                return redirect(url_for("index"))
            else:
                flash("Sorry, but you could not log in.")
        else:
            flash(u"Invalid username.")
    return render_template("login.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out.")
    return redirect(url_for("index"))

@app.route('/submit_new_look/', methods=['GET', 'POST'])
def submit_new_look():
    form = LookForm()
    if request.method == "POST":
        print "Current upload"
        look_id = str(add_look(form))
        flash("Sucess " + look_id)
        return redirect(url_for("index"))

    return render_template('submit_new_look.html', form=form)

@app.route('/add_item/<look_id>', methods=['POST'])
def add_item(look_id):
    if request.method == "POST":
        print "Adding item"
        look = mongo.db.looks.find_one({'_id': ObjectId(look_id)})
        items = look['items']

        new_item = {"name":"Clark's Dessert Boots",
        "price":110.00,
        "type":"boot",
        "screenshot":"blah.jpg",
        "link":"http://google.com/"}

        item_id = mongo.db.items.insert(new_item)

        items.append(item_id)
        mongo.db.looks.update({'_id': ObjectId(look_id)},
                              {'$set' : {'items': items}})
        flash("Sucess ")
        return 'OK'
    return 'OK'

@app.route('/upload', methods=['POST'])
def upload():
    # for property, value in vars(request).iteritems():
    #     print property, ": ", value
    if request.method == 'POST' and 'file' in request.files:
        filename = photos.save(request.files['file'])
        mongo.db.users.update({'_id': ObjectId(current_user.id)},
                              {'$set' : {'current_upload': filename}})
        flash("Photo saved.")
        return "OK"
    return "OK"

@app.route('/looks/<look_id>/<lookname>')
def get_look(look_id, lookname):
    look = mongo.db.looks.find_one({'_id': ObjectId(look_id)})
    item_ids = look['items']
    items = [mongo.db.items.find_one({'_id': i}) for i in item_ids]
    return render_template('look.html', look=look, items=items)

if __name__ == '__main__':
    app.run(debug=True)
