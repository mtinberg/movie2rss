#! /usr/bin/env /usr/bin/python

import urllib
import string
import codecs
from dict2rss import dict2rss
from HTMLParser import HTMLParser

url = 'http://www.google.com/movies?hl=en&near=53705&tid=6ae426071b5ee724'
sock = urllib.urlopen(url)

movies = {'title': 'Movie times for Market Square', 'item': {}, 'version': '0.1', 'link': '' }

class parser(HTMLParser):
  def __init__(self):
    HTMLParser.__init__(self)
    self.printing = 0
    self.href = ""
  def handle_starttag(self, tag, attrs):
#    print(" tag: ", tag)
#    for name, value in attrs:
#      print("   attr: ", name, value)
    if tag == 'div':
      for name, value in attrs:
        if name == "class" and value == "name":
          self.printing = 1 
    if tag == 'a':
      for name, value in attrs:
        if name == "href" and value.startswith('/movies'):
          self.href = "http://www.google.com" + value
  def handle_data(self, data):
    if self.printing == 1:
      movies['item'][data] = {}
      movies['item'][data]['description'] = data
      movies['item'][data]['content'] = self.href
      self.printing = 0

p = parser()

#print(sock.info())
html = codecs.decode(sock.read())
#print(len(html))
fixed = string.replace(html, '"onresize', '" onresize')
p.feed(fixed)
p.close()
sock.close()

#print(movies)

rss = dict2rss(movies)
rss.PrettyPrint()
