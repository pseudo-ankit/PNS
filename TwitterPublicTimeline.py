import tweepy
import sys, os
from tweepy.streaming import StreamListener
import credentials
from TwitterHandles import handles
from nltk.tokenize import WordPunctTokenizer
from bs4 import BeautifulSoup
import re
import pandas as pd
import json

tok = WordPunctTokenizer()
CURR_DIR = os.getcwd()	
DATA_PATH = os.path.join(CURR_DIR, 'Data')

consumer_key = credentials.consumer_key
consumer_secret  = credentials.consumer_secret
access_token = credentials.access_token
access_token_secret = credentials.access_token_secret


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


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

try:
	f = open('handles.json', 'r')
	handles = json.load(f)
except:
	print("Something went wrong when reading from the file: {}".format('handles.json'))
finally:
	f.close()


def tweet_cleaner(text):
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
    words = [x for x  in tok.tokenize(letters_only) if len(x) > 1]
    return (" ".join(words)).strip()


tweets = []
for handle in handles['handles']:
	for tweet in tweepy.Cursor(api.user_timeline, screen_name = handle['screen_name'], since_id = handle['since_id'], tweet_mode='extended').items(2):
			tweets.append([tweet.created_at, tweet_cleaner(tweet.full_text)])
			handle['since_id'] = tweet.id


try:
	f = open('handles.json', 'w')
	handles = json.dump(handles, f, indent = 2)
except:
	print("Something went wrong when writing to the file: {}".format('handles.json'))
finally:
	f.close()


tweets_processed = pd.DataFrame(data = tweets, columns = ['created_at','tweet'])
print(tweets_processed.shape)
tweets_processed.to_csv(os.path.join(DATA_PATH, 'Tweets.csv'))