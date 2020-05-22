import re
from app.api import bp
from datetime import datetime
from app.extensions import db
from app.api.auth import token_auth
from app.api.errors import bad_request, error_response
from flask import request, jsonify, url_for, g, current_app
from app.models import User, Permission, Comment, Notification


@bp.route('/users', methods=['POST'])
def create_user():
    """注册一个用户"""
    data = request.get_json()
    # print(data['school'])
    if not data:
        return bad_request('You must post JSON data.')

    message = {}
    # 检查用户名
    if 'username' not in data or not data.get('username', None):
        message['username'] = 'Username required.'
    # 检查学校
    if 'school' not in data or not data.get('school', None):
        message['school'] = 'School required.'
    # 检查邮箱
    pattern = '^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'
    if 'email' not in data or not re.match(pattern, data.get('email', None)):
        message['email'] = 'Email required.'
    # print(data.get('username'))
    # 检查密码
    if 'password' not in data or not data.get('password', None):
        message['password'] = 'Password required.'

    if User.query.filter_by(username=data.get('username', None)).first():
        message['username'] = 'Duplicate username, please use a different username.'
    if User.query.filter_by(email=data.get('email', None)).first():
        message['email'] = 'Duplicate email, please use a different email.'

    if message:
        return bad_request(message)

    user = User()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 201
    # HTTP协议要求201响应包含一个值为新资源URL的Location头部
    response.headers['Location'] = url_for('api.get_user', id=user.id)
    response.headers['Content-Type'] = 'text/plain;charset=UTF-8'
    return response


@bp.route('/users', methods=['GET'])
@token_auth.login_required
def get_users():
    """返回用户集合，分页"""
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = User.to_collection_dict(User.query, page, per_page, 'api.get_users')
    return jsonify(data)


@bp.route('/users/<int:id>', methods=['GET'])
@token_auth.login_required
def get_user(id):
    """返回一个用户"""
    return jsonify(User.query.get_or_404(id).to_dict())


@bp.route('/users/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_user(id):
    """修改一个用户"""
    user = User.query.get_or_404(id)

    data = request.get_json()
    if not data:
        return bad_request('You must post JSON data.')

    message = {}
    # 检查是否为空值
    if 'username' in data and not data.get('username', None):
        message['username'] = 'Username required.'
    if 'school' in data and not data.get('school', None):
        message['school'] = 'School required.'
    # pattern = '^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'
    # if 'email' in data and not re.match(pattern, data.get('email', None)):
    #     message['email'] = 'Please provide a valid email address.'

    # 检查是否重复
    if 'username' in data and data['username'] != user.username and \
            User.query.filter_by(username=data['username']).first():
        message['username'] = 'Duplicate username, please use a different username.'

    # if 'email' in data and data['email'] != user.email and \
    #         User.query.filter_by(email=data['email']).first():
    #     message['email'] = 'Please use a different email address.'

    if message:
        return bad_request(message)

    user.from_dict(data)
    db.session.commit()
    return jsonify(user.to_dict())


@bp.route('/users/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_user(id):
    """删除一个用户"""
    user = User.query.get_or_404(id)
    if g.current_user == user or g.current_user.can(Permission.ADMIN):
        db.session.delete(user)
        db.session.commit()
        return '', 204
    else:
        return error_response(403)


@bp.route('/users/<int:id>/received-comments/', methods=['GET'])
@token_auth.login_required
def get_user_received_comments(id):
    """返回该用户收到的所有评论"""

    user = User.query.get_or_404(id)
    if g.current_user != user:
        return error_response(403)

    page = request.args.get('page', 1, type=int)
    per_page = min(
        request.args.get(
            'per_page', current_app.config['COMMENTS_PER_PAGE'], type=int), 100)

    # 用户发布的所有文章ID集合
    user_posts_ids = [post.id for post in g.current_user.posts.all()]

    # 评论的 post_id 在 user_posts_ids 集合中，且评论的 author 不是当前用户（即文章的作者）
    data = Comment.to_collection_dict(
        Comment.query.filter(Comment.post_id.in_(user_posts_ids), Comment.author != g.current_user)
        .order_by(Comment.is_read, Comment.timestamp.desc()),
        page, per_page, 'api.get_user_received_comments', id=id)

    # 标记哪些评论是新的
    last_read_time = user.last_recived_comments_read_time or datetime(2020, 1, 1)
    for item in data['items']:
        if item['timestamp'] > last_read_time:
            item['is_new'] = True

    # 需要考虑分页的问题，比如新评论有25条，默认分页是每页10条，
    # 如果用户请求第一页时就更新 last_received_comments_read_time，那么后15条就被认为不是新评论了，这是不对的
    if data['_meta']['page'] * data['_meta']['per_page'] >= user.new_recived_comments():
        # 更新 last_received_comments_read_time 属性值
        user.last_received_comments_read_time = datetime.utcnow()
        # 将新评论通知的计数归零
        user.add_notification('unread_received_comments_count', 0)
    else:
        # 用户剩余未查看的新评论数
        n = user.new_recived_comments() - data['_meta']['page'] * data['_meta']['per_page']
        # 将新评论通知的计数更新为未读数
        user.add_notification('unread_received_comments_count', n)

    db.session.commit()
    return jsonify(data)


@bp.route('/users/<int:id>/notifications/', methods=['GET'])
@token_auth.login_required
def get_user_notifications(id):
    """
    返回该用户的新通知
    增加服务器并发负担且意义不大，暂时不用
    """

    user = User.query.get_or_404(id)
    if g.current_user != user:
        return error_response(403)

    # 只返回上次看到的通知以来发生的新通知
    # 比如用户在 10:00:00 请求一次该API，在 10:00:10 再次请求该API只会返回 10:00:00 之后产生的新通知
    since = request.args.get('since', 0.0, type=float)
    notifications = user.notifications.filter(
        Notification.timestamp > since).order_by(Notification.timestamp.asc())
    return jsonify([n.to_dict() for n in notifications])


