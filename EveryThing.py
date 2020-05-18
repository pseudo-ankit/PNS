from newsapi import NewsApiClient
#import json
#import pandas as pd
#import re
import os
from credentials import news_api_key

CURR_DIR = os.getcwd()
newsapi = NewsApiClient(api_key=news_api_key)

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



# page_count = 5
# counts = []
# for i in range(1, page_count+1):
# 	all_articles = newsapi.get_everything(q='bitcoin',
#                                       sources='bbc-news,the-verge',
#                                       domains='bbc.co.uk,techcrunch.com',
#                                       from_param='2020-05-12',
#                                       to='2017-05-14',
#                                       language='en',
#                                       sort_by='relevancy',
#                                       page=i)
# 	counts.append([len(all_articles['articles'])])

# print(counts)

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