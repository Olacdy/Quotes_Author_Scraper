import scrapy
from scrapy import signals
from ..items import AuthorItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class QuotesAuthorSpider(CrawlSpider):
    name = "quotes_author"
    start_urls = [
        'http://quotes.toscrape.com/page/1/'
    ]

    rules = (Rule(LinkExtractor(allow=(), restrict_xpaths=('/html/body/div[1]/div[2]/div[1]/nav/ul/li/a',)),
                  callback="parse", follow=True),)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = args[0]
    
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesAuthorSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        self.parent.is_closed = True

    def parse(self, response, **kwargs):
        for href in response.css(".quote span a::attr('href')"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        item = AuthorItem()
        item['name'] = response.css('.author-title::text').extract()
        item['birth_date'] = response.css('.author-born-date::text').extract()
        item['birth_place'] = response.css('.author-born-location::text').extract()
        item['description'] = response.css('.author-description::text').extract()
        yield item
