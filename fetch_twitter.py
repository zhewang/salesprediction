from twython import Twython

twitter = Twython()
results = twitter.get_user_timeline(user_id='amazondeals')

print(results)