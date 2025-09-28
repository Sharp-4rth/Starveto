from flask import render_template,  url_for, redirect, request, flash
from app import app
from app.models import User
from app.forms import PostcodeForm, LoginForm, ChangePasswordForm, RegisterForm, ChangeEmailForm
from flask_login import current_user, login_user, logout_user, login_required, fresh_login_required
import sqlalchemy as sa
from app import db
from urllib.parse import urlsplit
from selenium.common import TimeoutException
from app.gather_restaurants import gather_data


@app.route('/', methods=['POST', 'GET'])
def home():
    form = PostcodeForm()
    above_search = None

    # If the user is logged in, show their saved postcode above the form.
    if current_user.is_authenticated:
        above_search = "Postcode: " + current_user.get_postcode()
        print(current_user.get_postcode())

    # If redirected here due to an error, show the error message instead.
    if error_message := request.args.get('error_message'):
        above_search = error_message

    if form.validate_on_submit():
        postcode = form.postcode.data
        print("".join(postcode.strip().split(" ")), len("".join(postcode.strip().split(" "))))
        if len("".join(postcode.strip().split(" "))) >= 5:
            # current_user.set_postcode(postcode)
            return redirect(url_for('fastest_restaurants', postcode=postcode, above_search=above_search))
        else:
            above_search = "Please enter a valid postcode."
            print("wrong postcode")

    return render_template('index.html', form=form, title="Starveto!", restaurants_times=[], above_search=above_search)

@app.route('/fastest_restaurants', methods=['POST', 'GET'])
def fastest_restaurants():
    restaurants_times = []
    form = PostcodeForm()
    postcode = ""
    if current_user.is_authenticated:
        postcode = current_user.get_postcode()
    else:
        postcode = request.args.get('postcode')
    # if not postcode:  # Handle case where postcode is None
    #     flash('No postcode provided. Please enter a valid postcode.', 'danger')
    #     return redirect(url_for('home'))
    try:
        # restaurants_times = [{"McDonald's": 20.2}, {"WaitRose": 10}, {"Pizza Hut": 15.5}, {"Rudy's": 15.5}, {"Molly's": 4.00}]
        restaurants_times = gather_data(postcode)
        # print("after gathering data")
        for item in restaurants_times:
            for k, value in item.items():
                item[k] = f"will deliver in about {int(value)} minutes"
    except Exception as e:
        error_message = f"Unable to gather data right now. Please try again. "
        return redirect(url_for('home', error_message=error_message))

    return render_template('fastest_restaurants.html', restaurants_times=restaurants_times, title="Starveto!", postcode=postcode)

@app.route("/account")
@login_required
def account():
    return render_template('account.html', title="Account")

@app.route('/login', methods=['GET', 'POST'])
def login():
    # If the user is already logged in, redirect them to the homepage.
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()

    # When the login form is submitted, validate the credentials.
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':

            next_page = url_for('home')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/change_pw', methods=['GET', 'POST'])
@fresh_login_required
def change_pw():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        current_user.set_password(form.new_password.data)
        db.session.commit()
        flash('Password changed successfully', 'success')
        return redirect(url_for('home'))
    return render_template('change_pw.html', title='Change Password', form=form)

@app.route('/change_email', methods=['GET', 'POST'])
@fresh_login_required
def change_email():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        current_user.email = form.new_email.data
        db.session.commit()
        flash('Email changed successfully', 'success')
        return redirect(url_for('home'))
    return render_template('generic_form.html', title='Change Email', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data, postcode=form.postal.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

# Error handler for 403 Forbidden
@app.errorhandler(403)
def error_403(error):
    return render_template('errors/403.html', title='Error'), 403

# Handler for 404 Not Found
@app.errorhandler(404)
def error_404(error):
    return render_template('errors/404.html', title='Error'), 404

@app.errorhandler(413)
def error_413(error):
    return render_template('errors/413.html', title='Error'), 413

# 500 Internal Server Error
@app.errorhandler(500)
def error_500(error):
    return render_template('errors/500.html', title='Error'), 500