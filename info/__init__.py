import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask.ext.session import Session
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.wtf import CSRFProtect
from redis import StrictRedis
from config import Config_dict


# 初始化app
db=SQLAlchemy()
redis_store=None #type:StrictRedis

def Setup(config_name):
    # 设置日志的记录等级
    logging.basicConfig(level=Config_dict[config_name].LOG_LEVEL)  # 调试debug级
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024 * 1024 * 100, backupCount=10)
    # 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)


def Config_app(config_name):
    Setup(config_name)
    app = Flask(__name__)
    app.config.from_object(Config_dict[config_name])
    # 数据库实例化对象
    db.init_app(app)
    # 申明redis_store这个变量是全局变量，我们在视图函数里面就可以调用他
    global redis_store
    redis_store=StrictRedis(host=Config_dict[config_name].redis_host,port=Config_dict[config_name].redis_port,decode_responses=True)
    Session(app)
    # 设置CSRFProtect保护
    # CSRFProtect(app)
    # 什么时候调用，时候导入
    from .modules.index import index_blu
    # 将蓝图注册到app里面
    app.register_blueprint(index_blu)
    # 什么时候调用，时候导入
    from .modules.passport import passport_blu
    # 将蓝图注册到app里面
    app.register_blueprint(passport_blu)

    return app