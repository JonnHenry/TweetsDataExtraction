import json
from pymongo import MongoClient
from types import SimpleNamespace
from bson.json_util import dumps
import pandas as pd
import numpy as np


MONGO_HOST= 'mongodb://localhost/'  # assuming you have mongoDB installed locally
                                             # and a database called 'twitterdb'

client = MongoClient(MONGO_HOST)


def extract_data(client):
    db = client.twitterdb
    columns_find = ["created_at","favorite_count","full_text","id_str","metadata.iso_language_code","retweeted_status.created_at","retweeted_status.full_text","user.created_at","user.favourites_count","user.followers_count","user.friends_count","user.id_str","user.lang","user.location","user.verified"]
    data = db.twitter_search_lasso.find()
    data_tweets = None
    cont=0
    for tweet in data:
        dict_values_JSON = {}
        for column in columns_find:
            column_splited =  column.split(".")
            
            if len(column_splited)==2:
                if column_splited[0] in tweet:
                    data_key = tweet[column_splited[0]]
                    
                    if column_splited[1] in data_key:
                        dict_values_JSON[column] = [data_key[column_splited[1]]]
                    else:
                        dict_values_JSON[column] = [np.nan]
                else:
                    dict_values_JSON[column] = [np.nan]
            else:
                if column_splited[0] in tweet:
                    dict_values_JSON[column] = [tweet[column]]
                else:
                    dict_values_JSON[column] = [np.nan]

        if cont==0:
            data_tweets=pd.DataFrame(dict_values_JSON)
        else:
            df_auxiliar = pd.DataFrame(dict_values_JSON)
            data_tweets = pd.concat([data_tweets, df_auxiliar], axis=0)
            data_tweets = data_tweets.reset_index(drop=True)

        cont+=1
        

    return data_tweets

df_tweets = extract_data(client)
df_tweets.to_csv("Twitter_search_Lasso.csv",index=False)




