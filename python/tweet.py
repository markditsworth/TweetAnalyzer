#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 22:23:32 2020

@author: markd
"""

import tweepy
import argparse
from secret import *

def initTwitterAPI(api_key, api_secret_key, access_token, access_token_secret):
    auth = tweepy.OAuthHandler(api_key, api_secret_key)
    auth.set_access_token(access_token, access_token_secret)
    return tweepy.API(auth)


class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        try:
            tweet = status.extended_tweet
            if status.lang == 'en':
                text = tweet.full_text
                if text[:2] != "RT":
                    print("[%s] %s: %s"%(tweet.created_at, tweet.user.location, text))
                    
        except AttributeError:
            tweet = status
            if status.lang == 'en':
                text = tweet.text
                if text[:2] != "RT":
                    print("[%s] %s: %s"%(tweet.created_at, tweet.user.location, text))

def stream(topics=[''], screen_names=[''], Async=True):
    myStreamListener = MyStreamListener()
    api = initTwitterAPI(api_key, api_secret_key, access_token, access_token_secret)
    myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
    if topics[0] != '':
        myStream.filter(track=topics, is_async=Async)
    elif screen_names[0] != '':
        myStream.filter(follow=screen_names, is_async=Async)
    else:
        raise ValueError("topics and screen_names must be a list")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Stream tweets.')
    parser.add_argument('--topics', type=str, default='',
                        help='comma-separated list of keywords to stream.')
    parser.add_argument('--screen-names', type=str, default='',
                        help='screen names whose tweets to stream.')
    parser.add_argument('--synchronous',action='store_false')
    args = parser.parse_args()
    
    topics = args.topics.split(',')
    screen_names = args.screen_names.split(',')
    
    stream(topics=topics,screen_names=screen_names,Async=args.synchronous)