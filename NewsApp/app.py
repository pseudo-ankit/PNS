from NewsApp import app, db
from NewsApp.models import ArtilceDetails

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'ArtilceDetails':ArtilceDetails}
