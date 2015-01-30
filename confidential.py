#improt urllib2
import urllib2

#import BeautifulSoup
from bs4 import BeautifulSoup

#save the url as a variable
url = 'https://www.dmr.nd.gov/oilgas/confidential.asp'

#grab the url and open it
page = urllib2.urlopen(url)

#convert the opened url as html
soup = BeautifulSoup(page)

#opening a csv file to write
f = open('confidential.csv', 'w')

#the th tag enclosing the file# is the very first in the page
#There are five tags that I want so I go to six, but it's no inclusive
for thTags in range(0, 6):
	#found all the text between the th Tags and strip them away
	headers = soup.findAll('th')[thTags].text
	#if the tag is the fifth one then print on a new line
	if thTags == 5:
		f.write("\"" + headers + "\"" + '\n')
	#otherwise print on the same line	
	else:
		f.write("\"" + headers + "\"" + ',')

#start the scrape with the third tag and go to the 13593
for tdTags in range(3, 13593):
	#strip the tags from the text
	records = soup.findAll('td')[tdTags].text
	#there are six columns, and the last one is eight
	if tdTags%6 == 2:
		 #print on new line
		 f.write("\"" + records + "\"" + '\n')
	else:
		#print on the same line
		f.write("\"" + records + "\"" + ',')

#close file
f.close()