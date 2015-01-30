import urllib2
from bs4 import BeautifulSoup

url = 'http://www.mercurynews.com/sports'

page = urllib2.urlopen(url)

soup = BeautifulSoup(url)

headers = soup.findAll('options')