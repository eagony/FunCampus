# FunCampus

##### FunCampus是一个简单的大学生交友和互助网站，项目初衷是想改善真人表白墙的一些局限性，例如时效性差，不能实时显示，数量限制，范围较小等等，有完善的用户管理，角色管理，信息流展示，评论，以及后台管理。



- ##### 安装

1. 下载项目

    `git clone https://github.com/eagony/FunCampus.git`
    
    `cd FunCampus`
    
2. 部署后端

    `cd  backend`

    创建虚拟环境

    `python -m venv venv`

    激活虚拟环境

    `venv\Scripts\activate`

    安装依赖

    `pip install -r requirements.txt`

    这里因为flask_uploads导入werkzeug有点小问题,需要将venv\lib\site-packages\flask_uploads.py第26行的

    `from werkzeug import secure_filename, FileStorage`

    改成

```python
    from werkzeug.utils import secure_filename
    from werkzeug.datastructures import FileStorage
```

    同步数据库

    `flask db upgrade`

    部署

    `flask deploy`

    启动

    `flask run`

    测试，打开浏览器输入http://localhost:5000/api/ping如果返回"Pong"则后端启动成功

3. 部署前端

    先安装Node.js，前往 [官方网站](https://nodejs.org/zh-cn/) 下载并安装 `LTS` 版本

    安装好后，由于 `npm` 命令使用的国外镜像，在国内下载依赖包时很慢，这里换成 [淘宝 NPM 镜像](https://npm.taobao.org/)

    `npm install -g cnpm --registry=https://registry.npm.taobao.org`


    `cd front-end`

    安装依赖

    `cnpm install`

    运行前端应用

    `npm run dev`

    浏览器访问: `http://localhost:8080`

ps:注册前修改backend/config.py里的管理员邮箱，注册的时候将自动获得管理员权限。
