from bs4 import BeautifulSoup
from urllib2 import urlopen, URLError
from httplib import InvalidURL
from urlparse import urlparse
import re
import dictionaries
import json


class PageWithMisspells:
    def __init__(self):
        self.url = None
        self.title = None
        self.misspells = dict()
        self.links = set()


class PageWithMisspellsEncoder(json.JSONEncoder):
    def default(self, obj):
        if not isinstance(obj, PageWithMisspells):
            return super(PageWithMisspellsEncoder, self).default(obj)

        return obj.__dict__


def parse(url, allowed_words):
    #print "Parse " + str(url)
    if not url:
        #print "error not url"
        return None

    if not url.startswith('http'):
        url = "http://" + url

    try:
        content = urlopen(url)
    except (URLError, ValueError, InvalidURL), ex:
        #print "error " + str(ex)
        return None

    content_type = content.info()['Content-Type']
    if not content_type or "text/html" not in content_type:
        #print "error not text/html"
        return None

    page = PageWithMisspells()
    try:
        soup = BeautifulSoup(content, "lxml")

        page.url = url
        if soup.title:
            page.title = soup.title.string
        else:
            page.title = url
        page.misspells = __get_words(soup, allowed_words)
        page.links = __get_internal_links(soup, url)
    except AttributeError:
        #print "error AttributeError"
        return None

    #print "return page"
    return page


def __get_words(soup, allowed_words):
    if not allowed_words:
        allowed_words = dict()

    # kill all unnecessary elements
    for script in soup(["script", "style", "[document]", "head", "title", "meta"]):
        script.extract()    # rip it out

    # get content
    content = " ".join(soup.strings)

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in content.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    content = '\n'.join(chunk for chunk in chunks if chunk)
    content = content.encode('utf-8')

    # split text blob into words excluding all that isn't a word
    words = []
    for word in re.findall(r"[A-Za-z]+", content):
        if len(word) > 1:
            words.append(word.lower())

    words_with_misspells = dict()
    for word in words:
        if dictionaries.english.has_key(word) or allowed_words.has_key(word):
            continue

        if word not in words_with_misspells:
            words_with_misspells[word] = 1
        else:
            words_with_misspells[word] += 1

    return words_with_misspells


def __get_internal_links(soup, current_url):
    parts = urlparse(current_url)
    scheme = parts.scheme
    netloc = parts.netloc
    page_links = set()
    try:
        for link in [h.get('href') for h in soup.find_all('a')]:
            # Skip broken urls and urls that links on current page
            if not link or link.startswith("#"):
                continue

            # Correct double-slashed links
            if link.startswith("//"):
                link = scheme + '://' + link[2:]

            final_link = link
            if not link.startswith('http'):
                # Correct relational links
                if link.startswith('/'):
                    final_link = scheme + '://' + netloc + link
                else:
                    if current_url.endswith("/"):
                        final_link = current_url + link
                    else:
                        final_link = current_url + "/" + link
            else:
                # Check if link is internal
                domain = netloc
                if domain.startswith("www"):
                    domain = domain[3:]

                if domain not in urlparse(final_link).netloc:
                    # Skip external links
                    continue

            # Check if link is already added
            page_links.add(final_link)

    except Exception, ex:  # Magnificent exception handling
        print ex

    return page_links
