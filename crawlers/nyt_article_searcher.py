import sys
import os
import random
import requests
import datetime
import time
import json
import math

def crawl_nyt():
	
	dayjump = 1
	pages = range(1, 101)	
	
	api_keys = ['b9f6cf6ee1fdcaa58a3d760b4d693f15:19:74490258', 'd659a72afd30a86686d9545457a1ebe4:7:74490258' , '8e9b89987c890838ef2e722c3ab0e9ef:15:74492419', '83d2d910c9d30979c9a797db9839f59a:9:74492419', 'd4d257cbc2de8d993bba43782f1668f4:0:74492419', '7ba3836e2ab6c094de7b7e0aead16b19:10:74490258']

	start_date = datetime.date(2015, 9, 6);
	date_offset = datetime.timedelta(days = dayjump-1)
	date_objs = [((start_date + datetime.timedelta(days = i)),(start_date + datetime.timedelta(days=i) + date_offset)) for i in range(0, 2600, dayjump)]
	dates = [('%04d'%d1.year + '%02d'%d1.month + '%02d'%d1.day, '%04d'%d2.year + '%02d'%d2.month + '%02d'%d2.day)   for (d1, d2)  in date_objs]
	
	print(len(dates))
	#print(dates)
	#print(len(dates))
	#news_desks = ['Adventure Sports', 'Arts & Leisure', 'Arts', 'Automobiles', 'Blogs', 'Books', 'Booming', 'Business Day', 'Business', 'Cars', 'Circuits', 'Classifieds', 'Connecticut', 'Crosswords & Games', 'Culture', 'DealBook', 'Dining', 'Editorial', 'Education', 'Energy', 'Entrepreneurs', 'Environment', 'Escapes', 'Fashion & Style', 'Fashion', 'Favorites', 'Financial', 'Flight', 'Food', 'Foreign', 'Generations', 'Giving', 'Global Home', 'Health & Fitness', 'Health', 'Home & Garden', 'Home', 'Jobs', 'Key', 'Letters', 'Long Island', 'Magazine', 'Market Place', 'Media', "Men's Health", 'Metro', 'Metropolitan', 'Movies', 'Museums', 'National', 'Nesting', 'Obits', 'Obituaries', 'Obituary', 'OpEd', 'Opinion', 'Outlook', 'Personal Investing', 'Personal Tech', 'Play', 'Politics', 'Regionals', 'Retail', 'Retirement', 'Science', 'Small Business', 'Society', 'Sports', 'Style', 'Sunday Business', 'Sunday Review', 'Sunday Styles', 'T Magazine', 'T Style', 'Technology', 'Teens', 'Television', 'The Arts', 'The Business of Green', 'The City Desk', 'The City', 'The Marathon', 'The Millennium', 'The Natural World', 'The Upshot', 'The Weekend', 'The Year in Pictures', 'Theater', 'Then & Now', 'Thursday Styles', 'Times Topics', 'Travel', 'U.S.', 'Universal', 'Upshot', 'UrbanEye', 'Vacation', 'Washington', 'Wealth', 'Weather', 'Week in Review', 'Week', 'Weekend', 'Westchester', 'Wireless Living', "Women's Health", 'Working', 'Workplace', 'World', 'Your Money']

	
	
	parameters = {
	'sort' : 'newest',
	'fl': 'pub_date,headline,keywords,web_url,section_name',
	'fq' : 'source:("The New York Times")',
	}
	articles_collected = 0 
	for (begin_date, end_date) in dates:
	#	print(begin_date)
		parameters['begin_date'] = begin_date
		parameters['end_date'] =  end_date
		page_bound = 100
		opfile = open("../data/NYTimes/" + begin_date + "_to_" + end_date + ".data", 'w')

		for page in range(0,101):	
			attempts = 0
			parameters['page'] = page
				
			while True:
				attempts+=1
				api_key = random.choice(api_keys)
					
				parameters['api-key'] = api_key 
				r = requests.get("http://api.nytimes.com/svc/search/v2/articlesearch.json", params = parameters)
				#print(r.url)
				if(r.status_code == 200):
					response = r.json()['response']
					if page==0:
						print("Hits for ", begin_date, " =  " , response['meta']['hits'])
						page_bound = math.ceil(int(response['meta']['hits'])/10.0)
						
					for doc in response['docs']:
						articles_collected +=1
						entry = {}
						entry['web_url'] = doc['web_url']
							
						if 'headline' in doc.keys():
							if len(doc['headline'])>0:
								if 'main' in doc['headline'].keys():
									entry['headline'] = doc['headline']['main']
						if 'keywords' in doc.keys():
							entry['keywords'] = doc['keywords']
						if 'pub_date' in doc.keys():
							entry['pub_date'] = doc['pub_date']
						if 'section_name' in doc.keys():
							entry['section_name'] = doc['section_name']
						opfile.write(json.dumps(entry))
						opfile.write("\n")
					break
				else:
					if attempts >=50:
						print("API End Points exhausted! Going to sleep for a while . . . ")
						time.sleep(30000)
						attempts = 0 
			
			if page>page_bound:
				break

		print("Articles Collected = " , articles_collected)





crawl_nyt()
