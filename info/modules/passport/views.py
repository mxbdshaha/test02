import random

from flask import abort, jsonify
from flask import current_app
from flask import json
from flask import make_response
from flask import request

from info import constants
from info import redis_store
from info.utils.response_code import RET
from libs.yuntongxun.sms import CCP
from . import  passport_blu
from info.utils.captcha.captcha import captcha
import libs

@passport_blu.route('/imageCode')
def send_image():
    """
    1，取出其参数，
    2，判断是否有值
    3，生成图片
    4，把生成的唯一的值作为键，生成图片的内容作为键存入redis 中，
    5，把图片作为响应传给前端
    :return:
    """
    imageCode=request.args.get('imagecode')
    print(imageCode)
    if not imageCode:
        abort(404)
    # 生成图片
    name,text,image=captcha.generate_captcha()
    try:
        redis_store.setex('imageCodeId_'+imageCode,constants.IMAGE_CODE_REDIS_EXPIRES,text)
    except Exception as e:
        return jsonify(errno=RET.PARAMERR,errmes='参数错误')
    # 把值传给前端界面
    response=make_response(image)
    response.headers['ContentType']='image/jpg'
    return  response


@passport_blu.route('/sendcode',methods=['POST','GET'])
def send_code():
    """
    1,接受前端ajax传入的参数,前端是post 请求，一定要注意，把传入进来的数据转换成字典，三个参数分别
    为mobile , imagecode ,imageCodeId
    2,判断值是否为空，
    3,取出存储在redis 里面的真是的图片内容,判断是否取的出来
    4进行比对，
    5，生成发送的验证码
    6，把验证码存入ｒｅｄｉｓ中，过期时间
    7，把手机号，生成的验证码，发送给第三方平台，
    8，发送成功就返回状态码
    :return:
    """
    params=request.json
    print(params)
    mobile = params.get('mobile')
    image_code =params.get('imagecode')
    image_code_id = params.get("imagecodeid")

    if not all([mobile,image_code,image_code_id]):
        return jsonify(errno=RET.PARAMERR,errmes='参数错误')
    try:
        real_image_code=redis_store.get('imageCodeId_'+image_code_id)
    except Exception as e:
        return jsonify(errno=RET.DBERR , errmes='数据库查询失败')
    if not real_image_code:
        return jsonify(errno=RET.DBERR , errmes='数据已过期')
    print(real_image_code)
    print(image_code)
    if real_image_code.upper() != image_code.upper():
        current_app.logger.debug("111")
        return jsonify(errno=RET.PARAMERR , errmes='验证码不正确')
    mes_num = '%06d' % random.randint(0,999999)
    try:
        redis_store.setex('imagecode_'+mobile,constants.IMAGE_CODE_REDIS_EXPIRES,mes_num)
    except Exception as e:
        current_app.logger.debug("222")

        return jsonify(errno=RET.PARAMERR, errmes='数据保存不成功')

    result=CCP().send_template_sms(mobile, [mes_num, constants.SMS_CODE_REDIS_EXPIRES], '1')
    if result != 0:
        # 代表发送不成功
        current_app.logger.debug("333")
        return jsonify(errno=RET.THIRDERR, errmsg="发送短信失败")

    return jsonify(errno=RET.OK, errmsg="发送成功")







