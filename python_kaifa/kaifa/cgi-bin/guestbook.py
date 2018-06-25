#coding:utf-8
import shelve
from datetime import datetime

from flask import Flask, request, render_template, redirect, escape, Markup

application = Flask(__name__)

DATA_FILE = 'guestbook.bat'

def save_data(name, comment, creat_at):
    """保存提交的数据
    """
    #用shelve打开数据库文件
    database = shelve.open(DATA_FILE)
    #获取数据表
    if 'greeting_list' not in database:
        greeting_list = []
    else:
        greeting_list = database['greeting_list']
    #往表头插入数据
    greeting_list.insert(0,{
        'name':name,
        'comment':comment,
        'creat_at':creat_at,
        })
    #更新数据库
    database['greeting_list'] = greeting_list
    #关闭数据库
    database.close()

def load_data():
    """返回以提交的数据
    """
    #打开
    database = shelve.open(DATA_FILE)
    #返回greeting_list
    greeting_list = database.get('greeting_list',[])
    database.close()
    return greeting_list



@application.route('/')
def index():
    """ 首页
    使用模板显示页面
    """
    greeting_list = load_data()
    return render_template('index.html', greeting_list=greeting_list)

@application.route('/post', methods=['POST'])
def post():
    """ 用于提交评论的 URL
    """
    # 获取已提交的数据
    name = request.form.get('name')# 名字
    comment = request.form.get('comment')# 留言
    create_at = datetime.now()# 投稿时间(当前时间)
    # 保存数据
    save_data(name, comment, create_at)
    # 保存后重定向到首页
    return redirect('/')

@application.template_filter('nl2br')
def nl2br_filter(s):
    """ 将换行符置换为 br 标签的模板过滤器
    """
    return escape(s).replace('\n', Markup('<br>'))

@application.template_filter('datetime_fmt')
def datetime_fmt_filter(dt):
    """ 使 datetime 对象更容易分辨的模板过滤器
    """
    return dt.strftime('%Y/%m/%d %H:%M:%S')

if __name__ == '__main__':
    # 在 IP 地址 127.0.0.1 的 8000 端口运行应用程序
    application.run('127.0.0.1', 8080, debug=True)
