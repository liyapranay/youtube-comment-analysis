from flask import Flask,render_template,request, send_from_directory,session,redirect,url_for, redirect, jsonify
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from  nltk.corpus import stopwords
import re
import pickle
import seaborn as sns
from sklearn.feature_extraction.text import CountVectorizer
import random
pickle_in = open('classifier.pickle','rb')
classifier = pickle.load(pickle_in)
pickle_inn = open('tfidfvec.pickle','rb')
vec = pickle.load(pickle_inn)
app=Flask(__name__)
@app.route('/')
def mainpage():
	return render_template("ythome.html")

@app.route('/url_in', methods=["POST"])
def url_in():
	url = request.form['url_in']
	driver = webdriver.Chrome(executable_path=r"C:\Users\Pranay Liya\Downloads\chromedriver_win32 (1)\chromedriver.exe")
	driver.get(url)
	time.sleep(5)
	driver.execute_script('window.scrollTo(1, 500);')
	vertical = 5000
	#now wait let load the comments
	for i in range(0,20):
		time.sleep(10)
		driver.execute_script('window.scrollTo(1, {});'.format(vertical))
		vertical = vertical+5000
		comment_div=driver.find_element_by_xpath('//*[@id="contents"]')
		comments=comment_div.find_elements_by_xpath('//*[@id="content-text"]')
	total_comments=len(comments)
	con = []
	for comment in comments:
		con.append(comment.text)
	corpus = []
	for i in con:
		con = re.sub(r"\W",' ',str(i))
		con = con.lower()
		con = re.sub(r'\s+[a-z]\s+',' ',con)
		con = re.sub(r"^[a-z]\s+",' ',con)
		con = re.sub(r"\s+",' ',con)
		corpus.append(con)
	sample = vec.transform(corpus).toarray()
	pred = classifier.predict(sample)
	positive = 0
	negative = 0
	for i in pred:
		if i==1:
			positive +=1
		else:
			negative +=1
	percen_pos = 0
	percen_pos = 0
	percen_pos = (positive/total_comments)*100
	percen_pos = float("%.2f" % percen_pos)
	percen_neg = (negative/total_comments)*100
	percen_neg = float("%.2f" % percen_neg)
	vecz = CountVectorizer(max_features = 5000, min_df = 10, max_df= 0.6, stop_words = stopwords.words('english')).fit(corpus)
	bag_of_words = vecz.transform(corpus)
	sum_words = bag_of_words.sum(axis=0) 
	words_freq = [(word, sum_words[0, idx]) for word, idx in     vecz.vocabulary_.items()]
	words_freq =sorted(words_freq, key = lambda x: x[1], reverse=True)
	new = pd.DataFrame(words_freq[:5], columns=['Words','Count'])
	ax = sns.barplot(x="Words",y="Count", data=new, palette="Set3")
	name = random.randint(1,101)
	fig = ax.get_figure()
	fig.set_size_inches(5,4)
	fig.savefig("static/images/{}.png".format(name))

	return render_template("ythome.html", percen_neg=percen_neg,percen_pos=percen_pos,total = total_comments, name=name)
app.run()