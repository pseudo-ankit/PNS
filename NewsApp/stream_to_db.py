from NewsApp import db
from NewsApp.models import ArtilceDetails
import os
from datetime import date
import pandas as pd

CURR_DIR = os.getcwd()
CURR_DIR = "\\".join(CURR_DIR.split('\\')[:-1])
CURR_DIR = CURR_DIR + "\\DataCollection"
DATA_PATH = os.path.join(CURR_DIR, 'Data')


df = pd.read_csv(os.path.join(DATA_PATH, 'Articles-Evaluated.csv'))
df.dropna(axis=0, inplace=True)
df.reset_index(drop=True, inplace=True)
print(df.shape)

def stream_to_db():
    # print(df.index)
    # max_n = 20
    for i in df.index:
        print(i)
        # if(i>=max_n):
        #     break
        title = df.loc[i].title
        discription = df.loc[i].description
        imageurl = df.loc[i].urlToImage
        url = df.loc[i].url
        score = df.loc[i].score
        publishedAt = str(date.today())     # df.loc[i].publishedAt
        category = df.loc[i].category[0:10]

        datum = ArtilceDetails(title = title, discription = discription, imageurl = imageurl, url = url, score = score,  publishedAt = publishedAt, category = category)
        db.session.add(datum)
        db.session.commit()

stream_to_db()
