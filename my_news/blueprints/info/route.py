import base64
from io import BytesIO
from flask import Blueprint, render_template, jsonify
import my_news.db.models as models
from my_news.utils.session import logged_user
import matplotlib.pyplot as plot
import numpy


info = Blueprint('info', __name__)


@info.route('/getshort', methods=['POST'])
@logged_user.admin_required
def getshort():
    info = {}
    info['Users'] = f'{models.users.count()} registered'
    info['News'] = f'{models.news.count()} published'
    info['Comments'] = f'{models.comments.count()} posted'
    info['Reviews'] = f'{models.reviews.count()} written'
    return jsonify({'html': render_template('modules/info_cards.html', info=info)})


@info.route('/getfull', methods=['POST'])
@logged_user.admin_required
def getfull():
    info = []
    info.append(news_bar())
    info.append(comments_bar())
    info.append(reviews_bar())
    return jsonify({'html': render_template('modules/info_full.html', info=info)})


def news_bar():
    figure = plot.figure()

    all_users = models.users.getall(is_admin=1)
    authors = []
    count = []
    for user in all_users:
        authors.append(user['login'])
        count.append(models.news.count(user_login=user['login']))

    plot.bar(authors, count)
    if count:
        plot.yticks(numpy.arange(min(count), max(count) + 1, 1))
    plot.title('News count')
    plot.xlabel('Authors')
    plot.ylabel('Counts')

    temp = BytesIO()
    figure.savefig(temp, format='png')
    return base64.b64encode(temp.getvalue()).decode('utf-8')


def comments_bar():
    figure = plot.figure()

    all_users = models.users.getall()
    authors = []
    count = []
    for user in all_users:
        amount = models.comments.count(user_login=user['login'])
        if amount > 0:
            authors.append(user['login'])
            count.append(amount)

    plot.bar(authors, count)
    if count:
        plot.yticks(numpy.arange(min(count), max(count) + 1, 1))
    plot.title('Comments count')
    plot.xlabel('Authors')
    plot.ylabel('Counts')

    temp = BytesIO()
    figure.savefig(temp, format='png')
    return base64.b64encode(temp.getvalue()).decode('utf-8')


def reviews_bar():
    figure = plot.figure()

    stars_range = [1, 2, 3, 4, 5]
    count = []
    for i in stars_range:
        amount = models.reviews.count(stars=i)
        count.append(amount)

    plot.bar(stars_range, count)
    if count:
        plot.yticks(numpy.arange(min(count), max(count) + 1, 1))
    plot.title('Star rating')
    plot.xlabel('Stars')
    plot.ylabel('Count')

    temp = BytesIO()
    figure.savefig(temp, format='png')
    return base64.b64encode(temp.getvalue()).decode('utf-8')
