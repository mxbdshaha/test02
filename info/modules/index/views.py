# import logging
from flask import current_app
# from flask import session
#
# from info import redis_store
from flask import render_template

from . import  index_blu

@index_blu.route('/')
def index():
    return render_template('news/index.html')

@index_blu.route('/favicon.ico')
def favicon():
    return current_app.send_static_file('news/facicon.ico')