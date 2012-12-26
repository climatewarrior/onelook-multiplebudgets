#!/usr/bin/python

from pymongo import MongoClient
import datetime

connection = MongoClient()
db = connection.main
looks = db.looks

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

look = {"title": "Mike",
        "text": "My first look!",
        "tags": ["casual", "hawt", "reddit"],
        "screenshot": "4e4ng.jpg",
        "items": items}

looks.insert(look)
