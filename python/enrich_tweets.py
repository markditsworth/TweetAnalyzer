#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 09:40:56 2020

@author: markd
"""

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
import argparse
import json
from kafka import KafkaProducer
from kafka import KafkaConsumer

def parse_args():
    parser = argparse.ArgumentParser(description='Add NLP information about tweets.')
    parser.add_argument('--topic', type=str, default=None,
                        help='topic housing the tweets.')
    parser.add_argument('--host', type=str, default=None,
                        help='hostname of the kafka broker.')
    parser.add_argument('--port', type=str, default=None,
                        help='port number of the kafka broker.')
    parser.add_argument('--debug',action='store_true', help='print raw and enriched messages to console.')
    parser.add_argument('--no-produce', action='store_false', help='do not publish to kafka.')
    return parser.parse_args()

class TweetNLP:
    def __init__(self):
        try:
            self.Vader = SIA()
        except LookupError:
            nltk.download('vader_lexicon')
            self.Vader = SIA()

    def add_nlp(self, data):
        enriched_data = data.copy()
        if data['language'] == 'en':
            enriched_data['polarity_scores'] = self.getVaderSentiment(data['text'])
        else:
            enriched_data['polarity_scores'] = None
        return enriched_data
    
    def getVaderSentiment(self, text):
        return self.Vader.polarity_scores(text)
    

class Kafka(TweetNLP):
    def __init__(self, host, port, topic, debug=False, produce=True):
        super().__init__()
        self.consumer = KafkaConsumer(topic, group_id='{}-consumer-group5'.format(topic),
                                      bootstrap_servers=["{}:{}".format(host,port)],
                                      auto_offset_reset='earliest',
                                      value_deserializer=lambda m: json.loads(m.decode('ascii')))
        self.producer = KafkaProducer(bootstrap_servers=["{}:{}".format(host,port)])
        self.dest_topic = 'enriched-' + topic
        self.debug = debug
        self.produce = produce
    
    def serialize(self, dictionary):
        return json.dumps(dictionary).encode('ascii')
    
    def enrich(self):
        for m in self.consumer:
            message = m.value
            if self.debug and False:
                print("Raw message:")
                print(message)
                print("")
            enriched_message = self.add_nlp(message)
            if self.debug:
                print("Enriched message:")
                print(enriched_message)
                print("")
            if self.produce:
                self.producer.send(self.dest_topic, self.serialize(enriched_message))


if __name__ == '__main__':
    args = parse_args()
    
    topic = args.topic
    host = args.host
    port = args.port
    debug = args.debug
    produce = args.no_produce
    
    kafka = Kafka(host, port, topic, debug=debug, produce=produce)
    kafka.enrich()
    
    
    
