#-*- coding:utf-8 -*-
from flask import Flask, redirect, url_for


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


if __name__ == "__main__":
    print app.url_map
    app.run()