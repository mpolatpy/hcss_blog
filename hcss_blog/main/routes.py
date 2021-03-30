from flask import render_template, request, Blueprint, flash, redirect
from hcss_blog.models import Post
from datetime import datetime, timedelta

main = Blueprint('main', __name__)

@main.before_request
def before_request():
    if request.is_secure:
        return

    url = request.url
    if request.url.startswith('http://'):
        url = request.url.replace('http', 'https', 1)
    elif not 'https://' in url:
        url = f"https://{request.url}"

    return redirect(url, code=301)

@main.route('/')
@main.route('/home')
def index():
    page = request.args.get('page', 1, type=int)
    posts  = Post.query.filter_by(status='approved')\
                        .order_by(Post.date_posted.desc())\
                        .paginate(page=page, per_page=6)
    # posts = Post.query.order_by(Post.date_posted.desc()).limit(4)
    return render_template('index.html', posts=posts, title='Home Page')
