from datetime import date, timedelta, timezone
from app.api import bp
from app.extensions import db
from app.models import Statistic
from flask import jsonify


def s_today():
    return str(date.today())

def s_yesterday():
    return str(date.today() + timedelta(-1))
           

@bp.route('/statistics', methods=['GET'])
def get_statistics():
    """返回当天的统计数据"""
    statistic = Statistic.query.filter_by(date=s_today()).first()
    if not statistic:
        return 404
    return jsonify(statistic.to_dict())

    
@bp.route('/statistics/view', methods=['GET'])
def increase_view():
    today_statistic = Statistic.query.filter_by(date=s_today()).first()
    if today_statistic:
        today_statistic.increase_view()
    else:
        # 如果没有今天的统计数据则新建
        yesterday_statistic = Statistic.query.filter_by(date=s_yesterday()).first()
        new_statistic = Statistic()
        new_statistic.from_yesterday_statistic(yesterday_statistic)
        new_statistic.increase_view()
        db.session.add(new_statistic)
    db.session.commit()
    return jsonify({'success': 'total_view & new_view + 1'})

    
@bp.route('/statistics/user', methods=['GET'])
def increase_user():
    today_statistic = Statistic.query.filter_by(date=s_today()).first()
    if today_statistic:
        today_statistic.increase_user()
    else:
        # 如果没有今天的统计数据则新建
        yesterday_statistic = Statistic.query.filter_by(date=s_yesterday()).first()
        new_statistic = Statistic()
        new_statistic.from_yesterday_statistic(yesterday_statistic)
        new_statistic.increase_user()
        db.session.add(new_statistic)
    db.session.commit()
    return jsonify({'success': 'total_user & new_user + 1'})

@bp.route('/statistics/post', methods=['GET'])
def increase_post():
    today_statistic = Statistic.query.filter_by(date=s_today()).first()
    if today_statistic:
        today_statistic.increase_post()
    else:
        # 如果没有今天的统计数据则新建
        yesterday_statistic = Statistic.query.filter_by(date=s_yesterday()).first()
        new_statistic = Statistic()
        new_statistic.from_yesterday_statistic(yesterday_statistic)
        new_statistic.increase_post()
        db.session.add(new_statistic)
    db.session.commit()
    return jsonify({'success': 'total_post & new_post + 1'})


@bp.route('/statistics/comment', methods=['GET'])
def increase_comment():
    today_statistic = Statistic.query.filter_by(date=s_today()).first()
    if today_statistic:
        today_statistic.increase_comment()
    else:
        # 如果没有今天的统计数据则新建
        yesterday_statistic = Statistic.query.filter_by(date=s_yesterday()).first()
        new_statistic = Statistic()
        new_statistic.from_yesterday_statistic(yesterday_statistic)
        new_statistic.increase_comment()
        db.session.add(new_statistic)
    db.session.commit()
    return jsonify({'success': 'total_comment & new_comment + 1'})





