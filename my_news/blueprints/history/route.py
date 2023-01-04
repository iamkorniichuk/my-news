from flask import Blueprint, render_template, request, jsonify, json
import my_news.db.models as models


history = Blueprint('history', __name__)


@history.route('/get', methods=['POST'])
def get():
    ids = request.form['history']
    if ids:
        all_history = []
        for id in json.loads(ids):
            news = models.news.appendone_getone(models.news.getone(id), models.users, ['user_login', 'login'])
            if news:
                all_history.append(news)
        all_history.reverse()
        return jsonify({'html': render_template('modules/news_covers.html', news=all_history)})
    else:
        return jsonify({'html': render_template('modules/error.html', message='No news in history yet')})