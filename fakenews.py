import sys
import urllib
import json
from random import choice
import xml.etree.ElementTree as ET
from pattern.nl import parse, split

ns = {
    'dc': 'http://purl.org/dc/elements/1.1/',
    'content': 'http://purl.org/rss/1.0/modules/content/'
}


def fakenewsify(title):
    s = parse(title)
    sentences = s.split()
    first_sentence = sentences[0]
    new_sentence_words = []

    tags = [word_data[1] for word_data in first_sentence]
    tag_indices = []
    for i, word_data in enumerate(first_sentence):
        tag = word_data[1]
        if tag == 'NNP':
            tag_indices.append(i)
    if len(tag_indices) == 0:
        return None
    index_to_replace = choice(tag_indices)

    words = [word_data[0] for word_data in first_sentence]
    words[index_to_replace] = choice(TRENDS)
    new_sentence = ' '.join(words)
    return new_sentence


def do_fetch():
    urllib.urlretrieve('https://www.demorgen.be/rss.xml', 'demorgen.xml')
    urllib.urlretrieve('https://www.hln.be/rss.xml', 'hln.xml')
    urllib.urlretrieve('http://hawttrends.appspot.com/api/terms/',
                       'trends.json')


def do_generate():
    global TRENDS
    trends = json.load(open('trends.json'))
    TRENDS = trends['41']  # Belgie

    tree = ET.parse('demorgen.xml')
    root = tree.getroot()

    fake_items = []

    for item in root.find('channel').findall('item'):
        title = item.find('title').text
        fake_title = fakenewsify(title)
        if fake_title is None:
            continue

        image = item.find('content:encoded', ns)
        if image is None:
            continue
        image = image.text

        fake_items.append({'title': fake_title, 'image': image})
    return fake_items


def usage():
    print "python fakenews.py [command]"
    print "command is:"
    print "    fetch: fetch new news items"
    print "    generate: generate fake news items"


if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()
        sys.exit(0)
    command = sys.argv[1]
    if command == 'fetch':
        do_fetch()
    elif command == 'generate':
        items = do_generate()
        for item in items:
            print item['title']
