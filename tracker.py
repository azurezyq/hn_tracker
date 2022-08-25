#!/usr/bin/env python3
from lxml import etree
from urllib.request import urlopen
from datetime import datetime
import json
import argparse
import time

PARSER_VERSION = 2

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
    timestamp = subtext.xpath('.//span[@class="age"]/@title')
    if timestamp:
      timestamp = timestamp[0] + 'Z'
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
      'rank' : rank,
      'post_timestamp' : timestamp,
      'score' : score,
      'num_comments' : num_comments,
      'link' : link,
      'hn_link' : hn_link,
      'title' : title,
      'id' : id_str,
      'parser_version' : PARSER_VERSION,
      })
  return ret

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='HN tracker')
  parser.add_argument('--pages', type=int, nargs='?', default=3)
  args = parser.parse_args()

  results = []
  seen = datetime.now().isoformat() + 'Z'
  for n in range(1, args.pages + 1):
    time.sleep(2)
    url = f'https://news.ycombinator.com/news?p={n}'
    for x in ParsePage(url):
      x["seen"] = seen
      print(json.dumps(x))
