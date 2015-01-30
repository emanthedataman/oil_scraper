#import urllib2 library
import urllib2

#import BeautifulSoup library
from bs4 import BeautifulSoup

#save the url as variable
url = 'https://www.dmr.nd.gov/oilgas/riglist.asp'

#pass url into urlopen method to open and read the URL
page = urllib2.urlopen(url)

#convert opened url into an html_doc
soup = BeautifulSoup(page)

#open the file and set to the write
sout = open('active_drilling.csv', 'w')

#Start at the 6th tag and go all the way to the 15, but not including
for thTag in range(6, 15):
	#headers = find all the th tags and then text strips everything that surrounds that text.
	headers = soup.findAll('th')[thTag].text
	#5 for modulo. Added 9, because there are 9 headers, to six but you start at 6. the sum is 14, divide by 9 and the remainder is 5.
	#the thTag is the 14th tag then print on a new line
	if thTag%9 == 5:
		sout.write("\"" + headers + "\"" + '\n')
	#if the thTag is not the 14th tag then print on the same line
	else:
		sout.write("\"" + headers + "\"" + ',')

#start at the 9th td tag and go through the 1422nd tag, but no including
for rig in range(9, 1422):
	#the variable record is the text that is between every td tag
	record = soup.findAll('td')[rig].text
	#it's multiples of the 17. And 9 pieces of text. 17 divded by 9 has a remainder of 8
	if rig%9 == 8:
		#when modulo equals 8 start a new line
		sout.write("\"" + record + "\"" + '\n')
	else:
		#everything else print on the same line
		sout.write("\"" + record + "\"" + ',')

#close the file
sout.close()