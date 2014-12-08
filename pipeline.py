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

    response = alchemyapi.taxonomy('text', text)
    results = []

    if response['status'] == 'OK':
        for category in response['taxonomy']:
            results.append(category['label'] + ' : ' + category['score'])
    else:
        print('Error in taxonomy call: ', response['statusInfo'])

    return results


def ExtractImageTag(image_url):
    alchemyapi = AlchemyAPI()

    response = alchemyapi.imageTagging('url', image_url)
    results = []

    if response['status'] == 'OK':
        for keyword in response['imageKeywords']:
            results.append(keyword['text'])
            # print(keyword['text'], ' : ', keyword['score'])
        print('')
    else:
        print('Error in image tagging call: ', response['statusInfo'])

def ProcessTweet(tweet, dataPath):
    # make dir for a tweet
    tweet_dir = dataPath+'/'+tweet['user']['screen_name']+'/'+tweet['id_str']
    if os.path.isdir(tweet_dir) == False:
        os.mkdir(tweet_dir)
    
    # save tweet text
    tweet_info = open(tweet_dir+'/tweet.txt', 'w')

    # # get image url
    # imageTags = []
    # if 'media' in tweet['entities']:
    #     imageTags = ExtractImageTag(tweet['entities']['media'][0]['expanded_url'])
    #     print(imageTags)

    keywords = ExtractKeyword(tweet['text'])
    # print(kewwords)

    # ExtractEntity(tweet['text'])
    category = ExtractTaxonomy(tweet['text'])
    # ExtractImageTag(image_url)

    tweet_info.write(tweet['text']+'\n\n')
    tweet_info.write(', '.join(keywords)+'\n')
    tweet_info.write(', '.join(category)+'\n')
    tweet_info.close()

    # Search on ebay for sales data
    if len(keywords) > 0:
        ebayapi.SearchEbay(keywords, tweet_dir)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('datapath', help='Path of data files. For example "./data"')
    parser.add_argument('limit', default=0, type=int, help='Limit of number of tweets for each account.')

    args = parser.parse_args()
    
    dataPath = args.datapath
    t_limit = args.limit

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

        if t_limit == 0:
            for t in tweets:
                ProcessTweet(t, dataPath)
        else:
            maxnumber = min(t_limit, len(tweets))
            for i in range(maxnumber):
                ProcessTweet(tweets[i], dataPath)
            # print(t['created_at'])
            # print(t['retweet_count'])
            # print(t['text'].encode('utf-8'))

