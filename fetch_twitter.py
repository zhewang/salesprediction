from twython import Twython
import pickle

def GetTimeline(conn, user_id):
    results = conn.get_user_timeline(screen_name=user_id, count='200', exclude_replies='true')
    # results = twitter.search(q='@hp', count='5', until='2014-11-20')

    # readFile = open('tData.txt', 'rb')
    # results = pickle.load(readFile)

    for i in results:
        print(i['created_at'])
        print(i['retweet_count'])
        print(i['text'].encode('utf-8'))
        print(i['id'])
        print(i['user']['screen_name'])
        print("-------------------")

    saveFile = open('./data/'+user_id,'wb')
    pickle.dump(results, saveFile)
    saveFile.close()

def FetchData(id_list):

    ids = ['hp','eBay']

    APP_KEY = u'4MBVh0blR8toU4TZxPWl0yuwG'
    APP_SECRET = u'ZZe1zSflBXCXJopVyJ1x5uZHuwjXTCMmtDXfDwZL7FNLKbHAtP'
    OAUTH_TOKEN = u'2918875315-1dggMat8yFvQcQEccMqQ1LmPoZhr6j21KI669VY'
    OAUTH_TOKEN_SECRET = u'X7uULxPje1dqx5sfFFNekKMmzHkmNXe9gM5NSfZIxEu9B'

    twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

    for uid in ids:
        GetTimeline(twitter, uid)

if __name__ == '__main__':
    FetchData('test')

