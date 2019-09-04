# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 18:51:13 2019

Helper file to create a list of active players

"""
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 15:56:36 2019
"""
import sqlite3
import pandas as pd
import csv

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

#transferring the data into a dataframe and renaming the columns
df = pd.DataFrame(sql_command)
df.columns=table_columns
#we will define active players as players who have played a match in 2017 or later
yearCutoff=2016
df=df[df['Match year']>yearCutoff]
active_player_list=list(set(df["Player 1 (P1)"].tolist()+df["Player 2 (P2)"].tolist()))

#write list of active players to a csv file
with open('active_players.csv', 'w') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerows(active_player_list)
csvFile.close()


