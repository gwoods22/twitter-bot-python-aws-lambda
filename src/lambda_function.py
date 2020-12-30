import os
import tweepy
import re

def suffix(number):
    last_two = int(str(number)[-2:])
    last_digit = int(str(number)[-1:])
    if last_two == 11 or last_two == 12 or last_two == 13:
        return "th"
    elif last_digit == 1:
        return "st"
    elif last_digit == 2:
        return "nd"
    elif last_digit == 3:
        return "rd"
    else:
        return "th"

def lambda_handler(event, context):
    print("Get credentials")
    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")
    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

    print("Authenticate")
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    print("Get last tweet to increment day")
    tweets = api.user_timeline()
    if len(tweets) > 0:
        count = int(re.search("\d+", tweets[0].text).group()) + 1
    else:
        count = 1

    tweet = f"Asking @DavidDobrik to post a vlog for the {count}{suffix(count)} time."

    print(f"Post tweet: {tweet}")
    api.update_status(tweet)

    print("Update bio")
    api.update_profile(
        description = f'Tweeting @DavidDobrik every hour until he posts a vlog.\n{count} tweets so far.\n\nMade by @woodzy222'
    )

    return {"statusCode": 200, "tweet": tweet}
