CMPE 273 Project: sjsu chatbot
==============================

Make sure all the below required softwares are installed to run this chatbot:

Install Slack Client:
pip install slackclient

Install textblob:
pip install -U textblob

dependancy:
python -m textblob.download_corpora


About Application:
================

This is an interactive Chatbot meant to answer questions related to the university. Implemented using Slack API. The application so far can answer questions related to the courses and professors of Computer Engineering Department. For example, you can ask the Bot for a course description and pre-requisites, lecture hours and location for any of the class, or office hours of professor and location etc. 

The algorithm used to process the requests is based on NLP through TextBlob and is implemented in Python. We use Textblob to identify the parts of speech in the sentence and map the requests to the responses accordingly. Since the information provided as responses are time-specific, i.e. it is updated every semester, we decided to store them in the database, with tables for course, professors etc. Only these table need to be updated every semester, and the alogrithm will work without requiring any changes. Hence the responses are not static and it ia made as dynamic as possible. The Bot has been trained with requests related to courses and professors of Computer Engineering Department.



Database Structure:
================
We have used SQlite3 for implementing our SJSU chatbot application. It is a self-contained, server less, zero-configuration, transactional SQL database engine. The more important reason to choose this database is because its light weight which does not affect the performance of our application.
We have Defined all data structure shown as below and procedures to manipulate the database objects. All related scripts are in DB scripts folder.

|Table Name  |                                                              Details                          |
|----------  |                                  --------------------------------------------------------------|              
|COURSE     |                                   Details about Course code , description and its pre requisites| 
|COURSE_INFO |                                  Detailed information like course schedule, professor, class time, class section, class type,seats, class day , location|
|LECTURE_TYPE|                                  Details about lecture type code and its description|
|LECTURE_DAY|                                   Details about lecture day code and its description|
|GREET  |                                       Details about greeting requests, for example  Hi, Hello|
|DATA  |                                        Used by the algorithm to map requests to keywords and obtain details to fetch responses.|


How to Run:
===========
You need to have a Slack token and Bot ID to run this application. These two information must be stored in environment variables named : SLACK_BOT_TOKEN and BOT_ID. You can set them using commands:
export SLACK_BOT_TOKEN='your Slack token'
export BOT_ID='your bot id'

After this the Bot application can be started by using the command:

python sjsuchatbot.py

If you see the message : "SJSU Bot connected and running" , you can now log-in to Slack and start chatting.

