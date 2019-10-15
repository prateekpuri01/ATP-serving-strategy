# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 15:34:02 2019

helper file that creates and saves a dictionary of player id's and there associated career FSP and SSP
across all the games in their career that are saved in the ATP databse. Produced output file will be
used to sample serving percentages in the MC simulation
"""
import pickle
import pandas as pd


df = pd.read_pickle('raw_database_data.pkl')
pickle_file = "name_to_id.pkl"
with open(pickle_file, 'rb') as handle:
    name_to_id = pickle.load(handle)
players_ids=list(name_to_id.values())
serve_dict={}
for i,player in enumerate(players_ids):
    
    if i%100==0:
        print(i/len(players_ids))
    try:    
        FSPS=list(df.loc[player]['P1 first serves made']/df.loc[player]['P1 first serves total'])
        SSPS=list(df.loc[player]['P1 second serves made']/df.loc[player]['P1 second serves total'])
        serve_dict[player]=(FSPS,SSPS)
    except KeyError:
        continue

pickle_file = "player_serve_history.pkl"
with open(pickle_file, 'wb') as handle:
    pickle.dump(serve_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)