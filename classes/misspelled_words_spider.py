import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider, IgnoreRequest

class MisspelledWordsSpider(CrawlSpider):
    MAX_PAGES_WITH_MISSPELLS = 10
    MAX_PROCESSED_PAGES = 15

    name = 'misspelled_words_spider'
    pages_with_misspells = 0
    processed_pages = 0
    active = True

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {'classes.misspelled_words_spider.SpiderStatusMiddleware': None},
        'CONCURRENT_REQUESTS': 1,
        'CONCURRENT_ITEMS': 1,
    }

    rules = (
        Rule(LinkExtractor(), callback='parse_page', follow=True),
    )

    def __init__(self, start_url=None, allowed_domains=None, *args, **kwargs):
        super(MisspelledWordsSpider, self).__init__(*args, **kwargs)
        self.start_urls = [start_url]
        self.allowed_domains = allowed_domains
        print "SPIDER INIT url = " + start_url

    def parse_start_url(self, response):
        print "PARSE START"
        return self.parse_page(response)

    def parse_page(self, response):
        if not self.active:
            return None

        self.processed_pages += 1

        # Proccess page
        print "PROCESS PAGE " + str(self.processed_pages)
        # Change pages_with_misspells if misspells founded

        # Disable spider if maximum number of processed pages or pages with misspells is reached
        if self.active:
            if (self.pages_with_misspells >= self.MAX_PAGES_WITH_MISSPELLS):
                print "DISABLE SPIDER"
                self.active = False
                raise CloseSpider('max_pages_with_misspells_reached')

            if (self.processed_pages >= self.MAX_PROCESSED_PAGES):
                print "DISABLE SPIDER"
                self.active = False
                raise CloseSpider('max_processed_pages_reached')

        return None

    """def parse(self, response):
        for href in response.css('.question-summary h3 a::attr(href)'):
            full_url = response.urljoin(href.extract())
            yield scrapy.Request(full_url, callback=self.parse_question)

    def parse_question(self, response):
        yield {
            'title': response.css('h1 a::text').extract()[0],
            'votes': response.css('.question .vote-count-post::text').extract()[0],
            'body': response.css('.question .post-text').extract()[0],
            'tags': response.css('.question .post-tag::text').extract(),
            'link': response.url,
        }"""


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