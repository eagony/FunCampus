import jwt
import json
import base64
from hashlib import md5
from app.extensions import db
from flask import url_for, current_app
from datetime import datetime, timedelta, date
from sqlalchemy.orm import relationship, backref
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Float


class PaginatedAPIMixin(object):
    """
    辅助分页类，用于将用户集合转换成JSON
    """

    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        # 如果当前没有任何资源时，或者前端请求的 page 越界时，都会抛出 404 错误
        # 由 @bp.app_errorhandler(404) 自动处理，即响应 JSON 数据：{ error: "Not Found" }
        resources = query.paginate(page, per_page)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page,
                                **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page,
                                **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page,
                                **kwargs) if resources.has_prev else None
            }
        }
        return data


# 关注他人 暂时不用
followers = db.Table(
    'followers',
    Column('follower_id', Integer, ForeignKey('users.id')),
    Column('followed_id', Integer, ForeignKey('users.id')),
    Column('timestamp', DateTime, default=datetime.utcnow)
)

# 评论点赞 暂时也不用
comments_likes = db.Table(
    'comments_likes',
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('comment_id', Integer, ForeignKey('comments.id')),
    Column('timestamp', DateTime, default=datetime.utcnow)
)

# 评论发布
posts_likes = db.Table(
    'posts_likes',
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('post_id', Integer, ForeignKey('posts.id')),
    Column('timestamp', DateTime, default=datetime.utcnow)
)


