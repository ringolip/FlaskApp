#-*- coding:utf-8 -*-
from flask import Flask, redirect, url_for, request, abort, Response, make_response, jsonify
from werkzeug.routing import BaseConverter
import json


#创建flask应用对象
# __name__表示当前模块的名字
# Flask以当前模块所在的目录为总目录，自动寻找此目录下的static,templates
app = Flask(__name__,
            static_url_path="/python") # 静态资源目录的url

app.config.from_pyfile("config.cfg")
# app.config["DEBUG"] = True

@app.route('/')
def index():
    return "Hello Flask!"

@app.route('/login')
def login():
    url = url_for("index")
    return redirect(url)



class CheckNumber(BaseConverter): # 继承父类转换器
    """
    自定义路由转换器
    """
    def __init__(self, url_map, *args):
        super(CheckNumber, self).__init__(url_map) # 继承父类初始化方法
        self.regex = args[0] #属性regex是自定义正则的关键，不能修改名字

app.url_map.converters['check'] = CheckNumber # 将自定义转换器加入url_map.converters的映射

@app.route('/rule/<check(r"1[34578]\d{9}"):phone_number>') # 在路由中定义了手机号码的正则
def checkcheck(phone_number):
    return "Your phone number:%s is right." % phone_number


@app.route('/req', methods=["GET","POST"]) # request
def req():
    name = request.form.get("name") # 接受表单的数据
    age = request.form.get("age")
    city = request.args.get("city") # 接受来自查询字符串中的信息
    name_list = request.form.getlist("name")
    print request.data
    return "name is %s, age is %s,city is %s." % (name, age, city)

@app.route('/upload', methods=["POST"]) # request.files文件属性
def upload():
    pic = request.files.get("pic") # 接受request中文件的属性
    if pic is None:
        return "文件未上传成功"
    else:
        pic.save("demo.jpg")
        return "保存成功"

@app.route('/abort_test', methods=["GET"])
def abort_test():
    # abort函数可以立即终止视图函数的执行，并返回给前端特定的信息
    # abort(400) # 返回状态码
    res = Response("Hello") # 返回响应体
    abort(res)

@app.errorhandler(404)
def err_handler(err):
    return "啊哦，错误了哦。 %s" % err


@app.route('/respon')
def respon():
    # return "rrrrrresponse", 400, {"name":"ringo", "city":"Shanghai"} # 以元祖形式返回响应(body, status, headers)
    res = make_response("responseeeeeee!") # 用make_response返回响应
    res.status = "400"
    # res.headers = {"name": "Ringolip"}
    res.headers["name"] = "Ringolip"
    return res


@app.route('/jso') # json
def jso():
    data = {
        "name":"rrrrrrringo",
        "age":"18",
    }
    # Content-Type: application/json
    # json_data = json.dumps(data) # 将字典转换为json字符串
    # return jsonify(data)
    # return json_data, 200, {"Content-Type": "application/json"} # 在response中构造Content-Type为json格式
    return jsonify(name="bbbbbrank") # 也可以在jsonify中直接传入参数


@app.route('/coo') # cookie
def coo():
    res = make_response("cooooookie")
    res.set_cookie("name", "flaskkkkk")
    res.set_cookie("age","18", max_age=3600) # set_cookie(key, value=’’, max_age=None)
    return res

@app.route('/getcoo')
def getcoo():
    coo = request.cookies.get("age")
    return coo

@app.route('/delcoo')
def delcoo():
    res = make_response("删除Cookie成功")
    res.delete_cookie("name") # delete_cookie(key)
    return res

if __name__ == "__main__":
    # print app.url_map
    app.run()