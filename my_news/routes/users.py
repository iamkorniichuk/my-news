from flask import Blueprint, render_template, redirect, url_for
from my_news.forms import EditAccountForm
from my_news.utils.session import login_required, logged_user, add_session_user
from my_news.utils.files import save_file, users_folder, delete_file
from my_news.models.users import users_model
from my_news.models.posts import posts_model


users = Blueprint('users', __name__)


@users.route('/users')
def all():
    users = users_model.getallinorder({'key':'login', 'reverse':False})
    return render_template('users.html', title='News', users=users)


@users.route('/user/<login>')
def one(login):
    # TODO: To end
    user = users_model.getone(login)
    posts = posts_model.getallinorder({'key':'posted_time', 'reverse':False}, user_login=login)
    return render_template('user.html', title=user['login'], user=user, posts=posts)
    

@users.route('/account/')
@login_required
def me():
    oneuser = logged_user()
    return render_template('user.html', title=oneuser['login'], user=oneuser)


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
                delete_file(logged_user()['image'], users_folder())
                data['image'] = save_file(field.data, users_folder())
                continue
            data[field.name] = field.data
        add_session_user(logged_user()['login'])
        users_model.update(logged_user()['login'], **data)
        return redirect(url_for('users.me'))
    form.image.data = logged_user()['image']
    form.first_name.data = logged_user()['first_name']
    form.last_name.data = logged_user()['last_name']
    form.description.data = logged_user()['description']
    return render_template('edit_account.html', title='Edit Account', form=form)


@users.route('/account/delete', methods=['POST'])
@login_required
def delete():
    delete_file(logged_user()['image'], users_folder())
    users_model.delete(logged_user()['login'])
    return redirect(url_for('auth.logout'), code=307)
