from NewsApp import app, db
from NewsApp.models import ArticleDetails, ArticleProfile

@app.shell_context_processor
def make_shell_context():
    return {'db': db,
            'ArticleDetails':ArticleDetails,
            'ArticleProfile':ArticleProfile}
