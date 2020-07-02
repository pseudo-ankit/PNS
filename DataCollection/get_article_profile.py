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
from datetime import date

# CURR_DIR = os.getcwd()
DATA_PATH = os.path.join(CURR_DIR, 'Data')
today = date.today()
today = today.strftime("%b-%d-%Y")

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


class GetArticleProfile():

    def __init__(self, article_file_name):

        self.article_file_name = article_file_name
        self.articles_df = pd.read_csv(os.path.join(DATA_PATH, self.article_file_name))
        self.articles_df.dropna(inplace=True)
        self.articles_df.reset_index(drop=True, inplace=True)
        self.article_file_name_profile = 'Articles_Profile-{}.csv'.format(today)

        self.clean_articles = None
        self.clean_articles_vector = None
        self.model_knn = None
        self.articles_profile_list = None
        self.full_article_path_profile = None


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
            s = GetArticleProfile.__text_cleaner(self.articles_df.loc[i].title, self.articles_df.loc[i].source)
            s = s + ' ' + GetArticleProfile.__text_cleaner(self.articles_df.loc[i].description, self.articles_df.loc[i].source)
            self.clean_articles.append(s.strip())

        # return self.clean_articles

    def __cal_sim(self):

        vectorizer = TfidfVectorizer(min_df = 5) # ngram_range = (1,2)
        vectorizer.fit(self.clean_articles)

        self.clean_articles_vector = vectorizer.transform(self.clean_articles)
        self.clean_articles_vector = self.clean_articles_vector.toarray()
        self.model_knn = NearestNeighbors(metric = "cosine", algorithm = "brute")
        self.model_knn.fit(self.clean_articles_vector)

    def __get_profile(self):
        category_to_index = [ "business" ,
                              "entertainment" ,
                              "health" ,
                              "science" ,
                              "sports" ,
                              "technology"]
        self.articles_profile_list = []

        for query_index in range(len(self.clean_articles)):
            distances, indices = self.model_knn.kneighbors(self.clean_articles_vector[query_index].reshape(1, -1), n_neighbors = 11)
            profile_score = [0]*6

            for i in range(1, len(distances.flatten())):
                category = self.articles_df.loc[indices.flatten()[i]].category
                index = category_to_index.index(category)
                profile_score[index] += 1-distances.flatten()[i]
            self.articles_profile_list.append(profile_score)

        # return self.pop_list #sorted(pop_list,reverse=True)

    def calculate(self):
        self.__get_clean_data()
        self.__cal_sim()
        self.__get_profile()
        df = pd.DataFrame(self.articles_profile_list, columns = ['business', 'entertainment', 'health', 'science', 'sports', 'technology'])
        df.to_csv(os.path.join(DATA_PATH, self.article_file_name_profile), index=False, encoding='utf-8-sig')
        self.full_article_path_profile = os.path.join(DATA_PATH, self.article_file_name_profile)
