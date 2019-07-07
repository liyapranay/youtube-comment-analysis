# youtube-comment-analysis

For any Content creator it is important to work on feedback , so I have created a web application that will help to analyse the youtube comment ,whether the comment is positive or not and also shows top 5 words used in comments.This application is basically divided into 3 parts
1. web UI using Flask:
  so user can put the link of youtube video that they want to analyze.
2. Web scraping using Selenium Webdriver:
  This is used to parse the comment automatically from the given link.
3. Machine Learning and NLP:
  All the comments that are scraped is pass to trained NLP model which then classify the comment and display the results as shown at the end of the video. 


# File Description:

X.pickle - Training Data.
y.pickle - Target Data.
classifier.pickle - NLP pre-trained model.
tfidfvec.pickle - TFIDF vactorizer model.
servernew.py - python flask server , directly run it in your computer just create static/img folder in the same directory as servernew.py file.
