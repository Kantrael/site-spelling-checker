# coding=utf-8
from flask import Flask, render_template, json, request
from celery import task
from classes.crawler_script import CrawlerScript
from multiprocessing.queues import Queue

app = Flask(__name__)


# Celery task
@task()
def crawl_url(url):
    # Custom class that controls the Scrapy CrawlerProcess
    queue = Queue()
    crawler = CrawlerScript(queue)
    crawler.crawl(url)
    result_pages = queue.get()
    print "RESULT PAGES: " + str(result_pages)
    return None


# Flask routes
@app.route("/")
def main():
    return render_template('index.html')


@app.route('/check', methods=['POST'])
def check():
    # Read url that user entered in the input field
    _url = request.form['inputUrl']

    # Validate received url
    if _url:
        # Run crawling process in background within Celery task
        #queue = crawl_url(_url)
        crawl_url(_url)
        #print "GET QUEUE"
        #result_pages = queue.get()
        #if result_pages:
        #    # TODO: Do something with this result
        #    print "RESULT PAGES: " + str(result_pages)
        return "Url: " + _url
    else:
        return json.dumps({'html':'<span>Enter the required fields</span>'})

if __name__ == "__main__":
    app.run()
