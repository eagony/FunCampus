from app.api import bp
from app.extensions import db
from app.api.auth import token_auth
from app.models import Post, Comment, Permission
from app.utils.decorator import permission_required
from app.api.errors import error_response, bad_request
from flask import request, jsonify, url_for, current_app, g


@bp.route('/comments', methods=['POST'])
@token_auth.login_required
@permission_required(Permission.COMMENT)
def create_comment():
    """为Post添加评论"""
    data = request.get_json()
    if not data:
        return bad_request('You must post JSON data.')
    if 'content' not in data or not data.get('content').strip():
        return bad_request('Content is required.')
    if 'post_id' not in data or not data.get('post_id'):
        return bad_request('Post id is required.')

    post = Post.query.get_or_404(int(data.get('post_id')))
    comment = Comment()
    comment.from_dict(data)
    comment.author = g.current_user
    comment.post = post
    # 给文章作者发送新评论通知
    post.author.add_notification('unread_received_comments_count',
                                 post.author.new_received_comments())
    db.session.add(comment)
    db.session.commit()
    response = jsonify(comment.to_dict())
    response.status_code = 201
    # HTTP协议要求201响应包含一个值为新资源URL的Location头部
    response.headers['Location'] = url_for('api.get_comment', id=comment.id)
    return response


@bp.route('/comments', methods=['GET'])
@token_auth.login_required
def get_comments():
    """返回评论集合，分页"""
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', current_app.config['COMMENTS_PER_PAGE'], type=int), 100)
    data = Comment.to_collection_dict(Comment.query.order_by(Comment.timestamp.desc()), page, per_page,
                                      'api.get_comments')
    return jsonify(data)


@bp.route('/comments/<int:id>', methods=['GET'])
@token_auth.login_required
def get_comment(id):
    """返回单条评论"""
    comment = Comment.query.get_or_404(id)
    return jsonify(comment.to_dict())


@bp.route('/comments/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_comment(id):
    """修改单条评论"""
    comment = Comment.query.get_or_404(id)
    if g.current_user != comment.author and not g.current_user.can(Permission.COMMENT):
        return error_response(403)
    data = request.get_json()
    if not data:
        return bad_request('You must put JSON data.')
    comment.from_dict(data)
    db.session.commit()
    return jsonify(comment.to_dict())


@bp.route('/comments/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_comment(id):
    """删除单条评论"""
    comment = Comment.query.get_or_404(id)
    # 评论作者和管理员有权删除该评论
    if g.current_user == comment.author or g.current_user.can(Permission.ADMIN):
        # 给文章作者发送新评论通知(需要自动减1)
        comment.post.author.add_notification('unread_received_comments_count',
                                             comment.post.author.new_received_comments())
        db.session.delete(comment)
        db.session.commit()
        return '', 204
    else:
        return error_response(403)


@bp.route('/comments/<int:id>/like', methods=['GET'])
@token_auth.login_required
@permission_required(Permission.COMMENT)
def like_comment(id):
    """点赞评论"""
    comment = Comment.query.get_or_404(id)
    comment.liked_by(g.current_user)
    db.session.add(comment)
    db.session.commit()
    return jsonify({
        'status': 'success',
        'message': 'You are now liking comment [ id: %d ].' % id
    })


@bp.route('/comments/<int:id>/unlike', methods=['GET'])
@token_auth.login_required
@permission_required(Permission.COMMENT)
def unlike_comment(id):
    """取消点赞评论"""
    comment = Comment.query.get_or_404(id)
    comment.unliked_by(g.current_user)
    db.session.add(comment)
    db.session.commit()
    return jsonify({
        'status': 'success',
        'message': 'You are not liking comment [ id: %d ] anymore.' % id
    })

