from newsapi import NewsApiClient
import json
import pandas as pd
import re
import os
from credentials import news_api_key

CURR_DIR = os.getcwd()
newsapi = NewsApiClient(api_key=news_api_key)
sources = newsapi.get_sources()

sources_dic = {}
nation_list = []
for source in sources['sources']:
	if source['language'] == 'en':
		if source['country'] in sources_dic:
			sources_dic[source['country']]+=1
		else:
			sources_dic[source['country']]=1
	if source['country']=='in':
		nation_list.append(source['name'])
print(len(sources_dic))
print(sources_dic)
print(len(nation_list))
print(nation_list)