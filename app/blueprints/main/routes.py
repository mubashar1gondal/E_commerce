from app import db
from flask import render_template, request, redirect, url_for, flash
from app.blueprints.main import bp as main
from app.models import Post
from app.blueprints.authentication.models import User
from flask_login import login_user, logout_user, current_user, login_required



@main.route('/', methods=['GET', 'POST'])
@login_required
def home():
    # print("Current User:", current_user.is_authenticated)
    # print("Current User:", current_user.is_active)
    # print("Current User:", current_user.is_anonymous)
    # print("Current User:", current_user.get_id())
    if request.method == 'POST':
        p = Post(body=request.form.get('body_text'), user_id=current_user.get_id())
        db.session.add(p)
        db.session.commit()
        flash('Blog post created successfully', 'info')
        return redirect(url_for('main.home'))
    context = {
        'posts': current_user.followed_posts().all()
    }
    return render_template('index.html', **context)

@main.route('/explore')
@login_required
def explore():
    return render_template('explore.html', users=[u for u in User.query.all() if u.id != current_user.id])
 
@main.route('/unfollow')
@login_required
def unfollow():
    u = User.query.get(request.args.get('user_id'))
    current_user.unfollow(u)
    flash(f'You have unfollowed {u.first_name} {u.last_name} [{u.email}]', 'secondary')
    return redirect(url_for('main.explore'))

@main.route('/follow')
@login_required
def follow():
    u = User.query.get(request.args.get('user_id'))
    current_user.follow(u)
    flash(f'You have followed {u.first_name} {u.last_name} [{u.email}]', 'success')
    return redirect(url_for('main.explore'))

@main.route('/contact')
def contact():

    return render_template('contact.html')


@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        user = User.query.get(current_user.id)
        if user is not None:
            user.first_name = request.form.get('first_name')
            user.last_name = request.form.get('last_name')
            user.set_email()


            if request.form.get('password') and request.form.get('confirm_password') and request.form.get('password') == request.form.get('confirm_password'):
                user.password = request.form.get('password')
            elif not request.form.get('password') and not request.form.get('confirm_password'):
                pass
            else:
                flash('There was an issue updating your information. Please try again.', 'warning')
                return redirect(url_for('main.profile'))
            db.session.commit()
            flash('User updated successfully', 'success')
            return redirect(url_for('main.profile'))
    return render_template('profile.html')