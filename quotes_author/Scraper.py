import os
from flask import jsonify
from scrapy import signals
from inspect import isclass
from scrapy.crawler import CrawlerRunner
from scrapy.signalmanager import dispatcher
import quotes_author.pipelines as pipelines
from scrapy.utils.project import get_project_settings


class Scraper:
    def __init__(self, spider, output_format='json'):
        self.output_data = []
        self.is_closed = False
        settings_file_path = 'quotes_author.settings'
        os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
        settings = get_project_settings()
        classes = [x for x in dir(pipelines) if isclass(getattr(pipelines, x))]
        matching = [s for s in classes if output_format.lower() in s.lower()][0]
        settings.update(
            {
                "ITEM_PIPELINES": {
                    f'quotes_author.pipelines.{matching}': 1
                }
            }
        )
        self.process = CrawlerRunner(settings)
        self.spider = spider

    def run_spider(self):
        dispatcher.connect(self._crawler_result, signal=signals.item_scraped)
        self.process.crawl(self.spider, self)

    def _crawler_result(self, item, response, spider):
        self.output_data.append(dict(item))

    def get_output_data(self):
        return jsonify(self.output_data)

