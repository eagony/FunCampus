import os
from config import Config
from app import create_app, db
from flask import request, jsonify
from app.api.auth import token_auth
from app.utils.decorator import permission_required
from app.models import User, Post, Comment, Role, Permission, Statistic
from flask_uploads import UploadSet, IMAGES, configure_uploads

app = create_app(Config)

# 配置uploads
photos = UploadSet('PHOTO')
configure_uploads(app, photos)


# 图片上传
@token_auth.login_required
@permission_required(Permission.POST)
@app.route('/upload/picture', methods=['POST'])
def upload_picture():
    if 'file' in request.files:
        file_name = photos.save(request.files['file'])
        return jsonify({'data': {'state': 'success', 'file_name': file_name, 'url': photos.url(file_name)}})
    return jsonify('no picture detected.')


# 配置Flask shell
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Comment': Comment, 'Role': Role}


@app.cli.command()
def deploy():
    """ run deployment tasks """
    # 1. 创建角色
    Role.insert_roles()
    # 2. 初始化统计数据
    Statistic.init_statistic()
