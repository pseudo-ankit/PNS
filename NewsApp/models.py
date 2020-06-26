from NewsApp import db

class ArticleDetails(db.Model):

    articleId = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    discription = db.Column(db.String(512), nullable=False)
    imageurl = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    score = db.Column(db.Float, nullable=False)
    publishedAt = db.Column(db.DateTime, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    profile = db.relationship('ArticleProfile', backref='details', uselist=False)

    def __repr__(self):
        return '<Title %r>' % self.title


class ArticleProfile(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    business = db.Column(db.Float, nullable=False)
    entertainment = db.Column(db.Float, nullable=False)
    health = db.Column(db.Float, nullable=False)
    science = db.Column(db.Float, nullable=False)
    sports = db.Column(db.Float, nullable=False)
    technology = db.Column(db.Float, nullable=False)
    articleId = db.Column(db.Integer, db.ForeignKey('article_details.articleId'), nullable=False)

    def __repr__(self):
        return '<Id %r>' % self.articleId

#
# class UserDetails(db.Model):
#
#     userId = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(20), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
#     password = db.Column(db.String(60), nullable=False)
#     portfolio = db.relationship('UserPortfolio', backref='details', uselist=False)
#
#     def __repr__(self):
#         return '<User: %r>' % self.username
#
#
# class UserPortfolio(db.Model):
#
#     business = db.Column(db.Float, nullable=False)
#     entertainment = db.Column(db.Float, nullable=False)
#     health = db.Column(db.Float, nullable=False)
#     science = db.Column(db.Float, nullable=False)
#     sports = db.Column(db.Float, nullable=False)
#     technology = db.Column(db.Float, nullable=False)
#     userId = db.Column(db.Integer, db.ForeignKey('userdetails.userId'), nullable=False)
#
#     def __repr__(self):
#         return '<Id %r>' % self.userId
