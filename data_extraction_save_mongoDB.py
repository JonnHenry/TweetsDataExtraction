import os
import tweepy as tw
from Credentials import dataAPI
import json
from pymongo import MongoClient

consumer_key= dataAPI['API key']
consumer_secret= dataAPI['API secret key']
access_token= dataAPI['Access token']
access_token_secret= dataAPI['Access token secret']

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

MONGO_HOST= 'mongodb://localhost/'  # assuming you have mongoDB installed locally
                                             # and a database called 'twitterdb'


client = MongoClient(MONGO_HOST)

def get_data_Twitter(api_object,query,languaje,num_items,data_since,data_until,mongo_client):
    try:
        db = client.twitterdb
        tweets = tw.Cursor(api_object.search,q=query,lang=languaje,since=data_since,data_until=data_until,tweet_mode='extended').items(num_items)
        for tweet in tweets:
            datajson = json.loads(json.dumps(tweet._json)) 
            created_at = datajson['created_at']
            print("Tweet collected at " + str(created_at))
            #db.twitter_search_arauz.insert_one(datajson)
            #db.twitter_search_lasso.insert_one(datajson)
            db.twitter_search_hervas.insert_one(datajson)
    except Exception as e:
           print(e)

#search_words = "'Andres Arauz' OR 'Andrés Arauz' OR ecuarauz OR Arauz OR 'ANDRES ARAUZ'-is:nullcast "
#search_words = "'Guillermo Lasso' OR LassoGuillermo OR Lasso OR 'GUILLERMO LASSO' OR LASSO -is:nullcast"
search_words = "'Xavier Hervas' OR xhervas OR 'XAVIER HERVAS' OR 'XAVIER hervas' OR 'xavier HERVAS' -is:nullcast" 
#search_words = "'Yaku Pérez Guartambel' OR yakuperezg OR 'Yaku Pérez' OR YakuEs OR 'YAKU PEREZ' OR Yaku OR 'YAKU' -is:nullcast" 

date_since = "2020-10-8" # Fin de las inscripciones de las candidaturas 2020-10-8, la campaña electoral oficial es desde 31 de diciembre – 04 de febrero de 2021
data_until="2021-02-4"

get_data_Twitter(api,search_words,'es',200000,date_since,data_until,client)





















