from flask import render_template, flash, redirect, url_for, request
from NewsApp import app, bcrypt
from NewsApp import db
from NewsApp.models import ArticleDetails, ArticleProfile, UserDetails, UserProfile
from NewsApp.forms import RegistrationForm, LoginForm, UpdateAccountForm
from sqlalchemy import desc
from flask_login import login_user, logout_user, current_user, login_required
import secrets
from PIL import Image
import os
from datetime import datetime
from scipy import spatial



now = datetime.now()
datetimeFormat = "%Y-%m-%d %H:%M:%S"
now = now.strftime(datetimeFormat)

@app.route('/')
def home():

    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    categories = ["business" ,
                  "entertainment" ,
                  "health" ,
                  "science" ,
                  "sports" ,
                  "technology"]


    all_articles = ArticleDetails.query.all()
    articles = []
    user_profile = [current_user.profile.business/5, current_user.profile.entertainment/5, current_user.profile.health/5,
                    current_user.profile.science/5, current_user.profile.sports/5, current_user.profile.technology/5]

    for article in all_articles:


        article_profile = [article.profile.business, article.profile.entertainment, article.profile.health,
                            article.profile.science, article.profile.sports, article.profile.technology]

        # profile_score = current_user.profile.business*article.profile.business
        # profile_score += current_user.profile.entertainment*article.profile.entertainment
        # profile_score += current_user.profile.health*article.profile.health
        # profile_score += current_user.profile.science*article.profile.science
        # profile_score += current_user.profile.sports*article.profile.sports
        # profile_score += current_user.profile.technology*article.profile.technology

        profile_score = 1 - spatial.distance.cosine(user_profile, article_profile)

        popularity_score = article.score
        alpha = 0.6

        final_score = alpha*profile_score + (1-alpha)*popularity_score
        articles.append((article, final_score))

    articles.sort(reverse=True, key=(lambda x:x[1]))
    final_list = []

    for i in range(24):
        temp = "2020-07-02T12:48:41Z" #articles[i][0].publishedAt
        temp = temp[0:10] +" "+ temp[11:19]
        diff = datetime.strptime(now, datetimeFormat)\
                - datetime.strptime(temp, datetimeFormat)
        final_list.append((articles[i][0], diff))


    not_found_image = url_for('static', filename='image-not-found.png')

    return render_template('home.html', articles = final_list, title='NewsApp', not_found_image=not_found_image)


@app.route('/business')
def business():

    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    articles = ArticleDetails.query.filter_by(category='business')\
                                .order_by(desc(ArticleDetails.score)).limit(12).all()

    return render_template('business.html', articles = articles)


@app.route('/sports')
def sports():

    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    articles = ArticleDetails.query.filter_by(category='sports')\
                                .order_by(desc(ArticleDetails.score)).limit(12).all()

    return render_template('sports.html', articles = articles)


@app.route('/health')
def health():

    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    articles = ArticleDetails.query.filter_by(category='health')\
                                .order_by(desc(ArticleDetails.score)).limit(12).all()

    return render_template('health.html', articles = articles)


@app.route('/science')
def science():

    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    articles = ArticleDetails.query.filter_by(category='science')\
                                .order_by(desc(ArticleDetails.score)).limit(12).all()

    return render_template('science.html', articles = articles)


@app.route('/technology')
def technology():

    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    articles = ArticleDetails.query.filter_by(category='technology')\
                                .order_by(desc(ArticleDetails.score)).limit(12).all()

    return render_template('technology.html', articles = articles)


@app.route('/entertainment')
def entertainment():

    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    articles = ArticleDetails.query.filter_by(category='entertainment')\
                                .order_by(desc(ArticleDetails.score)).limit(12).all()

    return render_template('entertainment.html', articles = articles)



@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():

        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user_details = UserDetails  (username=form.username.data, email=form.email.data,
                                password=hashed_password, image_file='default.jpg')
        db.session.add(user_details)
        db.session.commit()

        user_profile = UserProfile(business=form.business.data, entertainment=form.entertainment.data, health=form.health.data,
                                    science=form.science.data, sports=form.sports.data, technology=form.technology.data,
                                    details=user_details)
        db.session.add(user_profile)
        db.session.commit()

        flash(f'Account created for {form.username.data}! You can log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title = 'Register', form = form)


@app.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = UserDetails.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            # load the user profile and compute the scores then show them in home page
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please try again', 'danger')
    return render_template('login.html', title = 'Login', form = form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    profile_pic_f_name = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static', 'profile_pics', profile_pic_f_name)

    output_size = (125, 125)
    new_pic = Image.open(form_picture)
    new_pic.thumbnail(output_size)
    new_pic.save(picture_path)

    return profile_pic_f_name



@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.profile_pic.data:
            picture_file = save_picture(form.profile_pic.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account Updated!', 'success')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/'+current_user.image_file)
    return render_template('profile.html', title='Profile',
                            image_file=image_file, form = form)
