#-*- coding:utf-8 -*-
from flask import Flask, request, abort, render_template
import hashlib 
import xmltodict
import time
import urllib2
import json

RINGO_TOKEN = "ringo" # 微信接口Token

APP_ID = "wx35a1eca48eb0e695"
APP_SECRET = "f3659c174be984d4224f217a46954cbc"


app = Flask(__name__)

# 开发者通过检验signature对请求进行校验。
# 若确认此次GET请求来自微信服务器，请原样返回echostr参数内容，则接入生效，成为开发者成功，否则接入失败。

# 校验流程：
# 将token、timestamp、nonce三个参数进行字典序排序
# 将三个参数字符串拼接成一个字符串进行sha1加密
# 开发者获得加密后的字符串可与signature对比，标识该请求来源于微信


@app.route('/ringochat', methods=["GET", "POST"]) # 根据微信借口url设置路由地址
def ringochat():
    data = request.args # 微信的查询字符串
    signature = data.get("signature")
    nonce  = data.get("nonce")
    timestamp = data.get("timestamp")

    if not all([signature, timestamp, nonce]):
        abort(400)

    # 生成echostr
    li = [RINGO_TOKEN, timestamp, nonce]
    li.sort() # 对参数排序
    data_str = "".join(li) # 拼接字符串
    hash_obj = hashlib.sha1(data_str) # 生成加密对象
    hash_str = hash_obj.hexdigest() # 转化为加密字符串

    if signature != hash_str: # 检验signature对请求进行校验
        abort(403)
    else:
        if request.method == "GET": #若请求方式为GET即为请求验证
            echostr = request.args.get("echostr") # 只有在验证时才会传入echostr
            return echostr # 原样返回echostr参数内容
        elif request.method == "POST":
            if request.data:
                xml_str = request.data
                xml_dict = xmltodict.parse(xml_str) # 将xml字符串转换为字典类型
                xml_dict = xml_dict.get("xml") # 继续提取xml键中的内容

                if xml_dict.get("MsgType") == "text": # 如果发送的内容为文本格式
                    # 构造回复的xml
                    return_dict = {
                        "xml":{
                            "ToUserName": xml_dict.get("FromUserName"),
                            "FromUserName": xml_dict.get("ToUserName"),
                            "CreateTime": int(time.time()),
                            "MsgType": "text",
                            "Content": xml_dict.get("Content"),
                        }  
                    }
                    return_xml_str = xmltodict.unparse(return_dict)
                    return return_xml_str # 返回回复的xml字符串
                else: # 如果是其他格式
                    return_dict = {
                        "xml":{
                            "ToUserName": xml_dict.get("FromUserName"),
                            "FromUserName": xml_dict.get("ToUserName"),
                            "CreateTime": int(time.time()),
                            "MsgType": "text",
                            "Content": u"现在只支持文字回复啦QAQ",
                        }  
                    }
                    return_xml_str = xmltodict.unparse(return_dict)
                    return return_xml_str # 返回回复的xml字符串



@app.route('/wechat/profile')
def profile():
    # 如果用户同意授权，页面将跳转至 redirect_uri/?code=CODE&state=STATE
    # 若用户禁止授权，则重定向后不会带上code参数，仅会带上state参数redirect_uri?state=STATE

    user_code = request.args.get("code") # redirect_uri/?code=CODE&state=STATE
    if user_code is not None: # 如果用户同意授权
        # 通过token 换取access_token
        req_url = "https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code" % (APP_ID, APP_SECRET, user_code)
        
        # 获取access_token
        response_obj = urllib2.urlopen(req_url) # 发送请求，返回相应对象
        json_str = response_obj.read()
        json_dict  = json.loads(json_str) # json转化为字典格式
        
        access_token = json_dict.get("access_token")
        openid = json_dict.get("openid")

        # 获取用户信息的json
        userinfo_url = "https://api.weixin.qq.com/sns/userinfo?access_token=%s&openid=%s&lang=zh_CN" % (access_token, openid)
        userinfo_json_str = urllib2.urlopen(userinfo_url).read()
        userinfo_dict = json.loads(userinfo_json_str)

        return render_template("userinfo.html", user=userinfo_dict) # 返回模板


if __name__ == "__main__":
    app.run(port=8000, debug=True)


