from BeautifulSoup import BeautifulSoup
import urllib2
import re
import time
import csv

start = time.time()
descList = [["Course Number","Course Name", "Description"]]
csv_file = open("description.csv", "wb")
courses = ['101', '102', '110', '120', '124', '125', '126', '127', '130', '131', '132', '133', '135', '137', '138', 
            '139', '140', '142', '146', '147', '148', '149', '150', '152', '163', '165', '172', '180', '187', '188',
            '189', '197', '198', '200', '202', '203', '206', '207', '208', '209', '210', '212', '213', '217', '219', 
            '220', '225', '226', '227', '235', '236', '237', '240', '242', '243', '244', '245', '250', '253', '255', 
            '256', '257', '264', '265', '270', '271', '272', '273', '274', '275', '276', '277', '279', '280', '281', 
            '282', '283', '284', '285', '287', '289', '292', '294', '297', '298']
for course in courses:
    url = "http://info.sjsu.edu/web-dbgen/catalog/courses/CMPE" + course + ".html"
    try:
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page)
        coursenumber, coursename = soup.html.body.findAll("h3")[:2]
        description = soup.html.body.findAll("p")[1].text
        descList.append([coursenumber.text, coursename.text, description.split("Description")[1]])
    except:
        pass
writer = csv.writer(csv_file)
writer.writerows(descList)
print "time taken  ", time.time()-start



 