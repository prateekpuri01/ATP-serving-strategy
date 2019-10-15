# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 15:56:36 2019

Take ATP SQL database and calculate relevant serving metrics, which are saved into a Pandas DataFrame
"""
import matplotlib.pyplot as plt 
import sqlite3
import pandas as pd
import numpy as np
import pickle
import os

connection = sqlite3.connect("atp_data.db")

#This list contains the column names for the ServeData dataframe
table_columns= ['Player 1 (P1)',
 'Player 2 (P2)',
 'Match year',
 'Tournament ID', 
 'P1 first serves made',
 'P1 first serves total',
 'P1 second serves made', 
 'P1 second serves total',
 'P1 first serve points won',
 'P1 first serve points total',
 'P1 second serve points won',
 'P1 second serve points total',
 'P1 break points saved',
 'P1 break points total',
 'P2 first serves made',
 'P2 first serves total',
 'P2 second serves made', 
 'P2 second serves total',
 'P2 first serve points won',
 'P2 first serve points total',
 'P2 second serve points won',
 'P2 second serve points total',
 'P2 break points saved',
 'P2 break points total']

#Preparing the command that will be used to extract the data from the ATP SQL database
sql_command = pd.read_sql_query(
'''SELECT
   WINNING_PLAYER, 
   LOSING_PLAYER, 
   MATCH_YEAR, 
   MATCH_ID, 
   P1_FIRST_SERVE_IN,
   P1_FIRST_SERVE_TOTAL,
   P1_SECOND_SERVE_IN,
   P1_SECOND_SERVE_TOTAL,
   P1_FIRST_SERVE_POINTS_WON,
   P1_FIRST_SERVE_POINTS_TOTAL,
   P1_SECOND_SERVE_POINTS_WON,
   P1_SECOND_SERVE_POINTS_TOTAL,
   P1_WINNER_BREAK_POINTS_SAVED,
   P1_WINNER_BREAK_POINTS_SERVED_TOTAL,
   P2_FIRST_SERVE_IN,
   P2_FIRST_SERVE_TOTAL,
   P2_SECOND_SERVE_IN,
   P2_SECOND_SERVE_TOTAL,
   P2_FIRST_SERVE_POINTS_WON,
   P2_FIRST_SERVE_POINTS_TOTAL,
   P2_SECOND_SERVE_POINTS_WON,
   P2_SECOND_SERVE_POINTS_TOTAL,
   P2_WINNER_BREAK_POINTS_SAVED,
   P2_WINNER_BREAK_POINTS_SERVED_TOTAL
   from SERVE_STATS''', connection)

#transferring the SQL data into a Pandas dataframe and renaming the columns
df = pd.DataFrame(sql_command)
df.columns=table_columns

#we are going to restrict ourself to matches where players hit at least 'minServes=20' serves to remove
#matches where players retired or situations in which match data was not input

minServes=20
df=df[(df['P1 first serve points total']>minServes) & (df['P1 second serve points total']>minServes/2) & \
      (df['P2 first serve points total']>minServes) & (df['P2 second serve points total']>minServes/2)]

#Now I want to create a dictionary that can map player ID numbers to actual names and vice versa
f=open('atp_players.csv')
name_to_id={}
id_to_name={}
player_ids=[] #list of all player id's
for line in f:
    line=line.split(',')
    if line[0]=='player_id':
        continue
    else:
        id_to_name[line[0]]=line[1]+" "+line[2]
        name_to_id[line[1]+" "+line[2]]=line[0]
        player_ids.append(line[0])
    
#save dictionaries to pkl files    
pickle_file = "name_to_id.pkl"
with open(pickle_file, 'wb') as handle:
    pickle.dump(name_to_id, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
pickle_file = "id_to_name.pkl"
with open(pickle_file, 'wb') as handle:
    pickle.dump(id_to_name, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
#the winnings player (P1) and the losing player (P2) will be set as the  
#multi-index for the dataframe
df=df.set_index(['Player 1 (P1)','Player 2 (P2)']).sort_index()   
df.to_pickle(r'raw_database_data.pkl')

#%%

serve_percentages={}
num_matches={}

#I am now going to retrieve serve make and win percentges for each player

for id in player_ids:
    id_check=0
    try:
        temp_total_wins=df.loc[[id]].sum() #get summed match data for all wins by a player
        num_wins=len(df.loc[[id]]) #track win number as well
    except KeyError:
        id_check+=1 #if the player has never won a match before, the key error will register and the id_check variable will be updated
        num_wins=0
        pass
    try:
        temp_total_losses=df.loc[(slice(None), id), :].sum() #get the summed match data for all player losses
        num_losses=len(df.loc[(slice(None), id), :])
    except KeyError:
        id_check+=2 #if the player has never won a match before, the key error will register and the id_check variable will be updated
        num_losses=0
        pass
    if id_check==0: #if no errros registered, get summed data for both player losses and wins
        fsp=(temp_total_wins.iloc[2]+temp_total_losses[2+10])/(temp_total_wins.iloc[3]+temp_total_losses[3+10]) # career first serve make percentage
        ssp=(temp_total_wins.iloc[4]+temp_total_losses[4+10])/(temp_total_wins.iloc[5]+temp_total_losses[5+10]) # career second serve make percentage
        fswp=(temp_total_wins.iloc[6]+temp_total_losses[6+10])/(temp_total_wins.iloc[7]+temp_total_losses[7+10])# career first serve winning percentage
        sswp=(temp_total_wins.iloc[8]+temp_total_losses[8+10])/(temp_total_wins.iloc[9]+temp_total_losses[9+10])# career second serve winning percentage
        em=fsp*fswp-ssp*sswp #this is the 'enhancement metric' that calculates the additional service pt win probability expected from switching from strategy (1) to strategy (2) [see readme.md]
    elif id_check==2: #if only player loss error registered, just use the player win data
        fsp=temp_total_wins.iloc[2]/temp_total_wins.iloc[3]
        ssp=temp_total_wins.iloc[4]/temp_total_wins.iloc[5]
        fswp=(temp_total_wins.iloc[6])/(temp_total_wins.iloc[7])
        sswp=(temp_total_wins.iloc[8])/(temp_total_wins.iloc[9])
        em=fsp*fswp-ssp*sswp
    elif id_check==1:  #if only player win error registered, just use the player loss data
        fsp=temp_total_losses.iloc[2+10]/temp_total_losses.iloc[3+10]
        ssp=temp_total_losses.iloc[4+10]/temp_total_losses.iloc[5+10]
        fswp=(temp_total_losses[6+10]/temp_total_losses[7+10])
        sswp=(temp_total_losses[8+10]/temp_total_losses[9+10])
        em=fsp*fswp-ssp*sswp
    else:
        continue
    serve_percentages[id]=(fsp,ssp,fswp,sswp,em) #store career serve data into dictionary
    num_matches[id]=num_wins+num_losses #store total number of career matches into dictionary

#save the created dictionaries to files
pickle_file = "player_serve_info.pkl"
with open(pickle_file, 'wb') as handle:
    pickle.dump(serve_percentages, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
pickle_file = "player_match_number_info.pkl"
with open(pickle_file, 'wb') as handle:
    pickle.dump(num_matches, handle, protocol=pickle.HIGHEST_PROTOCOL)

df.reset_index(inplace=True)

#calculate the EM factor for each match for both the winner and loser
df['P1 Enhancement Metric']=df['P1 first serves made']/df['P1 first serves total']* \
                df['P1 first serve points won']/df['P1 first serve points total'] - \
                df['P1 second serves made']/df['P1 second serves total']* \
                df['P1 second serve points won']/df['P1 second serve points total']

df['P2 Enhancement Metric']=df['P2 first serves made']/df['P2 first serves total']* \
                df['P2 first serve points won']/df['P2 first serve points total'] - \
                df['P2 second serves made']/df['P2 second serves total']* \
                df['P2 second serve points won']/df['P2 second serve points total']

#we want to restrict our data to players who have played at least 50 matches
match_cutoff=50
df=df[(df['Player 1 (P1)'].apply(lambda x: num_matches[x]>=match_cutoff)) & \
      df['Player 2 (P2)'].apply(lambda x: num_matches[x]>=match_cutoff)]
    
df=df.set_index(['Player 1 (P1)','Player 2 (P2)']).sort_index()


#extract all player matchups in our database   
player_pairs=df.index.values.tolist()
#remove duplicates
player_pairs=list(dict.fromkeys(player_pairs))
total_pairs=len(player_pairs)

#dataseries will be iteratively added to this list
#the SeriesList will then be used to construct a dataframe
SeriesList=[]

for i,players in enumerate(player_pairs):
        
        #we want to store data from all matches in which these two players have played
        player_1=players[0]
        player_2=players[1]
        player_loss_no_error=0
        
        #keep track of loop progress
        if i%1000==0:
            print(i/total_pairs*100, "% done")
        
        #take a data slice where player 1 has won
        player_1_win_slice=df.loc[player_1,player_2]
        #extract the enhancement metrics for these matches for player 1
        player_1_win_EM=list(player_1_win_slice["P1 Enhancement Metric"].values)
        #extract the enhancement metrics for these matches for player 2
        player_2_loss_EM=list(player_1_win_slice["P2 Enhancement Metric"].values)
        summed_player_1_win_data=player_1_win_slice.sum()
        num_player_1_wins=len(player_1_win_EM)

        #now check if player 1 has ever lost to player 2
        if df.index.isin([(player_2,player_1)]).any():
            #if so take a data slice of all these amtches
            player_1_loss_slice=df.loc[player_2,player_1]
            player_1_loss_EM=list(player_1_loss_slice["P2 Enhancement Metric"].values)
            summed_player_1_loss_data=player_1_loss_slice.sum()
            player_loss_no_error=1
            num_player_1_losses=len(player_1_loss_EM)
            
        if player_loss_no_error==1:
            #if player 1 has both wins and losses against player 2, this section of loop will execute
            
            #would be nice to look at EM factors in win, losses, and their combined total
            # for EM factor calculation, I will assume the FSP and SSP is determined by player career averages instead of 
            #their average against a certian player since who you play should not affect your percentages too much (this will help reduce noise)
            
            #serve percentage/EM factor calculation for wins
            p1_win_first_serve_win_perc=summed_player_1_win_data.iloc[6]/summed_player_1_win_data.iloc[7]
            p1_win_second_serve_win_perc=summed_player_1_win_data.iloc[8]/summed_player_1_win_data.iloc[9]
            p1_win_EM=serve_percentages[player_1][0]*p1_win_first_serve_win_perc-serve_percentages[player_1][1]*p1_win_second_serve_win_perc
            
            #serve percentage/EM factor calculation for losses
            p1_loss_first_serve_win_perc=summed_player_1_loss_data.iloc[6+10]/summed_player_1_loss_data.iloc[7+10]
            p1_loss_second_serve_win_perc=summed_player_1_loss_data.iloc[8+10]/summed_player_1_loss_data.iloc[9+10]
            p1_loss_EM=serve_percentages[player_1][0]*p1_loss_first_serve_win_perc-serve_percentages[player_1][1]*p1_loss_second_serve_win_perc
            
            #serve percentage/EM factor calculation for combined wins and losses
             
            p1_total_first_serve_win_perc=(summed_player_1_win_data.iloc[6]+summed_player_1_loss_data.iloc[6+10])/(summed_player_1_loss_data.iloc[7+10]+summed_player_1_win_data.iloc[7]) 
            p1_total_second_serve_win_perc=(summed_player_1_win_data.iloc[8]+summed_player_1_loss_data.iloc[8+10])/(summed_player_1_loss_data.iloc[9+10]+summed_player_1_win_data.iloc[9])
            p1_total_EM=serve_percentages[player_1][0]*p1_total_first_serve_win_perc-serve_percentages[player_1][1]*p1_total_second_serve_win_perc
            
            total_EM=player_1_win_EM+player_1_loss_EM
            p1_serve_tuple=(serve_percentages[player_1][0],p1_total_first_serve_win_perc,serve_percentages[player_1][1],p1_total_second_serve_win_perc)
            
            new_data={'Player 1 (P1)':player_1, 'Player 2 (P2)':player_2, \
                       'P1 Win EM Series':player_1_win_EM, \
                       'P1 Loss EM Series':player_1_loss_EM, \
                       'P1 Total EM Series':total_EM,\
                       'P1 Win EM': p1_win_EM,\
                       'P1 Loss EM': p1_loss_EM , \
                       'P1 Global EM':p1_total_EM,\
                       'Number of Matches':num_player_1_wins+num_player_1_losses, \
                       'Serve percentages':p1_serve_tuple, \
                       'Career EM Factor':serve_percentages[player_1][-1], \
                       'Number of Wins': num_player_1_wins, \
                       'Number of Losses': num_player_1_losses}
            
            SeriesList.append(pd.Series(new_data))
        else:
            #if player 1 only has wins against player2, this section of loop will execute
            
            #calculate EM factors for all player 1 wins
            p1_win_first_serve_win_perc=summed_player_1_win_data.iloc[6]/summed_player_1_win_data.iloc[7]
            p1_win_second_serve_win_perc=summed_player_1_win_data.iloc[8]/summed_player_1_win_data.iloc[9]
            p1_win_EM=serve_percentages[player_1][0]*p1_win_first_serve_win_perc-serve_percentages[player_1][1]*p1_win_second_serve_win_perc
            p1_serve_tuple=(serve_percentages[player_1][0],p1_win_first_serve_win_perc,serve_percentages[player_1][1],p1_win_second_serve_win_perc)
                
            new_data={'Player 1 (P1)':player_1, 'Player 2 (P2)':player_2, \
                       'P1 Win EM Series':player_1_win_EM, \
                       'P1 Loss EM Series':np.NaN, \
                       'P1 Total EM Series':player_1_win_EM,\
                       'P1 Win EM': p1_win_EM,\
                       'P1 Loss EM': np.NaN, \
                       'P1 Global EM':p1_win_EM, \
                       'Number of Matches':num_player_1_wins, \
                       'Serve percentages': p1_serve_tuple, \
                       'Career EM Factor':serve_percentages[player_1][-1], \
                       'Number of Wins': num_player_1_wins, \
                       'Number of Losses': 0}
            
            SeriesList.append(pd.Series(new_data))
            
            #We will also create a data entry for player 2 playing against player 1
            
            p2_loss_first_serve_win_perc=summed_player_1_win_data.iloc[6+10]/summed_player_1_win_data.iloc[7+10]
            p2_loss_second_serve_win_perc=summed_player_1_win_data.iloc[8+10]/summed_player_1_win_data.iloc[9+10]
            p2_loss_EM=serve_percentages[player_2][0]*p2_loss_first_serve_win_perc-serve_percentages[player_2][1]*p2_loss_second_serve_win_perc
            p2_serve_tuple=(serve_percentages[player_2][0],p2_loss_first_serve_win_perc,serve_percentages[player_2][1],p2_loss_second_serve_win_perc)
            
            new_data={'Player 1 (P1)':player_2, 'Player 2 (P2)':player_1, \
                       'P1 Win EM Series':np.NaN, \
                       'P1 Loss EM Series':player_2_loss_EM, \
                       'P1 Total EM Series':player_2_loss_EM,\
                       'P1 Win EM': np.NaN,\
                       'P1 Loss EM': p2_loss_EM, \
                       'P1 Global EM':p2_loss_EM, \
                       'Number of Matches':num_player_1_wins, \
                       'Serve percentages': p2_serve_tuple, \
                       'Career EM Factor':serve_percentages[player_2][-1], \
                       'Number of Wins': 0, \
                       'Number of Losses': num_player_1_wins}
            
            SeriesList.append(pd.Series(new_data))
            
            
#construct data frame from SeriesList and then save to pkl file 
filled_df=pd.DataFrame(SeriesList).set_index(['Player 1 (P1)','Player 2 (P2)']).sort_index()     
filled_df=filled_df.loc[~filled_df.index.duplicated(keep='first')]   
filled_df.to_pickle(r'enhancement_metrics.pkl')
            
            
    
    

        




