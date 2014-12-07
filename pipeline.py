import json
import os
import pickle
import ebayapi
import glob
import argparse
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
            results.append(keyword['text'])
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

def ProcessTweet(tweet, dataPath):
    # make dir for a tweet
    tweet_dir = dataPath+'/'+tweet['user']['screen_name']+'/'+tweet['id_str']
    if os.path.isdir(tweet_dir) == False:
        os.mkdir(tweet_dir)
    
    keywords = ExtractKeyword(tweet['text'])
    # print(kewwords)

    # ExtractEntity(tweet['text'])
    # ExtractTaxonomy(demo_text)
    # ExtractImageTag(image_url)

    # Search on ebay for sales data
    if len(keywords) > 0:
        ebayapi.SearchEbay(keywords, tweet_dir)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('datapath', help='Path of data files. For example "./data"')
    args = parser.parse_args()
    
    dataPath = args.datapath

    pool = Pool(10)
    files = glob.glob(dataPath+"/*.t")
    # print(files)
    for f in files:
        tweets = pickle.load(open(f, 'rb'))

        # make dir for an account
        account_dir = dataPath+'/'+tweets[0]['user']['screen_name']
        print(account_dir)

        if os.path.isdir(account_dir)==False:
            os.mkdir(account_dir)

        for t in tweets:
            ProcessTweet(t, dataPath)
            # print(t['created_at'])
            # print(t['retweet_count'])
            # print(t['text'].encode('utf-8'))

