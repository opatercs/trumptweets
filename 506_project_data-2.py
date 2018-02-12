import json
import unittest 

#Twitter Data
#Data collected and cached process modeled after the sample_twitter.py file
twitter_ref = open("twitter_recent_tweets.txt", "r")
twitter_str = twitter_ref.read()
twitter_data = json.loads(twitter_str)


#New York Times Data
#Data collected and cached from the API Tool from http://developer.nytimes.com/ and saved into a file called "nyt_all_sections"
nyt_ref = open("nyt_recent_articles.txt","r")
nyt_str = nyt_ref.read()
nyt_data = json.loads(nyt_str)


#positive and negative words list to compare text and titles to
pos_ws = []
f = open('positive-words.txt', 'r')

for l in f.readlines()[35:]:
    pos_ws.append(unicode(l.strip()))
f.close()

neg_ws = []
f = open('negative-words.txt', 'r')
for l in f.readlines()[35:]:
    neg_ws.append(unicode(l.strip()))


#class to create instances of the NYT articles
class Article():
	def __init__ (self, nyt_data={}): 
		self.title = nyt_data['title']
		self.author = nyt_data['byline']
		self.url = nyt_data['url']
		self.date = nyt_data['published_date']
		self.topic = nyt_data['des_facet'] 
		self.section = nyt_data['section']
		self.abstract = nyt_data['abstract']
 
	def trump_mentions(self):
		if "Trump" in self.title:
			return True

	def most_positive(self):
		pos_total = {}
		split = self.title.lower().split()
		for word in split:
			if word in pos_ws:
				if word not in pos_total:
					pos_total[word] = 1
				else:
					pos_total[word] += 1
		return pos_total

	def most_negative(self):
		neg_total = {}
		split = self.title.lower().split()
		for word in split:
			if word in neg_ws:
				if word not in neg_total:
					neg_total[word] = 1
				else:
					neg_total[word] += 1
		return neg_total
    

#Create a list of article instances
def article_lst(nyt_data):
	art_lst = []
	for item in nyt_data['results']:
		article = Article(item) 
		art_lst.append(article)
	return art_lst
	

#class to create instances of recent Tweets from the NYTimes page
class Tweet:
	def __init__(self, twitter_data={}): 
		if 'text' in twitter_data:
			self.text = twitter_data['text']
		else:
			self.text = ''

		if 'retweet_count' in twitter_data:
			self.retweets = twitter_data['retweet_count']
		else:
			self.retweets = ''

		if 'favorite_count' in twitter_data:
			self.favorited = twitter_data['favorite_count']
		else:
			self.favorited = ''

		if 'created_at' in twitter_data:
			self.date = twitter_data['created_at']
		else:
			self.date = ''

		if 'urls' in twitter_data:
			self.url = twitter_data['entities']['url'][0]
		else:
			self.url = ''


	def popularity(self):
		pop = self.retweets + self.favorited
		return pop

	def trump_mentions(self):
		if "Trump" in self.text:
			return True

	def most_positive(self):
		pos_total = {}
		split = self.text.lower().split()
		for word in split:
			if word in pos_ws:
				if word not in pos_total:
					pos_total[word] = 1
				else:
					pos_total[word] += 1
		return pos_total

	def most_negative(self):
		neg_total = {}
		split = self.text.lower().split()
		for word in split:
			if word in neg_ws:
				if word not in neg_total:
					neg_total[word] = 1
				else:
					neg_total[word] += 1
		return neg_total


#List comprehension to create a list of tweet instances
def tweet_lst(twitter_data):
	return [Tweet(item) for item in twitter_data['statuses']]


#sorting the tweet instances from 'most popular' to 'least popular' 
sorted_tweet_list = sorted (tweet_lst(twitter_data), key = lambda x: x.popularity(), reverse = True)
most_popular_tweets = sorted_tweet_list[:20]


#create a list of the top 20 most popular recent tweets from the NYTimes account mentioning Trump
trump_tweets = []
for x in most_popular_tweets:
	if x.trump_mentions() == True:
		trump_tweets.append(x.text)


