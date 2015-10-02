import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider, IgnoreRequest
from scrapy.selector import Selector
import re

class PageWithMispells(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    mispells = scrapy.Field()

class MisspelledWordsSpider(CrawlSpider):
    MAX_PAGES_WITH_MISSPELLS = 1
    MAX_PROCESSED_PAGES = 1

    name = 'misspelled_words_spider'
    pages_with_misspells = 0
    processed_pages = 0
    active = True

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {'classes.misspelled_words_spider.SpiderStatusMiddleware': None}
    }

    rules = (
        Rule(LinkExtractor(), process_links='process_links', callback='parse_page', follow=True),
    )

    def __init__(self, start_url=None, allowed_domains=None, *args, **kwargs):
        super(MisspelledWordsSpider, self).__init__(*args, **kwargs)
        self.start_urls = [start_url]
        self.allowed_domains = allowed_domains

    def parse_start_url(self, response):
        page = self.process_page(response)
        if page:            
            yield page

    def parse_page(self, response):
        page = self.process_page(response)
        if page:            
            yield page

    def process_page(self, response):
        if not self.active:
            raise CloseSpider('this spider is not active anymore')
        elif (response.status == 200):
            # Process page
            print "PROCESS PAGE " + response.url

            title = response.selector.xpath('//title/text()').extract()

            # TODO: Change pages_with_misspells if misspells founded

            words = response.xpath('//text()').re(r'\w+')
            mispells = []
            for word in words:
                # Test condition, will be changed to real mispell checking
                if "w" in word and "o" in word:
                    mispells.append(word)

            page = PageWithMispells(url=response.url)
            page['title'] = title
            page['mispells'] = mispells

            self.processed_pages += 1

            # Disable spider if maximum number of processed pages or pages with misspells is reached
            if (self.pages_with_misspells >= self.MAX_PAGES_WITH_MISSPELLS or self.processed_pages >= self.MAX_PROCESSED_PAGES):
                print "DISABLE SPIDER, pages processed: " + str(self.processed_pages)
                self.active = False

            #print "RETURNING PARSED INFO: " + response.url
            return page

    # Check that url links on a valid page (not .txt file)
    def process_links(self, links):
        valid_links = []
        for link in links:
            if not link.url.endswith(".txt"):
                valid_links.append(link)
        return valid_links

# Ignores spider's request and responses if spider.active is set to False
class SpiderStatusMiddleware():

    def process_request(self, request, spider):
        if not spider.active:
            raise IgnoreRequest()
        return None

    def process_response(self, request, response, spider):
        if not spider.active:
            raise IgnoreRequest()
        return response