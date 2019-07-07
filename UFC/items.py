# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class EventItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    date = scrapy.Field()
    location = scrapy.Field()
    attendance = scrapy.Field()
    name = scrapy.Field()
    fight_count = scrapy.Field()

class FightItem(scrapy.Item):
	bout_order = scrapy.Field()

