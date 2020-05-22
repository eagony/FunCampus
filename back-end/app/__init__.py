from flask import Flask
from config import Config
from app.api import bp as api_bp
from app.extensions import cors, db, migrate


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    configure_blueprints(app)
    configure_extensions(app)

    return app


def configure_blueprints(app):
    # 注册蓝图
    app.register_blueprint(api_bp, url_prefix='/api')


def configure_extensions(app):
    # 配置扩展应用
    cors.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
