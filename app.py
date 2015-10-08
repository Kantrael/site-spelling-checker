# coding=utf-8
from flask import Flask, render_template, json, request
from classes import misspells_parsing

app = Flask(__name__)


# Flask routes
@app.route("/")
def main():
    return render_template('index.html')


@app.route('/check', methods=['POST'])
def check():
    # Read url that user entered in the input field
    _url = request.form['inputUrl']
    print "URL: " + _url

    page = misspells_parsing.parse(_url)
    print "LINKS:"
    for link in page.links:
        print link

    # Validate received url
    if _url:
        print "Request for parsing: " + _url

        return "Url: " + _url
    else:
        return json.dumps({'html': '<span>Enter the required fields</span>'})

if __name__ == "__main__":
    app.run()
