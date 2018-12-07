# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HexunItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    classify_name = scrapy.Field()
    links = scrapy.Field()
    names = scrapy.Field()

class DataItem(scrapy.Item):
    data = scrapy.Field()
    classify_name = scrapy.Field()
