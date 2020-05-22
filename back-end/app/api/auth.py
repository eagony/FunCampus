from flask import g
from app.models import User
from app.api.errors import error_response
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()


@basic_auth.verify_password
def verify_password(username, password):
    """用于检查用户提供的用户名和密码"""
    user = User.query.filter_by(username=username).first()
    if user is None:
        return False
    g.current_user = user
    return user.check_password(password)


@basic_auth.error_handler
def basic_auth_error():
    """用于在认证失败的情况下返回错误响应"""
    return error_response(401)


@token_auth.verify_token
def verify_token(token):
    """用于检查用户请求是否有token，并且token真实存在且在有效期内"""
    g.current_user = User.verify_jwt(token) if token else None
    return g.current_user is not None


@token_auth.error_handler
def token_auth_error():
    """用于在Token Auth 认证失败的情况下返回错误响应"""
    return error_response(401)
