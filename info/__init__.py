from flask import Flask
from flask.ext.session import Session
from flask.ext.sqlalchemy import SQLAlchemy
from redis import StrictRedis
from config import Config_dict


# 初始化app
db=SQLAlchemy()


def Config_app(config_name):
    app = Flask(__name__)
    app.config.from_object(Config_dict[config_name])
    # 数据库实例化对象
    db.init_app(app)
    redis_store=StrictRedis(host=Config_dict[config_name].redis_host,port=Config_dict[config_name].redis_port)
    Session(app)
    # 什么时候调用，时候导入
    from .modules.index import index_blu
    # 将蓝图注册到app里面
    app.register_blueprint(index_blu)

    return app