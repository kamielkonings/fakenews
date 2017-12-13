import sys
import urllib
import json
from random import choice, randint
import xml.etree.ElementTree as ET
from pattern.nl import parse, split

ns = {
    'dc': 'http://purl.org/dc/elements/1.1/',
    'content': 'http://purl.org/rss/1.0/modules/content/',
    'media': 'http://search.yahoo.com/mrss/'
}


def fakenewsify(title, trends,num):
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
    random_trend_index = num
    ###random_trend_index = randint(0, len(trends) - 1)
    words = [word_data[0] for word_data in first_sentence]
    words[index_to_replace] = trends[random_trend_index]
    del trends[random_trend_index]

    new_sentence = ' '.join(words)
    return new_sentence


def do_fetch(publication='demorgen'):
    if publication == 'demorgen':
        urllib.urlretrieve('https://www.demorgen.be/rss.xml', 'demorgen.xml')
    elif publication == 'hln':
        urllib.urlretrieve('https://www.hln.be/rss.xml', 'hln.xml')
    urllib.urlretrieve('http://hawttrends.appspot.com/api/terms/',
                       'trends.json')


def do_generate(publication='demorgen'):
    all_trends = json.load(open('trends.json'))
    local_trends = all_trends['41']  # Belgie

    tree = ET.parse(publication + '.xml')
    root = tree.getroot()

    fake_items = []

    for item in root.find('channel').findall('item'):
        if len(local_trends) == 0: break
        title = item.find('title').text
        random_trend = randint(0, len(local_trends) - 1)
        fake_title = fakenewsify(title, local_trends,random_trend)
        if fake_title is None:
            continue

        image = item.find('content:encoded', ns)
        if image is None:
            image = item.find('media:content', ns)
            if image is None:
                continue
        image = image.text or image.get('url')

        fake_items.append({'title': fake_title, 'local_trend':local_trends[0],'image': image})
    return fake_items


def get_trends():
    all_trends = json.load(open('trends.json'))
    local_trends = all_trends['41']  # Belgie


    return local_trends

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
            print item['local_trend']