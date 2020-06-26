from NewsApp import db
from NewsApp.models import ArticleDetails, ArticleProfile
import os
from datetime import date
import pandas as pd
from tqdm import tqdm

CURR_DIR = os.getcwd()
CURR_DIR = "\\".join(CURR_DIR.split('\\')[:-1])
CURR_DIR = CURR_DIR + "\\DataCollection"
DATA_PATH = os.path.join(CURR_DIR, 'Data')


df_1 = pd.read_csv(os.path.join(DATA_PATH, 'Articles-Evaluated.csv'))
df_1.dropna(axis=0, inplace=True)
df_1.reset_index(drop=True, inplace=True)

df = pd.read_csv(os.path.join(DATA_PATH, 'Articles-Profle.csv'))
df.dropna(axis=0, inplace=True)
df.reset_index(drop=True, inplace=True)

print(df_1.shape)
print(df.shape)

def stream_to_db():

    if(df_1.shape[0]==df.shape[0]):

        num_points = df_1.shape[0]

        for i in tqdm(range(num_points), total = num_points, desc = "Article Details: "):

            title = df_1.loc[i].title
            discription = df_1.loc[i].description
            imageurl = df_1.loc[i].urlToImage
            url = df_1.loc[i].url
            score = df_1.loc[i].score
            publishedAt = str(date.today())     # df_1.loc[i].publishedAt
            category = df_1.loc[i].category

            article_detail = ArticleDetails(title = title, discription = discription, imageurl = imageurl,
                                    url = url, score = score,  publishedAt = publishedAt, category = category)
            db.session.add(article_detail)
            db.session.commit()

            business = df.loc[i].business
            entertainment = df.loc[i].entertainment
            health = df.loc[i].health
            science = df.loc[i].science
            sports = df.loc[i].sports
            technology = df.loc[i].technology

            article_profile = ArticleProfile(business = business, entertainment = entertainment, health = health,
                                        science = science, sports = sports,  technology = technology, details = article_detail)
            db.session.add(article_profile)
            db.session.commit()

    else:
        print("Check the shapes of the csv files!")

stream_to_db()
