from flask import Blueprint, render_template, redirect, url_for
import my_news.db.models as models
from my_news.utils.session import logged_user


pages = Blueprint('pages',  __name__)


@pages.route('/')
@pages.route('/news')
def news():
    return render_template('pages/news.html', title='News')


@pages.route('/news/<int:id>')
def one_news(id):
    return render_template('pages/one_news.html', title='News', id=id)


@pages.route('/users')
def users():
    return render_template('pages/users.html', title='Users')


@pages.route('/user/<login>')
def user(login):
    if login == logged_user.info['login']:
        return redirect(url_for('pages.account'))
    name = models.users.getone(login)['login']
    return render_template('pages/user.html', title=name, login=login)


@pages.route('/account')
def account():
    login = logged_user.info['login']
    return render_template('pages/user.html', title='Account', login=login)


@pages.route('/about')
def about():
    return render_template('pages/about.html', title='About')


@pages.route('/history')
def history():
    return render_template('pages/history.html', title='History')


@pages.route('/info')
@logged_user.admin_required
def info():
    return render_template('pages/info.html', title='Info')
