from NewsApp import db, app
from NewsApp.models import ArticleDetails, ArticleProfile
import os
from os import walk
import glob
import json
from NewsApp.setting import CURR_DIR
from datetime import date
import pandas as pd
from tqdm import tqdm

# path = os.getcwd()
# CURR_DIR = os.path.dirname(path)
# CURR_DIR = os.path.join(CURR_DIR, 'DataCollection')
DATA_PATH = os.path.join(os.path.dirname(CURR_DIR), 'DataCollection', 'Data')

try:
    f = open(os.path.join(CURR_DIR, 'last_used_csv.json'), 'r')
    all_used_csv = json.load(f)
except:
    print("Something went wrong when reading from the file: {}".format('last_used_csv.json'))
finally:
    f.close()


all_csv_files = []
for (dirpath, dirnames, filenames) in walk(DATA_PATH):
    for filename in filenames:
        _, file_extension = os.path.splitext(os.path.join(DATA_PATH, filename))
        if file_extension == '.csv':
            all_csv_files.append(filename)
    break


new_csv_files = {'details':[], 'profile':[]}


for csv_file in all_csv_files:

    if csv_file not in all_used_csv['details']:
        if 'Details' in csv_file:
            print(csv_file)
            new_csv_files['details'].append(csv_file)
            all_used_csv['details'].append(csv_file)

    if csv_file not in all_used_csv['profile']:
        if 'Profile' in csv_file:
            print(csv_file)
            new_csv_files['profile'].append(csv_file)
            all_used_csv['profile'].append(csv_file)


try:
	f = open(os.path.join('last_used_csv.json'), 'w')
	json.dump(all_used_csv, f, indent = 2)
except:
	print("Something went wrong when writing to the file: {}".format('last_used_csv.json'))
finally:
	f.close()


class StreamToDb():

    def __init__(self):

        self.new = True
        if len(new_csv_files['details']) and len(new_csv_files['profile']):

            self.df_1 = pd.concat([pd.read_csv(os.path.join(DATA_PATH, new_csv)) for new_csv in new_csv_files['details']])
            # self.df_1 = pd.read_csv(os.path.join(DATA_PATH, 'Articles-Evaluated.csv'))
            self.df_1.dropna(axis=0, inplace=True)
            self.df_1.reset_index(drop=True, inplace=True)

            self.df = pd.concat([pd.read_csv(os.path.join(DATA_PATH, new_csv)) for new_csv in new_csv_files['profile']])
            # self.df = pd.read_csv(os.path.join(DATA_PATH, 'Articles-Profle.csv'))
            self.df.dropna(axis=0, inplace=True)
            self.df.reset_index(drop=True, inplace=True)

            if len(self.df_1)==0 or len(self.df)==0:
                self.new=False
        else:
            self.new = False


    def stream_to_db(self):

        if self.new:

            if(self.df_1.shape[0]==self.df.shape[0]) and len(self.df_1) and len(self.df):

                num_points = self.df_1.shape[0]

                for i in tqdm(range(num_points), total = num_points, desc = "Updating the DataBase: "):

                    title = self.df_1.loc[i].title
                    discription = self.df_1.loc[i].description
                    imageurl = self.df_1.loc[i].urlToImage
                    url = self.df_1.loc[i].url
                    score = self.df_1.loc[i].score
                    publishedAt = str(date.today())     # self.df_1.loc[i].publishedAt
                    category = self.df_1.loc[i].category

                    article_detail = ArticleDetails(title = title, discription = discription, imageurl = imageurl,
                                            url = url, score = score,  publishedAt = publishedAt, category = category)
                    db.session.add(article_detail)
                    db.session.commit()

                    business = self.df.loc[i].business
                    entertainment = self.df.loc[i].entertainment
                    health = self.df.loc[i].health
                    science = self.df.loc[i].science
                    sports = self.df.loc[i].sports
                    technology = self.df.loc[i].technology

                    article_profile = ArticleProfile(business = business, entertainment = entertainment, health = health,
                                                science = science, sports = sports,  technology = technology, details = article_detail)
                    db.session.add(article_profile)
                    db.session.commit()

            else:
                print("Number of rows not same in the csv files!")
        else:
            print('No new Files Datected!')
