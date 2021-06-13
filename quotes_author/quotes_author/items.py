import scrapy


class AuthorItem(scrapy.Item):
    name = scrapy.Field()
    birth_date = scrapy.Field()
    birth_place = scrapy.Field()
    description = scrapy.Field()
    pass
