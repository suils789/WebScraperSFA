import numpy as np
from google import search
from bs4 import BeautifulSoup
import random
import time
from collections import OrderedDict
import pandas as pd
import re
import flask
from flask import Flask, Response, request, render_template, redirect, url_for
from flaskext.mysql import MySQL
import flask_login
from werkzeug import secure_filename
import os, base64

app = Flask(__name__)
app.secret_key = 'super secret string'  # Change this!



@app.route('/', methods = ['GET', 'POST'])
def mergingData():
	if request.method == 'POST':
		print ('starting...')
		print ('loading data...')
	##note: change the path of database before running the follow line of code
		
		data = request.files['data']
		data = pd.read_excel(data).drop('ID', axis = 1)
		print ('finish loading data...')
		keywords = request.form.get('description')
		list1 = keywords.split(',')
		list2= request.form.getlist('states')
		urlnumber = int(request.form.get('number'))
		list3 = []
		# list1 = ["drug testing services"] 
		# list2= ["CT"]
		# urlnumber = 20
		# list3 = []

		file_name = list1[0] + '.csv'
		if not os.path.exists('/Users/admin/Desktop/output/' + file_name):
			print ('Everything is good, start scraping:')
		else:
			raise Exception('A very specific bad thing happened')
		    

		for i in range(len(list1)):
			for j in range(len(list2)):
				list3.append(list1[i] + '' + list2[j])
		        
		res = {}

		i = 0
		while i < len(list3): 
			try:
				for url in search(list3[i], tld='com', lang='en', num=100, start=0, stop=urlnumber, pause=random.uniform(5.0,30.0)):
					r = re.compile(r"https?://(www\.)?")
					url = r.sub('', url).strip().strip('/')
					url = url.split('/')[0]
					if list3[i][:-2] in res:
						res[list3[i][:-2]].append(url)
					else:
						res[list3[i][:-2]] = [url]

					if len(res[list3[i][:-2]])%10 == 0:
						print (list3[i][:-2] + ' number of urls scraped: ' + str(len(res[list3[i][:-2]])))

				i += 1
			except:
				print ('IP got blocked, restarting...')
				time.sleep(1000)
		for key in res:
			for i in range(len(res[key])):
				res[key][i] = res[key][i].replace('https://', '').replace('http://', '').replace('www.', '').replace('\xa0', '/')
				res[key][i] = res[key][i].split('/')[0]
		res[key] = list(set(res[key]))

		exclude_term = ['capterra.com', 'angieslist.com', 'thomasnet.com', 'indeed.com', 'amazon.com', 'bloomberg.com', 'ziprecruiter.com', 'monster.com', 'manta.com', 'bbb', 'facebook', 'yelp', 'cognate.com', 'yellowpages', 'linkedin', 'angieslist', '.gov', '.org', 'zoominfo', 'bloomberg', 'superpage', 'bluebook', 'opencorporate', 'bizstanding', 'indeed.', 'homeadvisor', 'bizapedia', 'thumbtack', 'findthecompany', 'nasdaq', 'smallbusinessdb', 'whitepages', 'caselaw', 'bizpedia', 'plus.google', 'prezi.com', '.co.', 'kompass', 'usplaces.com', 'buzzfile.com', 'businessdetail', 'companydetail', 'hipaaspace', 'registry', 'twitter', 'govtribe', 'foursquare', 'referenceforbusiness', '.edu', '.uk', 'ebay.', 'corps', 'amazon.', 'youtube.', 'statelaw', 'buildzoom', 'company-detail', 'corporationwiki', 'moreopp', 'freightconnect', 'care.com', 'scribd', 'groupon', 'estatesales', 'carmax', 'alibaba', 'porch.com', 'yellowbook', 'usbizs', 'thomasnet', 'houzz', 'www.inc.com', 'foodcorporations', 'encyclopedia.com', 'directionus.com', 'companiesflorida', 'landscape', '.com.', 'staffing', 'allonesearch', 'broker', 'localbiziness', 'law.justia', 'investment', 'investor', 'google.', 'roofing', 'international', 'carpet', 'construction', 'wealth', 'insurance', 'auto', 'grading', 'health', 'siccode', 'kompass', 'macraesbluebook', 'indeed', 'bakery', 'whitepages', 'staff', 'hoovers', 'news', 'crunchbase', 'myvisajob', 'furniture', 'cpa', 'wiki', 'jewel', 'journal', 'pinterest', 'twitter', 'dealer', 'porch', 'investor', 'registry', 'farm', 'wedding', 'industrycat', 'wordpress', 'obituar', 'overstock', 'aerospace', 'usacorporates', 'instagram', '.mil', 'kayak.com', 'intelius', '.in/', 'dictionary', 'cortera', 'payscale', 'uscompanies', 'mapquest', 'glassdoor', 'weebly', 'businessfinder', 'macafee', 'espn.com', 'chron.com', 'imdb.com', 'food', 'lawyer', 'corporationsearchus.com', 'tribune', 'ancestry.com', 'nytimes.com', 'wsj.com', 'bostonglobe.com', 'careerbuilder.com', 'glassdoor.com', 'snagajob.com', 'dice.com', 'beyond.com', 'flexjobs.com']

		for x in range(len(res[key])):
			for y in exclude_term:
				if y in res[key][x]:
					res[key][x] = 'this is a bad url!!!'


		# res[key]=[x for x in res[key] if not '.gov' in x if not'youtube'in x if not 'manta' in x if not '.edu' in x if not 'yelp' in x\
		# 			if not 'yellowbook' in x if not 'glassdoor' in x if not 'linkedin' in x if not 'facebook' in x if not '.org' in x\
		# 			if not '.indeed' in x if not '.amazon' in x if not 'google' in x if not 'yellowpages' in x if not '.ca' in x]
					
		res[key] = [x for x in res[key] if '.com' in x or '.us' in x or '.org' in x or '.biz' in x or '.net' in x]
		        

		result = []
		for key in res:
			for i in range(len(res[key])):
				result.append((key, res[key][i]))
		industry = [list(t) for t in zip(*result)][0]
		urls = [list(t) for t in zip(*result)][1]

		test = pd.DataFrame(pd.Series(urls), columns = ['URLtrim'])
		test['industry'] = pd.Series(industry)
		result = data.merge(test, how = 'right', on = 'URLtrim')
		url_list = result['URLtrim'].values.tolist()
		
		for i in range(len(url_list)):
			url_list[i] = 'http://' + url_list[i]

		result['url'] = pd.Series(url_list)
		path_d = '/Users/admin/Desktop/output'

		result.to_csv(os.path.join(path_d, file_name)) 
		print ('scraping done, output file path: ' + path_d)
		print ('Bye')
		return 'scraping done'
	else:
		return render_template('webscraper.html')


if __name__ == "__main__":
	#this is invoked when in the shell  you run 
	#$ python app.py 
	app.run(host='127.0.0.1', debug=True, port=6235)