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

    current_depth = 0
    max_depth = 0
    visited_links = set()
    visiting_links = ([_url])
    links_to_visit = set()
    pages = []

    while current_depth <= max_depth:
        for link in visiting_links:
            visited_links.add(link)

            page = misspells_parsing.parse(link)
            if page:
                for page_link in page.links:
                    if page_link not in visited_links and page_link not in visiting_links:
                        links_to_visit.add(page_link)
                page.links = None

                pages.append(page)
            else:
                # If there is an error while parsing first URL - send it to the browser
                if current_depth == 0:
                    return json.dumps({'error': True})

        visiting_links = links_to_visit.copy()
        links_to_visit.clear()
        current_depth += 1

    # Return pages with misspells as json
    return json.dumps(pages, cls = misspells_parsing.PageWithMisspellsEncoder)

if __name__ == "__main__":
    app.run()
