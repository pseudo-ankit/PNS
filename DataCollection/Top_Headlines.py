from newsapi import NewsApiClient
from NewsCategories import categories
import json
import pandas as pd
import re
import os
from tqdm import tqdm
from credentials import news_api_key
from nltk.tokenize import WordPunctTokenizer
from datetime import date
import time
from setting import CURR_DIR
from langdetect import detect

start_time = time.time()
today = date.today()
today = today.strftime("%b-%d-%Y")
tok = WordPunctTokenizer()
# CURR_DIR = os.getcwd()
# CURR_DIR = os.path.join()
DATA_PATH = os.path.join(CURR_DIR, 'Data')



class CollectArtilces():

	def __init__(self, page_size=100):

		self.newsapi = NewsApiClient(api_key=news_api_key)

		self.data = []
		self.unique_titles = set()
		self.page_size = page_size
		self.countries = ['in', 'ca', 'au', 'ie', 'us', 'gb', 'za']
		self.names = ['India', 'Canada', 'Australia', 'Ireland', 'United States', 'United Kingdom', 'South Africa']
		self.country_name = dict(zip(self.countries, self.names))
		self.articles_file_name = 'Articles_Details-{}.csv'.format(today)


	def collect(self):

		print("Collecting News Articles({0}*{1}*{2}) .........".format(len(self.names), len(categories), self.page_size))

		for country in tqdm(self.countries, total = len(self.countries), desc = "countries: "):
			for category in tqdm(categories, total = len(categories), desc = "for "+str(self.country_name[country])+" : "):
				top_headlines = self.newsapi.get_top_headlines(category=category, page_size=self.page_size, language='en', country = country)

				if top_headlines['status']=='ok':
					for article in tqdm(top_headlines['articles'], total = len(top_headlines['articles']),desc = "for "+str(category)+" : "):

							if article['title'] not in self.unique_titles:
								self.unique_titles.add(article['title'])
								self.data.append([	article['publishedAt'],
												article['title'],
												article['description'],
												article['url'],
												article['urlToImage'],
												category,
												article['source']['name']])


		news_processed = pd.DataFrame(data = self.data, columns = ['publishedAt', 'title', 'description', 'url', 'urlToImage', 'category', 'source'])

		print()
		print("Before Droping NULL values: "+str(news_processed.shape))
		print()

		news_processed.dropna(axis=0, inplace=True)
		news_processed.reset_index(drop=True, inplace=True)

		print("After Droping NULL values: "+str(news_processed.shape))
		news_processed.to_csv(os.path.join(DATA_PATH, self.articles_file_name), index=False, encoding='utf-8-sig')

		print()
		print("Articles saved to : "+os.path.join(DATA_PATH, self.articles_file_name))
		print()
		print("Time for collecting and processing Articles : --- %s seconds ---" % (time.time() - start_time))
		print()
