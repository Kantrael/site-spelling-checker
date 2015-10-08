# coding=utf-8
from flask import Flask, render_template, json, request
from classes import misspells_parsing

app = Flask(__name__)
app.debug = True


# Flask routes
@app.route("/")
def main():
    return render_template('index.html')


@app.route('/check', methods=['POST'])
def check():
    # Read url that user entered in the input field
    _url = request.form['inputUrl']
    print "URL: " + _url

    current_depth = 0
    max_depth = 0
    visited_links = set()
    visiting_links = set([_url])
    links_to_visit = set()
    pages = []

    while current_depth <= max_depth:
        print "DEPTH " + str(current_depth)
        for link in visiting_links:
            #print "GET LINK " + link + "AND ADD IT TO VISITED"
            visited_links.add(link)

            page = misspells_parsing.parse(link)
            if page:
                #print "PAGE RECEIVED"
                for page_link in page.links:
                    if page_link not in visited_links and page_link not in visiting_links:
                        #print "PAGE'S LINK IS NEW: " + page_link
                        links_to_visit.add(page_link)
                #print "OUTSIDE OF A LOOP"
                page.links.clear()
                #print "AFTER NULLING"

                pages.append(page)

        print "HERE"
        print "VISITED LINKS COUNT = " + str(len(visited_links))
        print "VISITING LINKS COUNT = " + str(len(visiting_links))
        print "LINKS TO VISIT COUNT = " + str(len(links_to_visit))
        visiting_links = links_to_visit.copy()
        links_to_visit.clear()
        print "THERE"
        print "VISITED LINKS COUNT = " + str(len(visited_links))
        print "VISITING LINKS COUNT = " + str(len(visiting_links))
        print "LINKS TO VISIT COUNT = " + str(len(links_to_visit))
        current_depth += 1

    print "FINAL PAGES COUNT = " + str(len(pages))
    print "TEST WORDS: "
    print str(pages[0].misspells)

    if _url:
        return "Url: " + _url
    else:
        return json.dumps({'html': '<span>Enter the required fields</span>'})

if __name__ == "__main__":
    app.run()
