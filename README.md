instagram dm analytics
======================

Simple python script which ranks the people you message on instagram through various metrics.

```bash
$ python analytics.py
```
![Demo](https://i.ibb.co/TYhHJ2X/instagram-dm-analytics-demo.png)

## How It Works
If you go into `Settings > Security` in Instagram you can request to download all of your instagram data. What the script does is, when placed in the root folder, will extract all messaging data and rank each person through different metrics.

## Install Dependences

Before you run the script you must have:
 - [`tabulate`](https://pypi.org/project/tabulate) for formatting tables
 - [`NRCLex`](https://pypi.org/project/NRCLex) for natural language processing
 - [`BeautifulSoup`](https://pypi.org/project/beautifulsoup4) for parsing HTML files
 
```bash
# Install Dependencies
$ pip install tabulate NRCLex beautifulsoup4 nltk
$ python
>>> import nltk
>>> nltk.download('punkt')
```
