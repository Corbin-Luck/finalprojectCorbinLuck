import os

import requests
import time

## Web App Functions ##

from flask import Flask, render_template

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

    # a simple page that says hello
    @app.route('/')
    def home_Page():
        return render_template('base.html')

    from . import home
    app.register_blueprint(home.bp)

    return app

## API Functions ##

api_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"
api_KEY = ""

def get_Lookup(cve_id=None):
    headers = {"apiKEY": api_KEY} if api_KEY else {}
    params = {"cveId" : cve_id}
    response = requests.get(api_URL, params=params, headers=headers)
    return response.json()