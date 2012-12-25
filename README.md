#Installation

* `git clone` the repository
* Make sure you're using python 2.7: 
	* `python --version` 
* Go into `onelook-multiplebudgets/`
* Install the dependencies:
	* `[sudo] easy_install pip`
	* `[sudo] pip install Flask`
	* `[sudo] pip install Flask-PyMongo`
	* `[sudo] pip install flask-bootstrap`
* Install MongoDB
	* OSX: `brew install mongodb`
* Run MongoDB: `mongod`
* Populate the DB: `python populatedb.py`
	* Default Host: `localhost`
	* Default Post: `27017`
	* Default DB: `main`
	* New Collection: `looks`
* Run the App: `python main.py`
* Open: `http://127.0.0.1:5000/`

# Open Source

* [MongoDB](http://www.mongodb.org/)
* [Flask](http://flask.pocoo.org/)
* [Flask-PyMongo](https://flask-pymongo.readthedocs.org/en/latest/)
* [Flask-Bootstrap](https://github.com/mbr/flask-bootstrap)