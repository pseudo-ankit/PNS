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

def text_cleaner(text):
	if text:
		stripped = re.sub(combined_pat, '', text)
	    stripped = re.sub(www_pat, '', stripped)
	    lower_case = stripped.lower()
	    neg_handled = neg_pattern.sub(lambda x: negations_dic[x.group()], lower_case)
	    letters_only = re.sub("[^a-zA-Z]", " ", neg_handled)
	    letters_only.replace()
	    words = [x for x  in tok.tokenize(letters_only) if len(x) > 1]
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