from flask import Blueprint, render_template
# from my_news.forms.users import EditForm, CreateForm
from my_news.models.reviews import reviews_model


about = Blueprint('about', __name__)


@about.route('/about')
@about.route('/reviews')
def info():
    allreviews = reviews_model.getallinorder({'key':'stars', 'reverse':True})
    return render_template('about.html', title='About', reviews=allreviews)
    