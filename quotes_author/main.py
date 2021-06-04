from quotes_author.spiders.QuotesAuthorSpider import QuotesAuthorSpider
from Scraper import Scraper


scraper = Scraper(QuotesAuthorSpider, output_format="MySQL")
scraper.run_spider()
