import json
import os
import pickle
import ebayapi
import glob
from multiprocessing import Pool
from alchemyapi import AlchemyAPI

def ExtractEntity(text):
    # Create the AlchemyAPI Object
    alchemyapi = AlchemyAPI()

    response = alchemyapi.entities('text', text, {'sentiment': 1})

    if response['status'] == 'OK':
        for entity in response['entities']:
            print('text: ', entity['text'].encode('utf-8'))
            print('type: ', entity['type'])
            print('relevance: ', entity['relevance'])
    else:
        print('Error in entity extraction call: ', response['statusInfo'])

def ExtractKeyword(text):
    alchemyapi = AlchemyAPI()

    response = alchemyapi.keywords('text', text, {'sentiment': 1})
    results = []
    if response['status'] == 'OK':
        for keyword in response['keywords']:
            results.append(keyword['text'].encode('utf-8'))
            # print('text: ', keyword['text'].encode('utf-8'))
            # print('relevance: ', keyword['relevance'])
    else:
        print('Error in keyword extaction call: ', response['statusInfo'])

    return results


def ExtractTaxonomy(text):
    alchemyapi = AlchemyAPI()

    response = alchemyapi.taxonomy('text', demo_text)

    if response['status'] == 'OK':
        for category in response['taxonomy']:
            print(category['label'], ' : ', category['score'])
    else:
        print('Error in taxonomy call: ', response['statusInfo'])


def ExtractImageTag(image_url):
    alchemyapi = AlchemyAPI()

    response = alchemyapi.imageTagging('url', image_url)

    if response['status'] == 'OK':
        for keyword in response['imageKeywords']:
            print(keyword['text'], ' : ', keyword['score'])
        print('')
    else:
        print('Error in image tagging call: ', response['statusInfo'])

def ProcessTweet(tweet):

    # ExtractEntity(tweet['text'])
    keywords = ExtractKeyword(tweet['text'])
    print(kewwords)
    # ExtractTaxonomy(demo_text)
    # ExtractImageTag(image_url)

    # Search on ebay for sales data
    if len(keywords) > 0:
        SearchEbay(keywords)


if __name__ == '__main__':
    
    dataPath = "./data/"    

    pool = Pool(10)
    files = glob.glob(dataPath+"*.t")
    # print(files)
    for f in files:
        tweets = pickle.load(open(f, 'rb'))
        pool.map_async(ProcessTweet, tweets)
        # for t in tweets:
            # ProcessTweet(t)
            # print(t['created_at'])
            # print(t['retweet_count'])
            # print(t['text'].encode('utf-8'))

    pool.close()
    pool.join()
