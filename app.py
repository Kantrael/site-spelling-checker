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
    _max_pages = request.form['maxPages']

    min_pages = 1
    default_pages = 10
    max_pages = 300

    try:
        max_pages_to_show = int(_max_pages)
    except ValueError:
        max_pages_to_show = default_pages

    if max_pages_to_show < min_pages:
        max_pages_to_show = min_pages

    if max_pages_to_show > max_pages:
        max_pages_to_show = max_pages

    current_depth = 0
    max_depth = 5
    visited_links = set()
    visiting_links = set([_url])
    links_to_visit = set()
    pages = []

    while current_depth <= max_depth and len(pages) < max_pages_to_show:
        if len(visiting_links) == 0:
            break

        for link in visiting_links:
            visited_links.add(link)

            page = misspells_parsing.parse(link)
            if page:
                for page_link in page.links:
                    if page_link not in visited_links and page_link not in visiting_links:
                        links_to_visit.add(page_link)
                page.links = None

                if len(page.misspells) > 0:
                    print "Added page: " + page.url
                    pages.append(page)
                    if not len(pages) < max_pages_to_show:
                        break
            else:
                # If there is an error while parsing first URL - send it to the browser
                if current_depth == 0:
                    return json.dumps({'error': True})

        visiting_links = links_to_visit.copy()
        #print "links to visit: " + str(len(visiting_links))
        links_to_visit.clear()
        current_depth += 1

    print "visiting_links = " + str(len(visiting_links))
    print "current_depth = " + str(current_depth)
    print "len(pages) = " + str(len(pages))

    # Return pages with misspells as json
    return json.dumps(pages, cls = misspells_parsing.PageWithMisspellsEncoder)

if __name__ == "__main__":
    app.run()
