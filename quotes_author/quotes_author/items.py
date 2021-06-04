# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AuthorItem(scrapy.Item):
    name = scrapy.Field()
    birth_date = scrapy.Field()
    birth_place = scrapy.Field()
    description = scrapy.Field()
    pass
