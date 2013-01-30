#!/usr/bin/env python

import sys
import json
import feedparser
from urlparse import urlparse, parse_qs
from HTMLParser import HTMLParser

import requests

feeds = [
    "http://news.google.com/news?ned=us&topic=h&output=rss",
    "http://news.google.com/news?ned=us&topic=w&output=rss",
    "http://news.google.com/news?ned=uk&topic=n&output=rss",
    "http://news.google.com/news?ned=us&topic=b&output=rss",
    "http://news.google.com/news?pz=1&cf=all&ned=us&hl=en&topic=tc&output=rss",
    "http://news.google.com/news?ned=us&topic=s&output=rss",
    "http://news.google.com/news?ned=us&topic=e&output=rss",
    "http://news.google.com/news?pz=1&cf=all&ned=us&hl=en&topic=snc&output=rss",
    ]

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        #return ''.join(self.fed)
        return self.fed
    
def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()
            
def main ():

    for f in feeds:
        print f
        news = feedparser.parse(f)
        for i in news['items']:
            
            o = urlparse(i['link'])
            if o.netloc == 'news.google.com':
                
                q = parse_qs(o.query)
                url = q['url'][0]
                texts = strip_tags(i.description)
                jist = max(texts, key=len)
                
                doc = dict(
                    title = i['title'],
                    url = url,
                    jist = jist,
                    )

                headers = {'content-type': 'application/json'}
                r = requests.post(
                    'http://localhost:5000/articles/',
                    data=json.dumps(doc),
                    headers=headers
                    )
                status = r.status_code
                
                if 200 <= status < 300:
                    print status, r.json()
                else:
                    print status, json.dumps(doc)
                    
                print

                

if __name__ == '__main__':
    try:
        main()
        sys.exit(0)
    except KeyboardInterrupt, e: # Ctrl-C
        raise e
