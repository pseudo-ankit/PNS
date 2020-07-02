from Top_Headlines import CollectArtilces
obj = CollectArtilces(page_size=100) # MAX LIMIT 100
obj.collect()

from TwitterPublicTimeline import CollectTweets
obj1 = CollectTweets(number_tweets=3000) # MAX LIMIT 3000
obj1.collect()

# print(obj.articles_file_name)
# print(obj1.tweets_file_name)

from get_article_pop_score import GetArticlePopularity
obj2 = GetArticlePopularity(self.articles_file_name, self.tweets_file_name)
obj2.calculate()

from get_article_profile import GetArticleProfile
obj3 = GetArticleProfile(self.articles_file_name)
obj3.calculate()

# print(obj2.full_article_path)
# print(obj3.full_article_path_profile)
