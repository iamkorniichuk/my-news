from flask import Blueprint, render_template
# from my_news.forms.users import EditForm, CreateForm
from my_news.models.users import users_model


users = Blueprint('users', __name__)


@users.route('/users')
def all():
    allusers = users_model.getallinorder({'key':'login', 'reverse':False})
    return render_template('users.html', title='News', users=allusers)


@users.route('/user/<login>')
def one(login):
    # TODO: To end
    oneuser = users_model.getone(login)
    return render_template('user.html', title=oneuser['login'], user=oneuser)
    