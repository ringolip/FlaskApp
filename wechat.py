#-*- coding:utf-8 -*-
from flask import Flask, request, abort
import hashlib 
import xmltodict
import time

RINGO_TOKEN = "ringo" # 微信接口Token

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



if __name__ == "__main__":
    app.run(port=8000, debug=True)


