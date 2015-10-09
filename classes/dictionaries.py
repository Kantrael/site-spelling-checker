import os

def init():
    # Dictionary path
    script_dir = os.path.dirname(__file__)
    rel_path = "../dict/wordlist-en_US-large-2015.08.24/en_US-large.txt"
    en_path = os.path.join(script_dir, rel_path)

    # Open english dictionary file an load it to dictionary variable
    en_file = open(en_path).readlines()
    en_file = map(lambda x: x.strip(), en_file)

    # Define global dict and put all words to it
    global english
    english = dict()
    for word in en_file:
        english[word] = True

init()