#create a list of the top 20 most popular recent articles from the NYTimes website mentioning Trump
trump_articles = []
for x in article_lst(nyt_data):
	if x.trump_mentions() == True:
		trump_articles.append(x.title)


#create a list of positively charged words from both the top 20 popular recent tweets and top 20 popular recent articles 
pos_charged_words = []
for x in most_popular_tweets:
	if x.trump_mentions() == True:
		if len(x.most_positive()) > 0:
			pos_charged_words.append(x.most_positive().keys())

for x in article_lst(nyt_data):
	if x.trump_mentions() == True:
		if len(x.most_positive()) > 0:
			pos_charged_words.append(x.most_positive().keys())


#create a list of positively charged words from both the top 20 popular recent tweets and top 20 popular recent articles
neg_charged_words = []
for x in article_lst(nyt_data):
	if x.trump_mentions() == True:
		if len(x.most_negative()) > 0:
			neg_charged_words.append(x.most_negative().keys())

for x in most_popular_tweets:
	if x.trump_mentions() == True:
		if len(x.most_negative()) > 0:
			neg_charged_words.append(x.most_negative().keys())


#user input/interaction with the information 
inp = int(raw_input("How many of the top 20 most popular recent tweets from the NYTimes account do you think have content related to Donald Trump? Type a number between 0 and 20. "))
if inp == len(trump_tweets):
	print 'Correct!'
else:
	print "\n"
	print 'Actually,', len(trump_tweets), "out of 20 of the most popular recent tweets have some content related to Trump!"

print "\n"
print "Here is a peek at those tweets:"
for item in trump_tweets:
	print "\n"
	print item

print '\n************************'
print "\n"

inp2 = int(raw_input("How many of the top 20 most popular recent articles from the NYTimes account do you think have content related to Donald Trump? Type a number between 0 and 20. "))
if inp2 == len(trump_articles):
	print 'Correct!'
else:
	print "\n"
	print 'Actually,', len(trump_articles), "out of 20 of the most popular recent articles have some content related to Trump!"

print "\n"
print "Here is a peek at those article titles:"
for item in trump_articles:
	print "\n"
	print item

print '\n************************'
print "\n"
print "Take a look at the below to see a list of what positively and negatively charged words the top 20 most popular recent NYTimes tweets and top 20 most popular recent NYTimes articles with mentions of Donald Trump from nytimes.com used."
print "\n"
print 'Positively charged words:'
for item in pos_charged_words:
	for i in item:
		print i
print "\n"
print "Negatively charged words:"
for item in neg_charged_words:
	for i in item:
		print i
print "\n"
print "Based off of these lists, does it seem that the New York Times' recent popular content shows a bias for or against Donald Trump-related news on their web platforms? Does this make New York Times a reliable news source?"

print "\n"
print '\n******* UNITTESTS ********'

class general_tests(unittest.TestCase):
	def test_1(self):
		self.assertEqual(type(article_lst(nyt_data)), type([]), "testing type of article_lst(nyt_data)")
	def test_2(self):
		self.assertEqual(len(article_lst(nyt_data)), 20, "testing the length of article_lst(nyt_data)")
	def test_3(self):
		self.assertEqual(type(x.most_negative()), type({}), "testing type of x.most_negative()")
	def test_4(self):
		self.assertEqual(len(tweet_lst(twitter_data)), 100, "testing length of tweet_lst(twitter_data)")
	def test_5(self):
		self.assertEqual(type(sorted_tweet_list), type([]), "testing type of sorted_tweet_list")
	def test_6(self):
		self.assertEqual(len(most_popular_tweets), 20, "testing length of most_popular_tweets")
	def test_7(self):
		self.assertEqual(type(trump_tweets), type([]), "testing the type of trump_tweets")
	def test_8(self):
		self.assertEqual(type(trump_articles), type([]), "testing the type of trump_articles")

unittest.main(verbosity=2)
