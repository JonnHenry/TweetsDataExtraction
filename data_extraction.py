import os
import tweepy as tw
import pandas as pd
from Credentials import dataAPI
import json

consumer_key= dataAPI['API key']
consumer_secret= dataAPI['API secret key']
access_token= dataAPI['Access token']
access_token_secret= dataAPI['Access token secret']

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

search_words = "'Andres Arauz' OR ecuarauz OR Arauz -is:nullcast"
date_since = "2020-10-8" # Fin de las inscripciones de las candidaturas 2020-10-8, la campaña electoral oficial es desde 31 de diciembre – 04 de febrero de 2021

def get_data_Twitter(api_object,query,languaje,num_items,data_since,columns_df):
    dictionary_data = {}
    tweets = tw.Cursor(api_object.search,q=query,lang=languaje,since=data_since).items(num_items)
    for tweet in tweets:
        print(tweet)

    return pd.DataFrame(data = dictionary_data,columns=columns_df)
        
tweets = tw.Cursor(api.search, q=search_words,lang="es",since=date_since,tweet_mode='extended').items(3)

# Iterate and print tweets
for tweet in tweets:
    #print(tweet._json,)
    data = json.dumps(tweet._json,indent=2) #Data converted to JSON
    #load_data = json.loads(data)
    #print(json.dumps(load_data["user"],indent=2))
    print(data)
    print("\n\n\n\n\n\n")