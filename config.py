import logging
from redis import StrictRedis


class Config(object):
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
    # 打印日志等级
    LOG_LEVEL= logging.debug

#    开发环境下的debug
class Development(Config):
    DEBUG=True

class  Production(Config):
    DEBUG = False
    LOG_LEVEL = logging.warning

class Testing(Config):
    DEBUG =True
    TESTING=True


Config_dict={
    'development':Development,
    'production':Production,
    'testing':Testing
}