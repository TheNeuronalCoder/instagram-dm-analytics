import os
import sys
import glob
import itertools
from nrclex import NRCLex
from bs4 import BeautifulSoup
from tabulate import tabulate

def load_data():
  print('Loading DM Data...')
  data = {}

  my_info = BeautifulSoup(
              open(f'{os.getcwd()}/account_information/personal_information.html', 'r').read(), 'lxml'
            ).find_all('tr', class_='_51mx')
  my_name = next(filter(lambda x: x.find('td', class_='_51m- vTop _2pin _2oao').text == 'Name', my_info))
  my_name = my_name.find('td', '_51m- vTop _2pin _2piu _23bw _51mw').text
  os.chdir('messages/inbox')

  for username in os.listdir(os.getcwd()):
    if os.path.isdir(username):
      messages = [BeautifulSoup(open(file, 'r').read(), 'lxml')
                  for file in glob.glob(f'{os.getcwd()}/{username}/message_*.html')]

      dms = { 'me': [], 'other': [] }
      for dm in sum([msg.find_all('div', class_='pam _3-95 _2ph- _2lej uiBoxWhite noborder') for msg in messages], []):
        if dm.find('div', class_='_3-95 _2let'):
          text = dm.find('div', class_='_3-95 _2let').find('div').find_all('div')[1].text
          if len(text) and not text.endswith(' '):
            if dm.find('div', class_='_3-95 _2pim _2lek _2lel').text == my_name:
              dms['me'].append(text)
            else:
              dms['other'].append(text)

      name = messages[0].find('div', class_='_3b0d').text
      name = username if name == 'Instagram User' else name
      data[name] = ({ 'me': dms['me']+data[name]['me'],
                      'other': dms['other']+data[name]['other'] }
                   if name in data
                   else dms)
      print(f'{name} ✓')

  return data

def rank(count):
  return sorted(
    [{ 'name': user, 'count': count(data[user]) } for user in data],
    key=lambda x: x['count'],
    reverse=True
  )

def text_count_rank():
  return rank(lambda dms: len(dms['me']+dms['other']))

def character_count_rank():
  return rank(lambda dms: len(''.join(dms['me']+dms['other'])))

def word_count_rank():
  return rank(lambda dms: ' '.join(dms['me']+dms['other']).count(' ')+1)

def query_count_rank(*words, sender):
  return rank(lambda dms: sum(' '.join(dms['me']+dms['other'] if sender=='both' else dms[sender]).count(word) for word in words))

def emotion_rank(emotion, sender):
  return rank(lambda dms: NRCLex(' '.join(dms['me']+dms['other'] if sender=='both' else dms[sender])).affect_frequencies.get(emotion, 0))

if __name__ == "__main__":
  data = load_data()
  print(tabulate(
    [[r+1,
      f'{(a["name"][:15] + "...") if len(a["name"]) > 15 else a["name"]} ({a["count"]} texts)',
      f'{(b["name"][:15] + "...") if len(b["name"]) > 15 else b["name"]} ({b["count"]} characters)',
      f'{(c["name"][:15] + "...") if len(c["name"]) > 15 else c["name"]} ({c["count"]} words)',
      f'{(d["name"][:15] + "...") if len(d["name"]) > 15 else d["name"]} ({d["count"]} times)',
      f'{(e["name"][:15] + "...") if len(e["name"]) > 15 else e["name"]} ({round(e["count"]*100)}%)']
    for r, a, b, c, d, e in zip(list(range(len(data))),
                                text_count_rank(),
                                character_count_rank(),
                                word_count_rank(),
                                query_count_rank('LMAO', 'LOL', 'HAHA', sender='other'),
                                emotion_rank('joy', sender='me'))],
    headers=['Rank', 'Invidiual Texts', 'Character Count', 'Word Count', 'Laugh Count', 'Joy'],
    tablefmt='fancy_grid'
  ))
