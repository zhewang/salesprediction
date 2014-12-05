from twython import Twython

APP_KEY = u'4MBVh0blR8toU4TZxPWl0yuwG'
APP_SECRET = u'ZZe1zSflBXCXJopVyJ1x5uZHuwjXTCMmtDXfDwZL7FNLKbHAtP'
OAUTH_TOKEN = u'2918875315-1dggMat8yFvQcQEccMqQ1LmPoZhr6j21KI669VY'
OAUTH_TOKEN_SECRET = u'X7uULxPje1dqx5sfFFNekKMmzHkmNXe9gM5NSfZIxEu9B'

twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

results = twitter.get_user_timeline(screen_name=u'hp', count='2')

for i in results:
    print(i['created_at'])
    print(i['retweet_count'])
    print(i['text'])
    print("-------------------")