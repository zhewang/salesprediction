#!/usr/bin/env python

from __future__ import print_function
from alchemyapi import AlchemyAPI
import json

import ebayapi


demo_text = 'Yesterday dumb Bob destroyed my fancy iPhone in beautiful Denver, Colorado. I guess I will have to head over to the Apple Store and buy a new one.'
demo_url = 'http://www.npr.org/2013/11/26/247336038/dont-stuff-the-turkey-and-other-tips-from-americas-test-kitchen'
demo_html = '<html><head><title>Python Demo | AlchemyAPI</title></head><body><h1>Did you know that AlchemyAPI works on HTML?</h1><p>Well, you do now.</p></body></html>'
image_url = 'http://demo1.alchemyapi.com/images/vision/football.jpg'


# Create the AlchemyAPI Object
alchemyapi = AlchemyAPI()

############################################
#   Entity Extraction Example              #
############################################

print('Processing text: ', demo_text)
print('')

response = alchemyapi.entities('text', demo_text, {'sentiment': 1})

if response['status'] == 'OK':
    # print('## Response Object ##')
    # print(json.dumps(response, indent=4))

    print('')
    print('## Entities ##')
    for entity in response['entities']:
        print('text: ', entity['text'].encode('utf-8'))
        print('type: ', entity['type'])
        print('relevance: ', entity['relevance'])
        print('sentiment: ', entity['sentiment']['type'])
        if 'score' in entity['sentiment']:
            print('sentiment score: ' + entity['sentiment']['score'])
        print('')
else:
    print('Error in entity extraction call: ', response['statusInfo'])


############################################
#   Keyword Extraction Example             #
############################################

response = alchemyapi.keywords('text', demo_text, {'sentiment': 1})

if response['status'] == 'OK':
    # print('## Response Object ##')
    # print(json.dumps(response, indent=4))

    print('')
    print('## Keywords ##')
    for keyword in response['keywords']:
        print('text: ', keyword['text'].encode('utf-8'))
        print('relevance: ', keyword['relevance'])
        print('sentiment: ', keyword['sentiment']['type'])
        if 'score' in keyword['sentiment']:
            print('sentiment score: ' + keyword['sentiment']['score'])
        print('')
else:
    print('Error in keyword extaction call: ', response['statusInfo'])


############################################
#   Taxonomy  Example                      #
############################################

response = alchemyapi.taxonomy('text', demo_text)

if response['status'] == 'OK':
    # print('## Response Object ##')
    # print(json.dumps(response, indent=4))

    print('')
    print('## Categories ##')
    for category in response['taxonomy']:
        print(category['label'], ' : ', category['score'])
    print('')

else:
    print('Error in taxonomy call: ', response['statusInfo'])

############################################
#   Image tagging Example                  #
############################################


response = alchemyapi.imageTagging('url', image_url)

if response['status'] == 'OK':
    # print('## Response Object ##')
    # print(json.dumps(response, indent=4))

    print('')
    print('## Image Keywords ##')
    for keyword in response['imageKeywords']:
        print(keyword['text'], ' : ', keyword['score'])
    print('')
else:
    print('Error in image tagging call: ', response['statusInfo'])

print('')
print('')
