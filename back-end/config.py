import os
from dotenv import load_dotenv
from flask_uploads import IMAGES

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'we-can-go-like-a-samurai'

    # 数据库
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 评论分页
    COMMENTS_PER_PAGE = 10

    # 管理员邮箱
    ADMINS = ['admin@qq.com']

    # 图片上传
    UPLOADED_PHOTO_DEST = os.path.dirname(os.path.abspath(__file__)) + '\\static\\images'
    UPLOADED_PHOTO_ALLOW = IMAGES
