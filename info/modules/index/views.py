import logging
from flask import current_app
from flask import session

from info import redis_store
from . import  index_blu

@index_blu.route('/')
def index():
    redis_store.set('password','123456789')
    logging.debug('这是一个测试')
    session['email']='215468657'
    current_app.logger.debug('这个是测试代码')
    return 'index'