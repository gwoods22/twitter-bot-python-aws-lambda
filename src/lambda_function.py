import os
import tweepy
import re


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
        day = int(re.search("\d+", tweets[0].text).group()) + 1
    else:
        day = 1
    tweet = f"Day {day} of asking @Casey to post a DJI Mini 2 Tech Tuesday"

    print(f"Post tweet: {tweet}")
    api.update_status(tweet)

    print("Update bio")
    api.update_profile(
        description = f'Day {day} of tweeting @Casey until he posts a DJI Mini 2 review\n\nMade by @woodzy222'
    )

    return {"statusCode": 200, "tweet": tweet}
