from flask_cors import CORS
from sqlalchemy import MetaData
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# 跨域访问
cors = CORS()

# 数据库
db = SQLAlchemy(metadata=MetaData(naming_convention={
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}))

# 数据库迁移同步
migrate = Migrate(render_as_batch=True)  # 启用删除整列
