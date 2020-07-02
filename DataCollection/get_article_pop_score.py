import pandas as pd
import numpy as np
import re
import os
import warnings

warnings.filterwarnings('ignore')

from bs4 import BeautifulSoup
import nltk

# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

from setting import CURR_DIR
from sklearn import utils
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors
from tqdm import tqdm

# CURR_DIR = os.getcwd()
DATA_PATH = os.path.join(CURR_DIR, 'Data')


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


class GetArticlePopularity():

    def __init__(self, article_file_name, tweets_file_name, top_k=3):

        self.article_file_name = article_file_name
        self.tweets_file_name = tweets_file_name
        self.articles_df = pd.read_csv(os.path.join(DATA_PATH, self.article_file_name))
        self.tweets_df = pd.read_csv(os.path.join(DATA_PATH, self.tweets_file_name))

        self.articles_df.dropna(inplace=True)
        self.articles_df.reset_index(drop=True, inplace=True)
        self.tweets_df.dropna(inplace=True)
        self.tweets_df.reset_index(drop=True, inplace=True)

        self.top_k = top_k

        self.clean_articles = None
        self.clean_tweets = None
        self.clean_text = None
        self.sim = None
        self.pop_list = None
        self.full_article_path = None


    def __text_cleaner(text, source=None):
        if text:
            # Remove all url patterns
            stripped = re.sub(combined_pat, '', text)
            stripped = re.sub(www_pat, '', stripped)
            if source:
                stripped = stripped.replace(source, " ")

            # LowerCase the text data
            lower_case = stripped.lower()

            # Handle the negations
            neg_handled = neg_pattern.sub(lambda x: negations_dic[x.group()], lower_case)

            # Remove all characters except alpha
            letters_only = re.sub("[^a-zA-Z]", " ", neg_handled)

            # Removing stop words and tekenizing the word tokens
            stop_words = set(stopwords.words("english"))
            # word_tokens = word_tokenize(letters_only)
            word_tokens = [x for x  in word_tokenize(letters_only) if len(x) > 1]
            clean_text = [word for word in word_tokens if word not in stop_words]

            #Lemmatize
            lemmatizer = WordNetLemmatizer()
            clean_text = [ lemmatizer.lemmatize(word) for word in clean_text if len(lemmatizer.lemmatize(word))>1]
            return " ".join(clean_text).strip()

    def __get_clean_data(self):

        self.clean_articles = []
        for i in tqdm(self.articles_df.index, desc="Articles: "):
            s = ''
            s = GetArticlePopularity.__text_cleaner(self.articles_df.loc[i].title, self.articles_df.loc[i].source)
            s = s + ' ' + GetArticlePopularity.__text_cleaner(self.articles_df.loc[i].description, self.articles_df.loc[i].source)
            self.clean_articles.append(s.strip())

        self.clean_tweets = []
        for i in tqdm(self.tweets_df.index, desc="Tweets: "):
            self.clean_tweets.append(GetArticlePopularity.__text_cleaner(self.tweets_df.loc[i].tweet.strip()))

        self.clean_text = self.clean_articles + self.clean_tweets
        # return self.clean_text, self.clean_articles, self.clean_tweets

    def query(self, i, k):
        s = ''
        s = self.articles_df.loc[i].title
        s = s + '\n' + self.articles_df.loc[i].description
        print("Queried article:\n", s)
        print()
        print("Top {} Simimlar Tweets: ".format(k))
        for j in np.argsort(sim[i])[-1:-k-1:-1]:
            print(self.clean_tweets[j], self.sim[i][j])

    def __cal_sim(self):

        vectorizer = TfidfVectorizer(min_df = 5) # ngram_range = (1,2)
        vectorizer.fit(self.clean_text)

        article_vec = vectorizer.transform(self.clean_articles)
        article_vec = article_vec.toarray()
        tweet_vec = vectorizer.transform(self.clean_tweets)
        tweet_vec = tweet_vec.toarray()
        self.sim = cosine_similarity(article_vec, tweet_vec)

    def __get_popularity(self):
        self.pop_list = []
        k = self.top_k
        for i in self.articles_df.index:
            val = 0
            for j in np.argsort(self.sim[i])[-1:-k-1:-1]:
                val += self.sim[i][j]
            self.pop_list.append(val/k)
        # return self.pop_list #sorted(pop_list,reverse=True)

    def calculate(self):
        self.__get_clean_data()
        self.__cal_sim()
        self.__get_popularity()
        self.articles_df['score'] = self.pop_list
        self.articles_df.to_csv(os.path.join(DATA_PATH, self.article_file_name), index=False, encoding='utf-8-sig')
        self.full_article_path = os.path.join(DATA_PATH, self.article_file_name)
        print("DONE")
