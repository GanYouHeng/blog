"""__author__ = 干友恒"""

import redis
from flask import Flask
from flask_script import Manager
from flask_session import Session

from back.models import db
from back.views import back_blue


from web.views import web_blue

# 生成Flask对象
app = Flask(__name__)

# 管理蓝图
app.register_blueprint(blueprint=back_blue, url_prefix='/back')
app.register_blueprint(blueprint=web_blue, url_prefix='/web')

# 加密, 加密复杂程度和设置有关
app.secret_key = '1234567890thnbtn'

# 配置redis
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis.Redis(host='127.0.0.1', port=6379)
Session(app)

# 配置数据库连接信息
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:ganyouheng@127.0.0.1:3306/blog'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# 生成Manager对象
manage = Manager(app)


if __name__ == '__main__':
    # 使用manage管理启动命令
    manage.run()