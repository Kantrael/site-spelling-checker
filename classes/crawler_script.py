# From http://stackoverflow.com/questions/11528739/running-scrapy-spiders-in-a-celery-task
from urlparse import urlparse
from multiprocessing import Process
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy import signals
from classes.misspelled_words_spider import MisspelledWordsSpider
from scrapy.xlib.pydispatch import dispatcher

class CrawlerScript():

    def __init__(self):
        self.crawler_process = CrawlerProcess(get_project_settings())
        self.items = []

    def _item_passed(self, item, response, spider):
        self.items.append(item)

    def crawl(self, url):
        p = Process(target=self._crawl, args=[url])
        p.start()
        p.join()

    def _crawl(self, url):
        domain = urlparse(url).netloc

        self.crawler_process.crawl(MisspelledWordsSpider, start_url=url, allowed_domains=[domain])

        crawler = list(self.crawler_process.crawlers)[0]

        crawler.signals.connect(self._item_passed, signal=signals.item_scraped)

        self.crawler_process.start()
        self.crawler_process.stop()
