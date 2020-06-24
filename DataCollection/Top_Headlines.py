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
from langdetect import detect

start_time = time.time()
today = date.today()
today = today.strftime("%b-%d-%Y")
tok = WordPunctTokenizer()
CURR_DIR = os.getcwd()
DATA_PATH = os.path.join(CURR_DIR, 'Data')

newsapi = NewsApiClient(api_key=news_api_key)

"""
Remove the duplicate the articles( using set() or something else)
"""

data = []
page_size = 100
countries = ['in', 'ca', 'au', 'ie', 'us', 'gb', 'za']
names = ['India', 'Canada', 'Australia', 'Ireland', 'United States', 'United Kingdom', 'South Africa']
country_name = dict(zip(countries, names))

print("Collecting News Articles({0}*{1}*{2}) .........".format(len(names), len(categories), page_size))

for country in tqdm(countries, total = len(countries), desc = "countries: "):
	for category in tqdm(categories, total = len(categories), desc = "for "+str(country_name[country])+" : "):
		top_headlines = newsapi.get_top_headlines(category=category,
												  page_size=page_size,
		                                          language='en',
								  		  		  country = country)

		if top_headlines['status']=='ok':
			data = data+ [[	article['publishedAt'],
							article['title'],
							article['description'],
							article['url'],
							article['urlToImage'],
							category,
							article['source']['name'] ]
							for article in tqdm(top_headlines['articles'],
							total = len(top_headlines['articles']),
							desc = "for "+str(category)+" : ")] # text_cleaner(article['content']) ]


news_processed = pd.DataFrame(data = data, columns = ['publishedAt', 'title', 'description', 'url', 'urlToImage', 'category', 'source'])

print()
print("Before Droping NULL values: "+str(news_processed.shape))
print()

news_processed.dropna(axis=0, inplace=True)
news_processed.reset_index(drop=True, inplace=True)

print("After Droping NULL values: "+str(news_processed.shape))
news_processed.to_csv(os.path.join(DATA_PATH, 'Articles-{}.csv'.format(today)))

print()
print("Articles saved to : "+os.path.join(DATA_PATH, 'Articles-{}.csv'.format(today)))
print()
print("Time for collecting and processing Articles : --- %s seconds ---" % (time.time() - start_time))
print()
