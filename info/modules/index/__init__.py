# 蓝图导入
from flask import  Blueprint

index_blu =Blueprint('index',__name__)


from .views import *