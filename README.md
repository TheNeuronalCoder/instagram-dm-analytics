instagram dm analytics
======================

Simple python script which ranks the people you DM on instagram through various metrics.

```bash
$ python analytics.py
```
![Demo](https://i.ibb.co/TYhHJ2X/instagram-dm-analytics-demo.png)

## How It Works
If you go into `Settings > Security` in Instagram you can request to download all of your instagram data. What the script does is, when placed in the root folder, will extract all messaging data and rank each person through different metrics.

## Install Dependences

Before you run the script you must have:
 - tabulate to form the formatted tables
 and
 - BeautifulSoup to parse HTML files
 
```bash
# Install Dependencies
$ pip install tabulate BeautifulSoup
```
