from app.api import bp
from app.extensions import db
from app.api.auth import token_auth
from app.models import Post, Comment, Permission
from app.utils.decorator import permission_required
from app.api.errors import error_response, bad_request
from flask import request, jsonify, url_for, g, current_app


@bp.route('/posts', methods=['POST'])
@token_auth.login_required
@permission_required(Permission.POST)
def create_post():
    data = request.get_json()
    if not data:
        return bad_request('You must post JSON data.')
    # print(data)
    message = {}
    # 暂时不需要检查title
    # if 'title' not in data or not data.get('title'):
    #     message['title'] = 'Title is required.'
    # elif len(data.get('title')) > 255:
    #     message['title'] = 'Title must less than 255 characters.'
    if 'content' not in data or not data.get('content'):
        message['content'] = 'Content is required.'
    if 'type' not in data or not data.get('type'):
        message['type'] = 'Type is required.'
    if message:
        return message
    post = Post()
    post.from_dict(data)
    post.author = g.current_user  # 通过auth.py中verify_token()传递过来的（同一个request中，需要先进行 Token 认证）
    db.session.add(post)
    db.session.commit()
    response = jsonify(post.to_dict())
    response.status_code = 201
    # HTTP协议要求201响应包含一个值为新资源URL的Location头部
    response.headers['Location'] = url_for('api.get_post', id=post.id)
    return response


@bp.route('/posts', methods=['GET'])
def get_posts():
    """返回所有Post，分页"""
    query_type = request.args.get('type', '', type=str)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)

    data = {}
    if not query_type:
        data = Post.to_collection_dict(Post.query.order_by(Post.timestamp.desc()), page, per_page, 'api.get_posts')
    else:
        data = Post.to_collection_dict(Post.query.filter_by(type=query_type).order_by(Post.timestamp.desc()), page, per_page, 'api.get_posts')
    return jsonify(data)


@bp.route('/posts/<int:id>', methods=['GET'])
def get_post(id):
    """返回单篇Post"""
    post = Post.query.get_or_404(id)
    return jsonify(post.to_dict())


@bp.route('/posts/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_post(id):
    """修改单篇Post内容"""
    post = Post.query.get_or_404(id)
    if g.current_user != post.author:
        return error_response(403)

    data = request.get_json()
    if not data:
        return bad_request('You must post JSON data.')

    message = {}
    if 'content' not in data or not data.get('content'):
        message['content'] = 'Content is required.'
    if message:
        return bad_request(message)

    post.from_dict(data)
    db.session.commit()
    return jsonify(post.to_dict())


@bp.route('/posts/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_post(id):
    """删除单篇Post"""
    post = Post.query.get_or_404(id)
    if g.current_user == post.author or g.current_user.can(Permission.ADMIN):
        db.session.delete(post)
        db.session.commit()
        return '', 204
    else:
        return error_response(403)


@bp.route('/posts/<int:id>/comments', methods=['GET'])
def get_post_comments(id):
    """返回当前文章下面的一级评论"""
    post = Post.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = min(
        request.args.get(
            'per_page', current_app.config['COMMENTS_PER_PAGE'], type=int), 100)
    # 先获取一级评论
    data = Comment.to_collection_dict(
        post.comments.filter(Comment.parent == None).order_by(Comment.timestamp.desc()), page, per_page,
        'api.get_post_comments', id=id)
    # 再添加子孙到一级评论的 descendants 属性上
    for item in data['items']:
        comment = Comment.query.get(item['id'])
        descendants = [child.to_dict() for child in comment.get_descendants()]
        # 按 timestamp 排序一个字典列表
        from operator import itemgetter
        item['descendants'] = sorted(descendants, key=itemgetter('timestamp'))
    return jsonify(data)


@bp.route('/posts/<int:id>/likeorunlike', methods=['GET'])
@token_auth.login_required
@permission_required(Permission.POST)
def like_or_unlike_post(id):
    """点赞或取消点赞Post"""
    post = Post.query.get_or_404(id)
    if post.is_liked_by(g.current_user):
        post.unliked_by(g.current_user)
    else:
        post.liked_by(g.current_user)

    db.session.add(post)
    db.session.commit()
    return jsonify({
        'status': 'success',
        'current_likes': len(post.likers)
    })


@bp.route('/posts/<int:id>/likes', methods=['GET'])
# @token_auth.login_required
# @permission_required(Permission.POST)
def get_post_likes(id):
    """返回单篇post的点赞数"""
    post = Post.query.get_or_404(id)
    return jsonify({'likes': len(post.likers)})