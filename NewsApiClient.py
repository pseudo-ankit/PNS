from newsapi import NewsApiClient
import json
import pandas as pd
import re
import os
from credentials import news_api_key
from nltk.tokenize import WordPunctTokenizer

tok = WordPunctTokenizer()
CURR_DIR = os.getcwd()

newsapi = NewsApiClient(api_key=news_api_key)

top_headlines = newsapi.get_top_headlines(category='sports',
										  page_size=10,
                                          language='en',
                                          country='in')

def text_cleaner(text):
	if text:
		text = re.sub( r'\[[^\]]*\]', " ", text)
		text = re.sub('[^A-Za-z]', " ", text)
		text = text.lower()
		words = [x for x  in tok.tokenize(text) if len(x) > 1]
		return (" ".join(words)).strip()
	else:
		return None

data = []
if top_headlines['status']=='ok':
	'''
	data = [[	article['publishedAt'],
				text_cleaner(article['title']), 
				text_cleaner(article['description']), 
				text_cleaner(article['content']) ]  
				for article in top_headlines['articles']]
	news_processed = pd.DataFrame(data = data, columns = ['publishedAt', 'title', 'description', 'content'])
	news_processed.to_csv('Articles.csv')'''

	for article in top_headlines['articles']:
		data.append(article)
print(len(data))