class User(PaginatedAPIMixin, db.Model):
    """
    用户模型, 存储和操作用户实例
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(64), index=True, unique=True)
    school = Column(String(64))
    email = Column(String(120), index=True, unique=True)
    password_hash = Column(String(128))

    name = Column(String(64))
    avatar_url = Column(String(128))
    location = Column(String(64))
    about_me = Column(Text())

    registration_date = Column(DateTime, default=datetime.utcnow)
    last_seen = Column(DateTime, default=datetime.utcnow)

    # 反向引用，直接查询出当前用户的所有博客文章; 同时，Post实例中会有 author 属性
    # cascade 用于级联删除，当删除user时，该user下面的所有posts都会被级联删除
    posts = relationship('Post', backref='author', lazy='dynamic', cascade='all, delete-orphan')

    # 用户所属的角色
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    # 反向引用，直接查询出当前用户的所有评论; 同时，Comment实例中会有 author 属性
    # cascade 用于级联删除，当删除user时，该user下面的所有 comments 都会被级联删除
    comments = relationship('Comment', backref='author', lazy='dynamic', cascade='all, delete-orphan')

    # 用户最后一次查看 收到的评论 页面的时间，用来判断哪些收到的评论是新的
    last_received_comments_read_time = db.Column(db.DateTime)

    # 用户的通知
    notifications = db.relationship('Notification', backref='user',
                                    lazy='dynamic', cascade='all, delete-orphan')

    # 关注者和关注的人，暂时不管
    # followeds 该用户关注的用户
    # followers 关注该用户的用户
    # followeds = relationship(
    #     'User',
    #     secondary=followers,
    #     primaryjoin=(followers.c.follower_id == id),
    #     secondaryjoin=(followers.c.followed_id == id),
    #     backref=backref('followers', lazy='dynamic'),
    #     lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def avatar(self, size):
        """根据用户邮箱随机生成头像"""
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self, include_email=False):
        """将User实例转换成JSON对象并返回给前端"""
        data = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'school': self.school,
            'name': self.name,
            'about_me': self.about_me,
            'avatar_url': self.avatar_url if self.avatar_url else self.avatar(64),
            'role': self.role.to_dict()['name'],
            'posts_count': self.posts.count(),
            'comments_count': self.comments.count(),
            'last_seen': self.last_seen.isoformat() + 'Z',
            'registration_date': self.registration_date.isoformat() + 'Z',
            '_links': {
                'self': url_for('api.get_user', id=self.id)
            }
        }

        return data

    def from_dict(self, data, new_user=False):
        """从JSON对象实例化User对象"""
        for field in ['username', 'school', 'email', 'name', 'about_me', 'avatar_url']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])
            # 新建用户时，给用户自动分配角色
            if self.role is None:
                if self.email in current_app.config['ADMINS']:
                    self.role = Role.query.filter_by(slug='administrator').first()
                else:
                    self.role = Role.query.filter_by(default=True).first()

    def ping(self):
        """更新用户上线时间"""
        self.last_seen = datetime.utcnow(),
        db.session.add(self)
        db.session.commit()

    def get_jwt(self, expires_in=3600 * 24 * 7):
        """加密传输用户信息"""
        now = datetime.utcnow()
        payload = {
            'user_id': self.id,
            'user_name': self.name if self.name else self.username,
            'user_avatar': base64.b64encode(self.avatar_url.encode('utf-8')).decode('utf-8') if self.avatar_url
            else base64.b64encode(self.avatar(64).encode('utf-8')).decode('utf-8'),
            'permissions': self.role.get_permissions(),
            'exp': now + timedelta(seconds=expires_in),
            'iat': now
        }
        return jwt.encode(
            payload,
            current_app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_jwt(token):
        try:
            payload = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256'])
        except jwt.exceptions.ExpiredSignatureError as e:
            return None
        return User.query.get(payload.get('user_id'))

    def can(self, perm):
        """检查用户是否有指定的权限"""
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        """检查是否为管理员"""
        return self.can(Permission.ADMIN)

    def new_received_comments(self):
        """用户发布的文章下面收到的新评论计数"""
        last_read_time = self.last_received_comments_read_time or datetime(2020, 1, 1)
        # 用户发布的所有文章
        user_posts_ids = [post.id for post in self.posts.all()]
        # 用户收到的所有评论，即评论的 post_id 在 user_posts_ids 集合中，且评论的 author 不是当前用户（即文章的作者）
        received_comments = Comment.query.filter(Comment.post_id.in_(user_posts_ids), Comment.author != self).order_by(
            Comment.is_read, Comment.timestamp.desc())
        # 新评论
        return received_comments.filter(Comment.timestamp > last_read_time).count()

    def add_notification(self, name, data):
        """给用户实例对象增加通知"""
        # 如果具有相同名称的通知已存在，则先删除该通知
        self.notifications.filter_by(name=name).delete()
        # 为用户添加通知，写入数据库
        n = Notification(name=name, payload_json=json.dumps(data), user=self)
        db.session.add(n)
        db.session.commit()
        return n


class Post(PaginatedAPIMixin, db.Model):
    """Post模型, 管理用户发布的各种类型的Post"""
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    type = Column(String(20))
    title = Column(String(255))
    content = Column(Text)
    picture_url = Column(String(128))
    timestamp = Column(DateTime, index=True, default=datetime.utcnow)

    contact_type = Column(String(8))
    contact_id = Column(String(32))

    # 外键, 直接操纵数据库当user下面有posts时不允许删除user，下面仅仅是 ORM-level “delete” cascade
    # db.ForeignKey('users.id', ondelete='CASCADE') 会同时在数据库中指定 FOREIGN KEY level “ON DELETE” cascade
    author_id = Column(Integer, ForeignKey('users.id'))

    # 反向引用，直接查询出当前Post下的所有评论; 同时，Comment实例中会有 post 属性
    # cascade 用于级联删除，当删除post时，该post下面的所有 comment 都会被级联删除
    comments = relationship('Comment', backref='post', lazy='dynamic', cascade='all, delete-orphan')

    # 外键，点赞用户集合， 一对多关系
    likers = relationship('User', secondary=posts_likes, backref=db.backref('liked_posts', lazy='dynamic'))

    def __repr__(self):
        return '<Post {}>'.format(self.title)

    def from_dict(self, data):
        for field in ['title', 'content', 'type', 'contact_type', 'contact_id', 'picture_url']:
            if field in data:
                setattr(self, field, data[field])

    def to_dict(self):
        data = {
            'id': self.id,
            'type': self.type,
            'title': self.title,
            'content': self.content,
            'picture_url': self.picture_url,
            'timestamp': self.timestamp,
            'contact_type': self.contact_type,
            'contact_id': self.contact_id,
            'likers_id': [user.id for user in self.likers],
            'author': {
                'id': self.author.id,
                'username': self.author.username,
                'name': self.author.name,
                'school': self.author.school,
                'avatar': self.author.avatar_url if self.author.avatar_url else self.author.avatar(64)
            },
            'comments_count': self.comments.count(),
            '_links': {
                'self': url_for('api.get_post', id=self.id),
                'author_url': url_for('api.get_user', id=self.author_id),
                'comments_url': url_for('api.get_post_comments', id=self.id)
            }
        }

        return data

    def is_liked_by(self, user):
        """判断用户是否已点过赞"""
        return user in self.likers

    def liked_by(self, user):
        """点赞"""
        if not self.is_liked_by(user):
            self.likers.append(user)

    def unliked_by(self, user):
        """取消点赞"""
        if self.is_liked_by(user):
            self.likers.remove(user)


class Comment(PaginatedAPIMixin, db.Model):
    """用户评论模型"""
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    content = Column(Text)
    timestamp = Column(DateTime, index=True, default=datetime.utcnow)
    # 作者会收到评论提醒，可以标记为已读
    is_read = Column(Boolean, default=False)
    # 屏蔽显示
    is_disabled = Column(Boolean, default=False)
    # 外键，点赞用户集合， 一对多关系
    likers = relationship('User', secondary=comments_likes, backref=db.backref('liked_comments', lazy='dynamic'))
    # 外键，评论作者的ID
    author_id = Column(Integer, ForeignKey('users.id'))
    # author = relationship('User', backref='')
    # 外键，评论所属发布的ID
    post_id = Column(Integer, ForeignKey('posts.id'))
    # 自引用的多级评论实现
    parent_id = Column(Integer, ForeignKey('comments.id', ondelete='CASCADE'))
    # 级联删除的CASCADE必须定义在“多”的那一侧，所以不能使用:
    # parent = relationship('Comment', backref='children', remote_side=[id], cascade='all, delete-orphan')
    parent = relationship('Comment', backref=backref('children', cascade='all, delete-orphan'), remote_side=[id])

    def __repr__(self):
        return '<Comment {}>'.format(self.id)

    def get_descendants(self):
        """递归获取一级评论的所有子评论"""
        data = set()

        def descendants(comment):
            if comment.children:
                data.update(comment.children)
                for child in comment.children:
                    descendants(child)

        descendants(self)

        return data

    def from_dict(self, data):
        for field in ['content', 'author_id', 'post_id', 'parent_id']:
            if field in data:
                setattr(self, field, data[field])

    def to_dict(self):
        data = {
            'id': self.id,
            'content': self.content,
            'timestamp': self.timestamp,
            'is_read': self.is_read,
            'is_disabled': self.is_disabled,
            'likes_id': [user.id for user in self.likers],
            'author': {
                'id': self.author.id,
                'username': self.author.username,
                'name': self.author.name,
                'avatar': self.author.avatar_url if self.author.avatar_url else self.author.avatar(64)
            },

            'post': {
                'id': self.post.id,
                'title': self.post.title,
                'author': self.post.author.id
            },
            'parent_id': self.parent_id if self.parent else None,
            '_links': {
                'self': url_for('api.get_comment', id=self.id),
                'author_url': url_for('api.get_user', id=self.author_id),
                'post_url': url_for('api.get_post', id=self.post_id),
                'parent_url': url_for('api.get_comment', id=self.parent.id) if self.parent else None,
                'children': [url_for('api.get_comment', id=child.id) for child in
                             self.children] if self.children else None
            }
        }
        return data

    def is_liked_by(self, user):
        """判断用户是否已点过赞"""
        return user in self.likers

    def liked_by(self, user):
        """点赞"""
        if not self.is_liked_by(user):
            self.likers.append(user)

    def unliked_by(self, user):
        """取消点赞"""
        if self.is_liked_by(user):
            self.likers.remove(user)


class Permission:
    """
    权限认证中的各种操作，对应二进制的位，比如
    VISIT:      0b00000001，转换为十六进制为 0x01
    POST:       0b00000010，转换为十六进制为 0x02
    COMMENT:    0b00000100，转换为十六进制为 0x04
    FOLLOW:     0b00001000，转换为十六进制为 0x08
    CHAT:       0b00010000，转换为十六进制为 0x10
    DELETE:     0b00100000，转换为十六进制为 0x20
    暂时保留一位 0x40
    ADMIN:      0b10000000，转换为十六进制为 0x80
    """

    # 浏览权限
    VISIT = 0x01
    # 发表权限
    POST = 0x02
    # 发表评论、评论点赞与踩权限
    COMMENT = 0x04
    # 关注其它用户权限
    FOLLOW = 0x08
    # 站内聊天权限
    CHAT = 0x10
    # 删除post和comment权限
    DELETE = 0x20
    # 管理网站的权限(对应管理员角色)
    ADMIN = 0x80


class Role(PaginatedAPIMixin, db.Model):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    slug = Column(String(255), unique=True)
    name = Column(String(255))  # 角色名称
    default = Column(Boolean, default=False, index=True)  # 当新增用户时，是否将当前角色作为默认角色赋予新用户
    permissions = Column(Integer)  # 角色拥有的权限，各操作对应一个二进制位，能执行某项操作的角色，其位会被设为 1
    users = relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    @staticmethod
    def insert_roles():
        """
        应用部署时，应该主动执行此函数，添加以下角色
        注意: 未登录的用户，可以浏览，但不能评论或点赞等
        shutup:        0b0000 0000 (0x00) 用户被关小黑屋，收回所有权限
        reader:        0b0000 0011 (0x03) 可以关注别人、评论与点赞，但不能发表文章
        author:        0b0000 0111 (0x07) 可以关注别人、评论与点赞，发表文章
        administrator: 0b1000 0111 (0x87) 超级管理员，拥有全部权限

        以后如果要想添加新角色，或者修改角色的权限，修改 roles 数组，再运行函数即可
        """
        roles = {
            'nothing': ('无权限', []),
            'visitor': ('游客', [Permission.VISIT]),
            'user': (
                '普通用户', [Permission.VISIT, Permission.POST, Permission.COMMENT, Permission.FOLLOW, Permission.CHAT]),
            'administrator': ('管理员', [
                Permission.VISIT, Permission.POST, Permission.COMMENT, Permission.FOLLOW, Permission.CHAT,
                Permission.DELETE, Permission.ADMIN])
        }
        default_role = 'user'
        for r in roles:  # r 是字典的键，比如 'reader'
            role = Role.query.filter_by(slug=r).first()
            if role is None:
                role = Role(slug=r, name=roles[r][0])
            role.reset_permissions()
            for perm in roles[r][1]:
                role.add_permission(perm)
            role.default = (role.slug == default_role)
            db.session.add(role)
        db.session.commit()

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def get_permissions(self):
        """获取角色的具体操作权限列表"""
        p = [(Permission.FOLLOW, 'follow'),
             (Permission.COMMENT, 'comment'),
             (Permission.VISIT, 'visit'),
             (Permission.POST, 'post'),
             (Permission.CHAT, 'chat'),
             (Permission.DELETE, 'delete'),
             (Permission.ADMIN, 'admin')]
        # 过滤掉没有权限，注意不能用 for 循环，因为遍历列表时删除元素可能结果并不是你想要的，
        # 参考: https://segmentfault.com/a/1190000007214571
        new_p = filter(lambda x: self.has_permission(x[0]), p)
        return ','.join(x[1] for x in new_p)  # 用逗号拼接成str

    def to_dict(self):
        data = {
            'id': self.id,
            'slug': self.slug,
            'name': self.name,
            'default': self.default,
            'permissions': self.permissions,
            '_links': {
                'self': url_for('api.get_roles', id=self.id)
            }
        }
        return data

    def from_dict(self, data):
        for field in ['slug', 'name', 'permissions']:
            if field in data:
                setattr(self, field, data[field])

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<Role {}>'.format(self.name)


class Notification(db.Model):  # 不需要分页
    __tablename__ = 'notifications'
    id = Column(Integer, primary_key=True)
    name = Column(String(128), index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    timestamp = Column(Float, index=True, default=datetime.utcnow().timestamp())
    payload_json = Column(Text)

    def __repr__(self):
        return '<Notification {}>'.format(self.id)

    def get_data(self):
        return json.loads(str(self.payload_json))

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'user': {
                'id': self.user.id,
                'username': self.user.username,
                'name': self.user.name,
                'avatar': self.user.avatar(128)
            },
            'timestamp': self.timestamp,
            'payload': self.get_data(),
            '_links': {
                'self': url_for('api.get_notification', id=self.id),
                'user_url': url_for('api.get_user', id=self.user_id)
            }
        }
        return data

    def from_dict(self, data):
        for field in ['body', 'timestamp']:
            if field in data:
                setattr(self, field, data[field])



class Statistic(PaginatedAPIMixin, db.Model):
    __tablename__ = 'statistics'
    id = Column(Integer, primary_key=True)
    date = Column(String(10), 
                    index=True, 
                    unique=True,
                    default=str(date.today()))

    # 总计
    total_views = Column(Integer, default=0)
    total_users = Column(Integer, default=0)
    total_posts = Column(Integer, default=0)
    total_comments = Column(Integer, default=0)

    # 每日新增
    new_views = Column(Integer, default=0)
    new_users = Column(Integer, default=0)
    new_posts = Column(Integer, default=0)
    new_comments = Column(Integer, default=0)

    def __repr__(self):
        return '<Statistic {}>'.format(self.date)

    def to_dict(self):

        data = {
            'id': self.id,
            'date': self.date,
            'total_views': self.total_views,
            'total_users': self.total_users,
            'total_posts': self.total_posts,
            'total_comments': self.total_comments,
            'new_views': self.new_views,
            'new_users': self.new_users,
            'new_posts': self.new_posts,
            'new_comments': self.new_comments
        }

        return data
    @staticmethod
    def init_statistic():
        """初始化第一天的统计数据"""
        if not Statistic.query.first():
            initially_statistic = Statistic()
            db.session.add(initially_statistic)
            db.session.commit()

    def from_yesterday_statistic(self, yesterday_statistic):
        for field in ['total_views', 'total_users', 'total_posts', 'total_comments']:
            setattr(self, field, yesterday_statistic.to_dict[field])

    def increase_view(self):
        self.total_views += 1
        self.new_views += 1

    def increase_user(self):
        self.total_users += 1
        self.new_users += 1

    def increase_post(self):
        self.total_posts += 1
        self.new_posts += 1

    def increase_comment(self):
        self.total_comments += 1
        self.new_comments += 1
    