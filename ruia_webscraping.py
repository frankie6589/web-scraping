# -*- coding: utf-8 -*-
import re
from datetime import datetime, timedelta
import pymysql
import pandas as pd
import numpy as np
from inlp.convert import char, chinese
from inlp.explode import Strokes, Chars
import bs4
from bs4 import BeautifulSoup, NavigableString, Tag,Comment
import requests
import time
#from new_words_finder import NewWordsFinder
import wordiscovery as wd
import matplotlib.pyplot as plt
import seaborn as sns
from cnt import rulebase
import os
from ruia import AttrField, TextField, Item
from ruia_pyppeteer import PyppeteerSpider as Spider


page_list=['https://www.openrice.com/zh/hongkong/restaurants/type/%E9%85%92%E5%90%A7?page={}'.format(i) for i in range(1,3)]  #請ben少在range function內,更改page number


class page_Item(Item):
    target_item = TextField(css_select='#global-container > main > section.sr1-center-content-wrapper.js-sr1-center-content-wrapper > section.sr1-listing-container.pois-listings.js-sr1-listings > #or-route-poi-list-main > ul.sr1-listing-content-cells.pois-restaurant-list.js-poi-list-content-cell-container')
    # Openrice 網頁內的css selector from google chrome :
    # lv 1:  #global-container > main > section.sr1-center-content-wrapper.js-sr1-center-content-wrapper
    # lv 2:  #global-container > main > section.sr1-center-content-wrapper.js-sr1-center-content-wrapper > section.sr1-listing-container.pois-listings.js-sr1-listings
    # lv 3:  #or-route-poi-list-main     /div.js-poi-list-main  (javascript) start from there
    # lv 4:  #or-route-poi-list-main > ul.sr1-listing-content-cells.pois-restaurant-list.js-poi-list-content-cell-container


    restaurant_names = TextField(css_select='li > div > section.content-wrapper > div.title-wrapper > h2 > a', many=True)
    #  Openrice 網頁內的css selector from google chrome :
    # lv 1:  li > div > section.content-wrapper > div.title-wrapper > h2
    # lv 2:  #or-route-poi-list-main > ul > li > div > section.content-wrapper > div.title-wrapper > h2 > a

class OpenRice_Spider(Spider):
    start_urls = page_list
    concurrency = 10

    async def parse(self, response):
        async for item in page_Item.get_items(html=response.html):
            yield item

    async def process_item(self, item: page_Item):
        for restaurant_name in item.restaurant_names:
            print(restaurant_name)


if __name__ == '__main__':
    OpenRice_Spider.start()
