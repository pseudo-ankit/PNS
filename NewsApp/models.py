from NewsApp import db

class ArtilceDetails(db.Model):

    artilceId = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    discription = db.Column(db.String(512), nullable=False)
    imageurl = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    score = db.Column(db.Float, nullable=False)
    publishedAt = db.Column(db.DateTime, nullable=False)
    category = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Title %r>' % self.title
