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

def get_data_Twitter(api_object,query,languaje,num_items,data_since,mongo_client):
    try:
        tweets = tw.Cursor(api_object.search,q=query,lang=languaje,since=data_since,tweet_mode='extended').items(num_items)
        for tweet in tweets:
            datajson = json.loads(json.dumps(tweet._json)) 
            created_at = datajson['created_at']
            print("Tweet collected at " + str(created_at))
            #db.twitter_search_arauz.insert_one(datajson)
            mongo_client.insert_one(datajson)
            #db.twitter_search_hervas.insert_one(datajson)
    except Exception as e:
           print(e)

search_words_Arauz = "'Andres Arauz' OR 'Andrés Arauz' OR ecuarauz OR Arauz OR 'ANDRES ARAUZ' -is:nullcast -is:retweet "
search_words_Guillen = "'Guillermo Lasso' OR LassoGuillermo OR Lasso OR 'GUILLERMO LASSO' OR LASSO -is:nullcast -is:retweet"
#search_words = "'Xavier Hervas' OR xhervas OR 'XAVIER HERVAS' OR 'XAVIER hervas' OR 'xavier HERVAS' -is:nullcast" 
#search_words = "'Yaku Pérez Guartambel' OR yakuperezg OR 'Yaku Pérez' OR YakuEs OR 'YAKU PEREZ' OR Yaku OR 'YAKU' -is:nullcast" 

date_since = "2021-1-24" # Fin de las inscripciones de las candidaturas 2020-10-8, la campaña electoral oficial es desde 31 de diciembre – 04 de febrero de 2021
db = client.twitterdb

data_base_lasso = db.twitter_search_lasso_after_elections
get_data_Twitter(api,search_words_Guillen,'es',90000000000,date_since,data_base_lasso)


data_base_arauz = db.twitter_search_arauz_after_elections
get_data_Twitter(api,search_words_Arauz,'es',900000000000,date_since,data_base_arauz)





















