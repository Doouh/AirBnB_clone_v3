#!/usr/bin/python3
"""
Create a basics routes and register the blueprint
"""
from models import storage
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify, make_response
from flask_cors import CORS
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)
a = CORS(app, resources={'/*': {'origins': '0.0.0.0'}})


@app.teardown_appcontext
def close(self):
    """ Function that close the session """
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """ Function that return an error when its not found """
    return make_response(jsonify({'error': "Not found"}), 404)


if __name__ == "__main__":
    app.run(host=getenv('HBNB_API_HOST'), port=getenv('HBNB_API_PORT'),
            threaded=True)
