# -*- coding:utf-8 -*-
from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell


app = Flask(__name__)



# 配置数据库
class Config(object):
    #设置连接数据库的URL
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@127.0.0.1:3306/booklists'

    # 自动跟踪数据库
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    SECRET_KEY = "adsasdsad" # 设置秘钥

app.config.from_object(Config)

# 注册至SQLAlchemy
db = SQLAlchemy(app)

# 创建脚本管理工具对象
manager = Manager(app)

# 创建数据库迁移对象
migrate = Migrate(app, db)

# 在脚本工具中添加数据库迁移语句
manager.add_command("db", MigrateCommand)

class Author(db.Model): # 定义数据模型
    __tablename__ = "tbl_authors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64))
    books = db.relationship("Book", backref="author")
    def __repr__(self):
        return "Author obj name: %s" % self.name


class Book(db.Model):
    __tablename__ = "tbl_books"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    author_id = db.Column(db.Integer, db.ForeignKey("tbl_authors.id")) # 外键
    def __repr__(self):
        return "Book obj name: %s" % self.name


class BookForm(FlaskForm): # 定义表单类
    author = StringField(label=u"作者", validators=[DataRequired(u"不能为空")])
    book = StringField(label=u"书籍", validators=[DataRequired(u"不能为空")])
    submit = SubmitField()




@app.route('/', methods=["GET","POST"])
def index():
    form = BookForm()

    if form.validate_on_submit(): # 如果数据验证正确且为POST方式发送
        author_name = form.author.data # 向数据库添加数据
        book_name = form.book.data
        author = Author(name=author_name)
        db.session.add(author)
        db.session.commit()

        book = Book(name=book_name, author=author)
        db.session.add(book)
        db.session.commit()
        # return redirect(url_for("index")) # 重定向刷新

    authors = Author.query.all() # 查询Author对象
    return render_template("books.html", authors=authors, form=form)


@app.route('/del_book')
def del_book():
    book_id = request.args.get("book_id") # 存储request中的查询字符串的id
    book = Book.query.filter_by(id=book_id).first()
    db.session.delete(book) # 删除数据
    db.session.commit()

    return redirect(url_for("index")) # 重定向至主页


if __name__ == "__main__":
    manager.run()
    # app.run(debug=True)
    # # 清除数据库里的所有数据
    # db.drop_all()

    # # 创建所有的表
    # db.create_all()

    # au_xi = Author(name='我吃西红柿')
    # au_qian = Author(name='萧潜')
    # au_san = Author(name='唐家三少')
    # db.session.add_all([au_xi,au_qian,au_san])
    # db.session.commit()

    # bk_xi = Book(name='吞噬星空', author_id=au_xi.id)
    # bk_xi2 = Book(name='寸芒', author_id=au_xi.id)
    # bk_qian = Book(name='飘渺之旅', author_id=au_qian.id)
    # bk_san = Book(name='冰火魔厨', author_id=au_san.id)
    # db.session.add_all([bk_xi,bk_xi2,bk_qian,bk_san])
    # db.session.commit()



