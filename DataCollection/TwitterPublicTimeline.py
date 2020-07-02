import tweepy
import sys, os
from tweepy.streaming import StreamListener
import credentials
from nltk.tokenize import WordPunctTokenizer
from bs4 import BeautifulSoup
import re
import pandas as pd
import json
from setting import CURR_DIR
from datetime import date
from tqdm import tqdm
from sys import stdout
import warnings
import time
# from TwitterHandles import handles
start_time = time.time()
warnings.filterwarnings("ignore", category=UserWarning, module='bs4') # handlk

today = date.today()
today = today.strftime("%b-%d-%Y")
tok = WordPunctTokenizer()
# CURR_DIR = os.getcwd()
DATA_PATH = os.path.join(CURR_DIR, 'Data')

consumer_key = credentials.consumer_key
consumer_secret  = credentials.consumer_secret
access_token = credentials.access_token
access_token_secret = credentials.access_token_secret


pat1 = r'@[A-Za-z0-9_]+'
pat2 = r'https?://[^ ]+'
combined_pat = r'|'.join((pat1, pat2))
www_pat = r'www.[^ ]+'
negations_dic = {"isn't":"is not", "aren't":"are not", "wasn't":"was not", "weren't":"were not",
                "haven't":"have not","hasn't":"has not","hadn't":"had not","won't":"will not",
                "wouldn't":"would not", "don't":"do not", "doesn't":"does not","didn't":"did not",
                "can't":"can not","couldn't":"could not","shouldn't":"should not","mightn't":"might not",
                "mustn't":"must not"}
neg_pattern = re.compile(r'\b(' + '|'.join(negations_dic.keys()) + r')\b')





class CollectTweets():

    def __init__(self, number_tweets=3000):

        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(self.auth)

        self.number_tweets = number_tweets
        self.tweets = []
        self.tweets_processed = None
        self.tweets_file_name = 'Tweets-{}.csv'.format(today)

    def __tweet_cleaner(text, screen_name):
        soup = BeautifulSoup(text, 'html.parser')
        souped = soup.get_text()
        try:
            bom_removed = souped.decode("utf-8-sig").replace(u"\ufffd", "?")
        except:
            bom_removed = souped
        stripped = re.sub(combined_pat, '', bom_removed)
        stripped = re.sub(www_pat, '', stripped)
        lower_case = stripped.lower()
        neg_handled = neg_pattern.sub(lambda x: negations_dic[x.group()], lower_case)
        letters_only = re.sub("[^a-zA-Z]", " ", neg_handled)
        letters_only = letters_only.replace(screen_name, " ")
        words = [x for x  in tok.tokenize(letters_only) if len(x) > 1]
        return (" ".join(words)).strip()


    def collect(self):

        f = open(os.path.join(CURR_DIR, 'handles.json'), 'r')
        handles = json.load(f)
        f.close()

        print("Collecting tweets({0}*{1}) .........".format(len(handles['handles']), self.number_tweets))

        for handle in tqdm(handles['handles'], total = len(handles['handles']), desc = "handles:  "):
            for tweet in tqdm(tweepy.Cursor(self.api.user_timeline, screen_name = handle['screen_name'], since_id = handle['since_id'], tweet_mode='extended').items(self.number_tweets), total = self.number_tweets, desc='from '+str(handle['screen_name'])+' : ', file = stdout):
                self.tweets.append([tweet.created_at, CollectTweets.__tweet_cleaner(tweet.full_text, handle['screen_name'])])
                handle['since_id'] = tweet.id

        f = open(os.path.join(CURR_DIR, 'handles.json'), 'w')
        handles = json.dump(handles, f, indent = 2)
        f.close()

        self.tweets_processed = pd.DataFrame(data = self.tweets, columns = ['created_at','tweet'])
        print()
        print("Before Droping NULL values: "+str(self.tweets_processed.shape))
        print()

        self.tweets_processed.dropna(axis=0, inplace=True)
        self.tweets_processed.reset_index(drop=True, inplace=True)
        self.tweets_processed.to_csv(os.path.join(DATA_PATH, self.tweets_file_name), index=False, encoding='utf-8-sig')

        print("Tweets saved to : "+os.path.join(DATA_PATH, self.tweets_file_name))
        print()
        print("Time for collecting and processing tweets : --- %s seconds ---" % (time.time() - start_time))
        print()
        print("After Droping NULL values: "+str(self.tweets_processed.shape))
