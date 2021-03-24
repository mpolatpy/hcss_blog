from flask import Blueprint, render_template, redirect, url_for, abort, flash
from hcss_blog.models import User, Post
from hcss_blog import db
from hcss_blog.admin.forms import AuthorizeUserForm
from flask_login import current_user, login_required
from hcss_blog.admin.utils import send_user_authorization_email

admin = Blueprint('admin', __name__)

@login_required
@admin.route('/admin', methods=['GET', 'POST'])
def admin_page():
    if not current_user.is_authenticated:
        abort(403)
    if current_user.role != 'admin':
        abort(403)
    users = User.query.filter_by(status='pending').order_by(User.username.asc()).all()
    posts = Post.query.filter_by(status='pending').order_by(Post.date_posted.desc()).all()
    all_users = User.query.filter(User.status!='pending').order_by(User.username.asc()).all()
    all_posts = Post.query.filter(Post.status!='pending').order_by(Post.date_posted.desc()).all()
    return render_template('admin.html', title='Admin', all_users=all_users,
                            all_posts=all_posts, users=users, posts=posts)


@login_required
@admin.route('/admin/view_user/<string:user_id>', methods=['GET', 'POST'])
def authorize_user(user_id):
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    if current_user.role != 'admin':
        abort(403)
    user = User.query.filter_by(id=user_id).first()
    form = AuthorizeUserForm()
    form.username.data = user.username
    form.email.data = user.email

    if form.validate_on_submit():
        user.role = form.account_role.data
        user.status = form.status.data
        db.session.commit()
        send_user_authorization_email(user)
        flash('User information is updated!', 'success')
        return redirect(url_for('admin.admin_page'))

    return render_template('approve_user.html', form=form, user=user)
