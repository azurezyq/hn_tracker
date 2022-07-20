#!/usr/bin/env python3
from lxml import etree
from urllib.request import urlopen
from datetime import datetime
import json

def ParsePage(url):
  d = etree.parse(urlopen(url), etree.HTMLParser())
  posts = d.xpath('//tr[@class="athing"]')
  subtexts = d.xpath('//td[@class="subtext"]')
  ret = []
  for post, subtext in zip(posts, subtexts):
    score = subtext.xpath('.//span[@class="score"]')
    if score:
      score = int(score[0].text.split()[0])
    else:
      score = None
    timestamp = d.xpath('.//span[@class="age"]/@title')
    if timestamp:
      timestamp = timestamp[0]
    else:
      timestamp = None
    comment_element = subtext.xpath('.//a[contains(text(),"comments")]')
    if comment_element:
      hn_link = comment_element[0].get('href')
      num_comments = int(comment_element[0].text.split()[0])
    else:
      hn_link = None
      num_comments = None
    rank = int(post.xpath('.//span[@class="rank"]')[0].text.strip(' .'))
    link = post.xpath('.//a[@class="titlelink"]/@href')[0]
    title = post.xpath('.//a[@class="titlelink"]')[0].text
    id_str = post.get('id')
    ret.append({
      "rank" : rank,
      "post_timestamp" : timestamp,
      "score" : score,
      "num_comments" : num_comments,
      "link" : link,
      "hn_link" : hn_link,
      "title" : title,
      "id" : id_str,
      })
  return ret

urls = [
    "https://news.ycombinator.com/news",
    "https://news.ycombinator.com/news?p=2",
    "https://news.ycombinator.com/news?p=3"
    ]

results = []
for url in urls:
  for x in ParsePage(url):
    x["seen"] = datetime.now().isoformat()
    print(json.dumps(x))
