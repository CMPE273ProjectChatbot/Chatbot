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


How to Run:
===========


Database Structure:
================
We have used SQlite3 for implementing our SJSU chatbot application. It is a self-contained, server less, zero-configuration, transactional SQL database engine. The more important reason to choose this database is because its light weight which does not affect the performance of our application.
We have Defined all data structure shown as below and procedures to manipulate the database objects.

Table Name                                                                Details
----------                                    --------------------------------------------------------------              
COURSE                                        Details about Course code , description and its pre requisites 
COURSE_INFO                                   Detailed information like course schedule, professor, class time, class section, class type,                                               seats, class day , location
LECTURE_TYPE                                  Details about lecture type code and its description
LECTURE_DAY                                   Details about lecture day code and its description
GREET                                         Details about greeting requests, for example  keywords(Noun) and its response
DATA                                          Details about requests,  for example  keywords(Noun) to fetch the details from tables to                                                   form response

