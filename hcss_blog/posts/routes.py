from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint, current_app)
from flask_login import current_user, login_required
from hcss_blog import db
from hcss_blog.models import Post, User
from hcss_blog.posts.forms import PostForm
from hcss_blog.posts.utils import month_range, send_new_post_email
from hcss_blog.utils import save_picture
import os

posts = Blueprint('posts', __name__)

def tags():
    return get_all_tags()

@posts.route('/student-posts')
def student_posts():
    page = request.args.get('page', 1, type=int)
    posts  = Post.query.join(User).filter(User.role == 'student')\
                        .order_by(Post.date_posted.desc())\
                        .paginate(page=page, per_page=6)
    return render_template('posts.html', posts=posts, title='Student Posts')

@posts.route('/staff_posts')
def staff_posts():
    page = request.args.get('page', 1, type=int)
    posts  = Post.query.join(User).filter(((User.role == 'staff') | (User.role == 'admin')) & (Post.status == 'approved'))\
                        .order_by(Post.date_posted.desc())\
                        .paginate(page=page, per_page=6)
    return render_template('posts.html', posts=posts, title='Staff Posts')

@posts.route("/datetags/<string:date_tag>")
def by_date_tag(date_tag):
    page = request.args.get('page', 1, type=int)
    first_day, last_day = month_range(date_tag)
    posts = Post.query.filter((Post.date_posted >= first_day) \
                             & (Post.date_posted < last_day )\
                             & (Post.status == 'approved'))\
                        .order_by(Post.date_posted.desc())\
                        .paginate(page=page, per_page=6)
    return render_template('datetags.html', posts=posts, date_tag=date_tag)

@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        if form.post_photo.data:
            photo = save_picture(form.post_photo.data)
        else:
            photo = 'no_picture.jpg'

        post = Post(title=form.title.data, content=form.content.data, tags=form.tags.data,
                    post_photo=photo, user_id=current_user.id)
        if (current_user.role == 'admin'):
            post.status = 'approved'
        db.session.add(post)
        db.session.commit()
        send_new_post_email(post)
        flash('Post is created successfully', 'info')
        return redirect(url_for('main.index'))
    return render_template('create_post.html', form=form, title='Create Post')


@posts.route("/post/<int:post_id>",methods=['GET', 'POST'] )
def post(post_id):
    post = Post.query.get_or_404(post_id)
    author = post.author
    posts_by_author = Post.query.join(User).filter((User.id == author.id) & (Post.id != post.id))\
                                .order_by(Post.date_posted.desc()).limit(5)
    if request.method == 'POST':
        if request.form['submit_button'] == 'Approve':
            post.status = 'approved'
            db.session.commit()
            flash('Post is available for public view now!', 'success')
            return redirect(url_for('admin.admin_page'))
        elif request.form['submit_button'] == 'Reject':
            post.status = 'rejected'
            db.session.commit()
            flash('Post will not be available for public view!', 'warning')
            return redirect(url_for('admin.admin_page'))
        elif request.form['submit_button'] == 'Delete':
            db.session.delete(post)
            db.session.commit()
            flash('Post is deleted from the blog successfully', 'success')
            return redirect(url_for('admin.admin_page'))
    elif request.method == 'GET':
        return render_template('post.html', title=post.title, post=post, posts_by_author=posts_by_author)

@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if not (post.author == current_user or current_user.role == 'admin'):
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.tags = form.tags.data
        if form.post_photo.data:
            old_pic = post.post_photo
            photo = save_picture(form.post_photo.data)
            post.post_photo = photo
            # if old_pic != 'no_picture.jpg':
            #     try:
            #         os.remove(os.path.join(current_app.root_path, 'static/images', old_pic))
            #     except:
            #         flash('Associated picture not found!', 'warning')
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.tags.data = post.tags
    return render_template('create_post.html', title='Update Post',
                        form=form, legend='Update Post')

@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if not (post.author == current_user or current_user.role == 'admin'):
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Post is deleted from the blog successfully', 'success')
    return redirect(url_for('main.index'))

@posts.route('/tags/<string:tag>')
def tag_posts(tag):
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter((Post.tags.contains(tag)) & (Post.status=='approved'))\
                    .order_by(Post.date_posted.desc())\
                    .paginate(page=page, per_page=6)
    return render_template('tags.html', posts=posts, tag=tag, title=tag.title())
