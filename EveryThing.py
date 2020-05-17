from newsapi import NewsApiClient
#import json
#import pandas as pd
#import re
import os
from credentials import news_api_key

CURR_DIR = os.getcwd()
newsapi = NewsApiClient(api_key=news_api_key)

'''
page_count = 5
counts = []
for i in range(1, page_count+1):
	all_articles = newsapi.get_everything(q='bitcoin',
                                      sources='bbc-news,the-verge',
                                      domains='bbc.co.uk,techcrunch.com',
                                      from_param='2020-05-12',
                                      to='2017-05-14',
                                      language='en',
                                      sort_by='relevancy',
                                      page=i)
	counts.append([len(all_articles['articles'])])

print(counts)
'''
page_count = 5
counts = []
for i in range(1, page_count+1):
	all_articles = newsapi.get_everything(q='bitcoin',
                                      sources='bbc-news,the-verge',
                                      domains='bbc.co.uk,techcrunch.com',
                                      from_param='2020-05-08',
                                      to='2017-05-15',
                                      language='en',
                                      sort_by='relevancy',
                                      page=i)
	counts.append([len(all_articles['articles'])])

print(counts)