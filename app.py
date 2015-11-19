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
    _url = request.form['inputUrl']
    max_pages = parse_max_pages(request.form['maxPages'])
    allowed_words = parse_allowed_words(request.form['allowedWords'])

    # Parse website and collect misspells
    pages = find_misspells(_url, max_pages, allowed_words)

    if pages is False:
        # Return error if the start url was not parsed correctly
        return json.dumps({'error': True})
    else:
        # Return pages with misspells as json
        return json.dumps(pages, cls=misspells_parsing.PageWithMisspellsEncoder)


# Helper methods

def parse_allowed_words(allowed_words_json):
    allowed_words_list = allowed_words_json.split() if allowed_words_json else []

    result = dict()
    for word in allowed_words_list:
        result[word.lower()] = True

    return result


def parse_max_pages(max_pages_json):
    default_pages = 10
    min_pages = 1
    max_pages = 300

    try:
        max_pages_to_show = int(max_pages_json)
    except ValueError:
        max_pages_to_show = default_pages

    max_pages_to_show = max(max_pages_to_show, min_pages)
    max_pages_to_show = min(max_pages_to_show, max_pages)

    return max_pages_to_show


def find_misspells(url, max_pages, allowed_words):
    visited_links = set()
    visiting_links = {url}
    links_to_visit = set()
    pages = []
    current_depth = 0
    max_depth = 5

    while current_depth <= max_depth and len(pages) < max_pages:
        if not visiting_links:
            break

        for link in visiting_links:
            if process_link(link, visited_links, visiting_links, links_to_visit, allowed_words, pages):
                if len(pages) >= max_pages:
                    break
            elif current_depth == 0:
                # If there is an error while parsing first URL - return False
                return False

        visiting_links = links_to_visit.copy()
        links_to_visit.clear()
        current_depth += 1

    return pages


def process_link(link, visited_links, visiting_links, links_to_visit, allowed_words, pages):
    visited_links.add(link)
    page = misspells_parsing.parse(link, allowed_words)
    if page:
        for page_link in page.links:
            if page_link not in visited_links and page_link not in visiting_links:
                links_to_visit.add(page_link)
        page.links = None

        if page.misspells:
            pages.append(page)
        return True
    else:
        return False


if __name__ == "__main__":
    app.run()
