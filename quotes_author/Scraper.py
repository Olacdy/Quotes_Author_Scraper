from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from inspect import isclass
import quotes_author.pipelines as Pipelines
import os


class Scraper:
    def __init__(self, spider, output_format='json'):
        settings_file_path = 'quotes_author.settings'
        os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
        settings = get_project_settings()
        classes = [x for x in dir(Pipelines) if isclass(getattr(Pipelines, x))]
        matching = [s for s in classes if output_format.lower() in s.lower()][0]
        settings.update(
            {
                "ITEM_PIPELINES": {
                    f'quotes_author.pipelines.{matching}': 1
                }
            }
        )
        self.process = CrawlerProcess(settings)
        self.spider = spider

    def run_spider(self):
        self.process.crawl(self.spider)
        self.process.start()
