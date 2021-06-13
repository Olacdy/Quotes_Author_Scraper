import os
import crochet
from flask import Flask
from Scraper import Scraper
from quotes_author.spiders.QuotesAuthorSpider import QuotesAuthorSpider


port = int(os.environ.get("PORT", 5000))
app = Flask(__name__)
crochet.setup()


@app.route('/get_items')
def get_items():
    scraper = Scraper(QuotesAuthorSpider)
    scraper.run_spider()

    while not scraper.is_closed:
        continue

    return scraper.get_output_data()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=port)

