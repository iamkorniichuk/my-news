from flask import Blueprint, render_template, redirect, url_for
from my_news.forms import EditAccountForm
from my_news.utils import login_required, logged_user, save_file, USERS_FOLDER
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
    

@users.route('/account/')
@login_required
def me():
    user = logged_user()
    return render_template('user.html', title=user['login'], user=user)


@users.route('/account/edit', methods=['POST', 'GET'])
@login_required
def edit():
    form = EditAccountForm()
    if form.validate_on_submit():
        data={}
        for field in form:
            if not field.data or field.name == 'submit' or field.name == 'csrf_token':
                continue
            if field.name == 'image':
                data['image'] = save_file(field.data, USERS_FOLDER)
                continue
            data[field.name] = field.data
        users_model.update(logged_user()['login'], **data)
        return redirect(url_for('users.me'))
    form.image.data = logged_user()['image']
    form.first_name.data = logged_user()['first_name']
    form.last_name.data = logged_user()['last_name']
    form.description.data = logged_user()['description']
    return render_template('edit_account.html', title='Edit Account', form=form)
