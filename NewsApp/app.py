from NewsApp import app, db
from NewsApp.models import ArticleDetails, ArticleProfile, UserDetails, UserProfile
# import argparse
#
# parser = argparse.ArgumentParser()
# parser.add_argument('--new_app', help='True --> setup new app Flase --> updating the files',
#                     choices=['True', 'False'])
#
# arg = parser.parse_args()
# print(arg.new_app)


@app.shell_context_processor
def make_shell_context():
    return {'db': db,
            'ArticleDetails':ArticleDetails,
            'ArticleProfile':ArticleProfile,
            'UserDetails':UserDetails,
            'UserProfile':UserProfile,}
