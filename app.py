# coding=utf-8
from flask import Flask, render_template, json, request
from celery import task
from classes.crawler_script import CrawlerScript

app = Flask(__name__)

# Custom class that controls the Scrapy's CrawlerProcces
crawler = CrawlerScript()

# Celery task
@task()
def crawl_url(url):
    return crawler.crawl(url)

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
        # Run crawling proccess in background
        crawl_url(_url)
        return "Url: " + _url
    else:
        return json.dumps({'html':'<span>Enter the required fields</span>'})

if __name__ == "__main__":
    app.run()
