from flask import Flask
from flask import session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import  Migrate,MigrateCommand
# 指定ｓｅｓｓｉｎ存储的位置
from flask_session import Session
from redis import  StrictRedis
from flask_script import Manager


app = Flask(__name__)

class Config(object):
    DEBUG= True
    # 数据库配置
    SQLALCHEMY_DATABASE_URI ='mysql://root:mysql@127.0.0.1:3306/information02'
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SECRET_KEY ='03pNX+bIhPuo9qS18caOuafDOMnUwSgjCM3ALjaB+yf4jIjuODiE8+kw7GsVcNce'
    # 配置redis
    redis_host='127.0.0.1'
    redis_port=6379
    # 设置ｓｅｓｓｉｏｎ
    SESSION_TYPE='redis'
    SESSION_USE_SINGER=True
    SESSION_REDIS=StrictRedis(host=redis_host,port=redis_port)
    # 设置过期是否需要过期，
    SESSION_PERMANENT=False
    # 设置过期时间,86400是一天，设置的过期时间是两天
    PERMANENT_SESSION_LIFETIME=86400*2
app.config.from_object(Config)
db = SQLAlchemy(app)
redis_store=StrictRedis(host=Config.redis_host,port=Config.redis_port)
Session(app)
manager = Manager(app)
Migrate(app,db)
manager.add_command('db',MigrateCommand)


@app.route('/')
def index():
    session['name']='yan'
    return 'index'


if __name__ == '__main__':
    manager.run()
