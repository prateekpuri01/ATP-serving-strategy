# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 13:33:22 2019

Takes data from Sackmann's ATP repository and stores it into an SQL database
"""


import sqlite3
import os

"""data from Sackmann databse will be loaded into an SQL database"""

connection = sqlite3.connect("atp_data.db")
cursor = connection.cursor()

try:
    cursor.execute("""DROP TABLE SERVE_STATS;""")
except:
    pass
     

"""Here we create the master SQL table that we will store all relevant
serving statistics in"""

sql_command = """
CREATE TABLE SERVE_STATS ( 
WINNING_PLAYER CHAR(4), 
LOSING_PLAYER CHAR(4), 
MATCH_YEAR INTEGER, 
MATCH_ID CHAR(4), 
P1_FIRST_SERVE_IN INTEGER,
P1_FIRST_SERVE_TOTAL INTEGER,
P1_SECOND_SERVE_IN INTEGER,
P1_SECOND_SERVE_TOTAL INTEGER,
P1_FIRST_SERVE_POINTS_WON INTEGER,
P1_FIRST_SERVE_POINTS_TOTAL INTEGER,
P1_SECOND_SERVE_POINTS_WON INTEGER,
P1_SECOND_SERVE_POINTS_TOTAL INTEGER,
P1_WINNER_BREAK_POINTS_SAVED INTEGER,
P1_WINNER_BREAK_POINTS_SERVED_TOTAL INTEGER,
P2_FIRST_SERVE_IN INTEGER,
P2_FIRST_SERVE_TOTAL INTEGER,
P2_SECOND_SERVE_IN INTEGER,
P2_SECOND_SERVE_TOTAL INTEGER,
P2_FIRST_SERVE_POINTS_WON INTEGER,
P2_FIRST_SERVE_POINTS_TOTAL INTEGER,
P2_SECOND_SERVE_POINTS_WON INTEGER,
P2_SECOND_SERVE_POINTS_TOTAL INTEGER,
P2_WINNER_BREAK_POINTS_SAVED INTEGER,
P2_WINNER_BREAK_POINTS_SERVED_TOTAL INTEGER);"""

cursor.execute(sql_command)
dataFiles = []
dataFolder='C:/Users/Anjana Puri/Documents/Python/TennisProject/JosephSackmann Data/tennis_atp-master/tennis_atp-master'
for f in os.listdir(dataFolder):
    dataFiles += [each for each in os.listdir(dataFolder) if each.endswith('.csv')]
    
 #extract only the csv files that contain match data   
dataFiles=dataFiles[23:52]

for file in dataFiles:
    f=open(file)
    for line in f:
        line=line.split(',')
        if line[0]=='tourney_id':
            continue
        else:
            try:
                match_full_ID=line[0].split('-')
                match_year=match_full_ID[0]
                tournament_ID=match_full_ID[1]
                p1=line[7]
                p2=line[15]
                
                #here we are extracting data on first/second serve statistics for each match
                #p1 (p2) refers to statistics for the winning (losing) player
            
                p1_first_serve_in=int(line[30])
                p1_first_serve_total=int(line[29])
                p1_first_serve_points_won=int(line[31])
                p1_second_serve_points_won=int(line[32])
                p1_double_faults=int(line[28])
                p1_second_serve_points_total=p1_first_serve_total-p1_first_serve_in
                p1_break_points_saved=int(line[34])
                p1_break_points_total=int(line[35])
                p1_second_serve_in=p1_first_serve_total-p1_first_serve_in-p1_double_faults
            
                p2_first_serve_in=int(line[30+9])
                p2_first_serve_total=int(line[29+9])
                p2_first_serve_points_won=int(line[31+9])
                p2_second_serve_points_won=int(line[32+9])
                p2_double_faults=int(line[28+9])
                p2_second_serve_points_total=p2_first_serve_total-p2_first_serve_in
                p2_break_points_saved=int(line[34+9])
                p2_break_points_total=int(line[35+9])
                p2_second_serve_in=p2_first_serve_total-p2_first_serve_in-p2_double_faults
                
            except ValueError:
                continue
                
            cursor.execute(""" INSERT INTO SERVE_STATS \
                        ( 
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
                                P2_WINNER_BREAK_POINTS_SERVED_TOTAL)
                        
                                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""" , \
                                (p1,p2,match_year,tournament_ID,p1_first_serve_in,p1_first_serve_total, \
                                 p1_second_serve_in,p1_second_serve_points_total, p1_first_serve_points_won, \
                                 p1_first_serve_in,p1_second_serve_points_won , \
                                 p1_second_serve_points_total, p1_break_points_saved, \
                                 p1_break_points_total, p2_first_serve_in, p2_first_serve_total, \
                                 p2_second_serve_in,p2_second_serve_points_total, p2_first_serve_points_won, \
                                 p2_first_serve_in,p2_second_serve_points_won , \
                                 p2_second_serve_points_total, p2_break_points_saved, \
                                 p2_break_points_total))
      
        
connection.commit()
      
      
      
                        
                        
        
        
        
                            
        
        
        
        
        

     