# From http://stackoverflow.com/questions/11528739/running-scrapy-spiders-in-a-celery-task
from urlparse import urlparse
from multiprocessing import Process
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from classes.misspelled_words_spider import MisspelledWordsSpider

class CrawlerScript():

    def __init__(self):
        self.crawler = CrawlerProcess(get_project_settings())

    def _crawl(self, url):
        print "Entered URL: " + url

        domain = urlparse(url).netloc
        print "Domain is: " + domain

        self.crawler.crawl(MisspelledWordsSpider, start_url=url, allowed_domains=[domain])
        self.crawler.start()
        self.crawler.stop()

    def crawl(self, url):
        p = Process(target=self._crawl, args=[url])
        p.start()
        p.join()

    def stop(self):
        self.crawler.stop()
        
