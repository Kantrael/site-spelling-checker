# From http://stackoverflow.com/questions/11528739/running-scrapy-spiders-in-a-celery-task
from urlparse import urlparse
from multiprocessing import Process
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy import signals
from classes.misspelled_words_spider import MisspelledWordsSpider


class CrawlerScript:

    def __init__(self, result_queue):
        self.crawler_process = CrawlerProcess(get_project_settings())
        self.items = []
        self.result_queue = result_queue

    def _item_passed(self, item, response, spider):
        print "APPEND ITEM"
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

        print "PUT RESULTS TO QUEUE"

        print len(self.items)
        self.result_queue.put(self.items)
        print "AFTER PUTTING"
