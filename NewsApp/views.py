from flask import render_template
from NewsApp import app
from NewsApp import db
from NewsApp.models import ArtilceDetails
from sqlalchemy import desc



@app.route('/')
def home():
    categories = ["business" ,
                  "entertainment" ,
                  "health" ,
                  "science" ,
                  "sports" ,
                  "technology"]
    articles = []
    for category in categories:
        articles = articles + ArtilceDetails.query.filter_by(category=category)\
                                    .order_by(desc(ArtilceDetails.score)).limit(5).all()

    return render_template('home.html', articles = articles)

@app.route('/business')
def business():

    articles = ArtilceDetails.query.filter_by(category='business')\
                                .order_by(desc(ArtilceDetails.score)).limit(12).all()

    return render_template('business.html', articles = articles)

@app.route('/sports')
def sports():

    articles = ArtilceDetails.query.filter_by(category='sports')\
                                .order_by(desc(ArtilceDetails.score)).limit(12).all()

    return render_template('sports.html', articles = articles)

@app.route('/health')
def health():

    articles = ArtilceDetails.query.filter_by(category='health')\
                                .order_by(desc(ArtilceDetails.score)).limit(12).all()

    return render_template('health.html', articles = articles)

@app.route('/science')
def science():

    articles = ArtilceDetails.query.filter_by(category='science')\
                                .order_by(desc(ArtilceDetails.score)).limit(12).all()

    return render_template('science.html', articles = articles)

@app.route('/technology')
def technology():

    articles = ArtilceDetails.query.filter_by(category='technology')\
                                .order_by(desc(ArtilceDetails.score)).limit(12).all()

    return render_template('technology.html', articles = articles)

@app.route('/entertainment')
def entertainment():

    articles = ArtilceDetails.query.filter_by(category='entertainment')\
                                .order_by(desc(ArtilceDetails.score)).limit(12).all()

    return render_template('entertainment.html', articles = articles)