#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 22:23:32 2020

@author: markd
"""

import tweepy
import argparse
import json
from datetime import datetime
from kafka import KafkaProducer
from secret import *

def initTwitterAPI(api_key, api_secret_key, access_token, access_token_secret):
    auth = tweepy.OAuthHandler(api_key, api_secret_key)
    auth.set_access_token(access_token, access_token_secret)
    return tweepy.API(auth)

class MyStreamListener(tweepy.StreamListener):
    def __init__(self, kafkaPublisher=None, topic=None, debug=False):
        tweepy.StreamListener.__init__(self)
        self.debug = debug
        assert topic, 'topic must be defined'
        self.topic = topic
        self.producer = kafkaPublisher
    
    def publishToKafka(self, message):
        self.producer.send(self.topic, message)
    
    def toJSON(self, timestamp, location, language, text):
        tweetInfo = {}
        tweetInfo['timestamp'] = datetime.strftime(timestamp, '%Y-%m-%d %H:%M:%S')
        tweetInfo['location'] = location
        tweetInfo['language'] = language
        tweetInfo['text'] = text
        return json.dumps(tweetInfo).encode('ascii')
            
    def on_status(self, status):
        try:
            tweet = status.extended_tweet
            text = tweet.full_text
            if text[:2] != "RT" and text[0] != "@":
                if self.producer:
                    # publish to kafka
                    self.publishToKafka(self.toJSON(tweet.created_at, tweet.user.location, status.lang, text))
                    
                if self.debug or not self.producer:
                    print("[{}] {} ({}): {}".format(tweet.created_at, tweet.user.location, status.lang, text))
                    
        except AttributeError:
            tweet = status
            text = tweet.text
            if text[:2] != "RT" and text[0] != "@":
                if self.producer:
                    # publish to kafka
                    self.publishToKafka(self.toJSON(tweet.created_at, tweet.user.location, status.lang, text))
                    
                if self.debug or not self.producer:
                    print("[{}] {} ({}): {}".format(tweet.created_at, tweet.user.location, status.lang, text))

def stream(topic=None, screen_name=None, Async=True, kafkaPublisher=None, debug=False):
    myStreamListener = MyStreamListener(kafkaPublisher=kafkaPublisher, topic=topic, debug=debug)
    api = initTwitterAPI(api_key, api_secret_key, access_token, access_token_secret)
    myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener,)
    if topic:
        myStream.filter(track=topic, is_async=Async)
    elif screen_name:
        myStream.filter(follow=screen_name, is_async=Async)
    else:
        raise ValueError("topic or screen_name must be given")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Stream tweets.')
    parser.add_argument('--topic', type=str, default=None,
                        help='keyword to stream on.')
    parser.add_argument('--screen-name', type=str, default=None,
                        help='screen name whose tweets to stream.')
    parser.add_argument('--synchronous',action='store_false')
    parser.add_argument('--debug',action='store_true', help='print tweets to console.')
    args = parser.parse_args()
    
    topic = args.topic
    screen_name = args.screen_name
    debug = args.debug
    assert topic or screen_name, "either --topic or --screen-name must be passed in."
    
    producer = KafkaProducer(bootstrap_servers=["localhost:29092"])
    
    stream(topic=topic,screen_name=screen_name,Async=args.synchronous, kafkaPublisher=producer, debug=debug)