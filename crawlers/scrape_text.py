import newspaper
import json
import os
import sys
import glob
import time
start_time = time.time()
reload(sys)
sys.setdefaultencoding('utf-8')


def print_data():

	json_dir = '../data/NYTimes/JSON'
	for jfile in glob.glob("../data/NYTimes/201512*.data"):
		timeperiod = os.path.basename(jfile).split('.')[0]
	        print(timeperiod)
		content_dir = '../data/NYTimes/Text/' + timeperiod
		if not os.path.exists(content_dir):
    			os.makedirs(content_dir)

		jsonop = open(json_dir + '/' +  timeperiod + '.json', 'w')
		
		with  open(jfile, 'r') as ipfile:
			
			for idd, line in enumerate(ipfile):			
				obj = json.loads(line)
				print(timeperiod, idd, time.time() - start_time)

				article = newspaper.Article(obj['web_url'])
				article.download()
				article.parse()
				
				txt_file =  content_dir  +'/' +  str(idd) + '.txt'
				with open(txt_file, 'w') as  txt_file_writer:
					txt_file_writer.write(article.text)

	
		  		obj['content_file'] = txt_file 
				jsonop.write(json.dumps(obj))
				jsonop.write("\n")			




		#print(article.text)
print("Hello World")
print_data()

