from flask import Blueprint, render_template
# from my_news.forms.posts import EditForm, CreateForm
from my_news.models.posts import posts_model
from my_news.utils import login_required


posts = Blueprint('posts', __name__)


@posts.route('/')
@posts.route('/posts')
def all():
    allposts = posts_model.getallinorder({'key':'posted_time', 'reverse':False})
    return render_template('posts.html', title='News', posts=allposts)


@posts.route('/post/<id>')
def one(id):
    onepost = posts_model.getone(id)
    return render_template('post.html', title=onepost['title'], post=onepost)
