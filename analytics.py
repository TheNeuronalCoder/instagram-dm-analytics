import os
import sys
import glob
import itertools
from bs4 import BeautifulSoup
from tabulate import tabulate

def parse_html(user):
  return filter(
    lambda dm: dm.find('div', class_='_3-95 _2let'),
    sum([
      BeautifulSoup(open(file, 'r').read(), 'lxml').find_all('div', class_='pam _3-95 _2ph- _2lej uiBoxWhite noborder')
      for file in glob.glob(f'{os.getcwd()}/{user}/message_*.html')
    ], [])
  )

def extract_all_messages(user):
  return list(filter(
    lambda text: len(text) and not (text.startswith('Reacted ') and text.endswith(' to your message ')),
    [dm.find('div', class_='_3-95 _2let').find('div').find_all('div')[1].text for dm in parse_html(user)]
  ))

def extract_messages(user):
  return list(filter(
    lambda text: len(text) and not (text.startswith('Reacted ') and text.endswith(' to your message ')),
    [text.find('div', class_='_3-95 _2let').find('div').find_all('div')[1].text for text in filter(
      lambda dm: dm.find('div', class_='_3-95 _2pim _2lek _2lel').text != 'candy slut',
      parse_html(user)
    )]
  ))

def rank(count):
  return sorted(
    [{'name':username,'count': count(username)} for username in os.listdir(os.getcwd())],
    key=lambda x: x['count'],
    reverse=True
  )

def text_count_rank():
  return rank(lambda p: len(extract_all_messages(p)))

def character_count_rank():
  return rank(lambda p: len(''.join(extract_all_messages(p))))

def word_count_rank():
  return rank(lambda p: ' '.join(extract_all_messages(p)).count(' ')+1)

def query_count_rank(word):
  return rank(lambda p: ' '.join(extract_messages(p)).count(word))

if __name__ == "__main__":
  os.chdir('messages/inbox')

  print(tabulate(
    [[r+1,
      f'{(a["name"][:15] + "...") if len(a["name"]) > 15 else a["name"]} ({a["count"]} texts)',
      f'{(b["name"][:15] + "...") if len(b["name"]) > 15 else b["name"]} ({b["count"]} characters)',
      f'{(c["name"][:15] + "...") if len(c["name"]) > 15 else c["name"]} ({c["count"]} words)',
      f'{(d["name"][:15] + "...") if len(d["name"]) > 15 else d["name"]} ({d["count"]} laughs)']
    for r, a, b, c, d in zip(list(range(len(os.listdir(os.getcwd())))),
                                  text_count_rank(),
                                  character_count_rank(),
                                  word_count_rank(),
                                  query_count_rank('LMAO'))],
    headers=["Rank", "Invidiual Texts", "Character Count", "Word Count", "Laugh Count"],
    tablefmt='fancy_grid'
  ))