# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 10:53:16 2019

this file creates a monte carlo simulation of a tennis match that predict the winner of the 
match based off of each players first/second serve make and winning percentages

"""
import random
import pandas as pd
import numpy as np
import pickle

#import necessary player info files and dataframes

pickle_file = "player_serve_info.pkl"
with open(pickle_file, 'rb') as handle:
    player_serve_info = pickle.load(handle)
    
pickle_file = "player_match_number_info.pkl"
with open(pickle_file, 'rb') as handle:
    num_matches = pickle.load(handle)

pickle_file = "name_to_id.pkl"
with open(pickle_file, 'rb') as handle:
    name_to_id = pickle.load(handle)

pickle_file = "id_to_name.pkl"
with open(pickle_file, 'rb') as handle:
    id_to_name = pickle.load(handle)

df = pd.read_pickle('enhancement_metrics.pkl')

#%%

""" simPoint: function that simulates whether a server wins a servus point
              player_fsp: server's first serve make percentage
              player_fswp: server's first serve winning percentage
              player_ssp: server's second serve make percentage
              player_sswp: server's second serve winning percentage
              strategy: 'timid'- means player hits standard second serve
                        'bold'- means player hits first serve as second serve
              
              return: (0,1) if returner wins
                      (1,0) if server wins
"""
        
def simPoint(player_fsp,player_fswp,player_ssp,player_sswp,strategy='timid'):
        
        #check if first serve is made
        if random.random()<=player_fsp: #if evaluates to true, server make first serve
            if random.random()<=player_fswp: #if evaluates to true, server wins point
                return (1,0)
            else:
                return (0,1) #otherwise server losses point
        #first serve has been missed, so second serve is hit
        else:
            
            #if 'timid' strategy is employed, second serve is hit
            if strategy=='timid':
                if random.random()<=player_ssp: #check if serve goes in
                    if random.random()<=player_sswp: #if in, this checks if server wins point
                        return (1,0)
                    else:
                        return (0,1) #player losses second serve point
                else:
                    return (0,1) #player double faults
                
            elif strategy=='bold': #bold strategy picked, first serve is hit again
                if random.random()<=player_fsp: #checks if first serve is in
                    if random.random()<=player_fswp: #checks if first serve pt is won
                        return (1,0) #server wins point
                    else:
                        return (0,1) #server losses point
                else:
                    return (0,1) #server doubles fault


""" simGame: function that simulates a service game
              player_fsp: server's first serve make percentage
              player_fswp: server's first serve winning percentage
              player_ssp: server's second serve make percentage
              player_sswp: server's second serve winning percentage
              strategy: 'timid'- means player hits standard second serve
                        'bold'- means player hits first serve as second serve
              
              return: True - server wins
                      False - returner wins
"""

def simGame(player_fsp,player_fswp,player_ssp,player_sswp,strategy='timid'):
    
    pts=(0,0)
    #pts keeps track of each players game point total (first element = server points, second element=returner points)
    
    #game ended when a player either has won four points while the opponent has less than three
    #or if the game goes to deuce (score gets tied at 3-3), the first player to have a two point separation wins
    while (not (abs(pts[0]-pts[1])>=2 and pts[0]>=3 and pts[1]>=3)) and (not (pts[0]==4 and pts[1]<3)) and (not (pts[1]==4 and pts[0]<3)):
        pts=tuple(map(sum,zip(pts,simPoint(player_fsp,player_fswp,player_ssp,player_sswp,strategy))))
        #pts is iteratively updated after each loop
    if pts[0]>pts[1]:
        return True
    else:
        return False
    

""" simTieBreaker: function that simulates a tiebreaker
              player1_fsp: initial server's first serve make percentage
              player1_fswp: initial server's first serve winning percentage
              player1_ssp: initial server's second serve make percentage
              player1_sswp: initial server's second serve winning percentage
              
              player2_fsp: second server's first serve make percentage
              player2_fswp: second server's first serve winning percentage
              player2_ssp: second server's second serve make percentage
              player2_sswp: second server's second serve winning percentage
              
              p1_strategy, p2_strategy: players' serving strategy 
                        'timid'- means player hits standard second serve
                        'bold'- means player hits first serve as second serve
              
              return: True - player_1 wins
                      False - player_2 wins
"""
    

def simTieBreaker(player1_fsp,player1_fswp,player1_ssp,player1_sswp,\
                  player2_fsp,player2_fswp,player2_ssp,player2_sswp,p1_strategy='timid',p2_strategy='timid'):
    #pts keeps track of each players tiebreaker point total
    
    pts=(0,0)
    
    #simulate the first point with player1_serving
    pts=tuple(map(sum,zip(pts,simPoint(player1_fsp,player1_fswp,player1_ssp,player1_sswp,p1_strategy))))
    
    #keeps track of who is serving
    loopNum=0    
    
    #tiebreaker wins when one player reaches 7, win by 2
    while (not((pts[0]-pts[1]>=2) and (pts[0]>=7))) and (not((pts[1]-pts[0]>=2) and (pts[1]>=7))):
        
        #is loop num is even, player 2 serve two points
        if loopNum%2==0:
            pts=tuple(map(sum,zip(pts,simPoint(player2_fsp,player2_fswp,player2_ssp,player2_sswp,p2_strategy)[::-1])))
            #simulate point with server 2 serving
            if ((pts[0]-pts[1]>=2) and (pts[0]>=7)) or ((pts[1]-pts[0]>=2) and (pts[1]>=7)):#check is tiebreaker is over
                continue
            else:
                #if tiebreaker is not over yet, let player 2 serve his second point
                pts=tuple(map(sum,zip(pts,simPoint(player2_fsp,player2_fswp,player2_ssp,player2_sswp,p2_strategy)[::-1])))
        
        #if loop num is odd, player 1 serves two points
        else:
            #simulate player 1 service point
            pts=tuple(map(sum,zip(pts,simPoint(player1_fsp,player1_fswp,player1_ssp,player1_sswp,p1_strategy))))
            if ((pts[0]-pts[1]>=2) and (pts[0]>=7)) or ((pts[1]-pts[0]>=2) and (pts[1]>=7)): #check if tiebreaker is over
                continue
            else: #if not over, simulate another player 1 service point
                pts=tuple(map(sum,zip(pts,simPoint(player1_fsp,player1_fswp,player1_ssp,player1_sswp,p1_strategy))))
        loopNum+=1 #update loopNum
    if pts[0]>pts[1]:
        return True
    else:
        return False
    
    
""" simSet:   function that simulates a set
              player1_fsp: initial server's first serve make percentage
              player1_fswp: initial server's first serve winning percentage
              player1_ssp: initial server's second serve make percentage
              player1_sswp: initial server's second serve winning percentage
              
              player2_fsp: second server's first serve make percentage
              player2_fswp: second server's first serve winning percentage
              player2_ssp: second server's second serve make percentage
              player2_sswp: second server's second serve winning percentage
              
              serve_first=player who is serving first in set
              
              p1_strategy, p2_strategy: players' serving strategy 
                        'timid'- means player hits standard second serve
                        'bold'- means player hits first serve as second serve
              
              return: (True, nextPlayer) - player_1 wins, nextPlayer is player who will serve first game of next set
                      (False,nextPlayer) - player_1 loses, nextPlayer is player who will serve first game of next set
"""
    

    
def simSet(player1_fsp,player1_fswp,player1_ssp,player1_sswp,\
                  player2_fsp,player2_fswp,player2_ssp,player2_sswp,serve_first,p1_strategy='timid',p2_strategy='timid'):
    
    
    #variable that track the number of game won by each player and number of games in set
    p1_games=0
    p2_games=0
    loopNum=0
    
    if serve_first=='player_1':
        modNum=0
    else:
        modNum=1
    
    #set is won when a player has 6 games and the other player has 4 or less
    #if players tie at 6-6, a tiebreaker decides the winner    
    while (not ((p1_games-p2_games)>=2 and p1_games>=6)) and (not ((p2_games-p1_games)>=2 and p2_games>=6)) and (not (p1_games==6 and p2_games==6)):
        if loopNum%2==modNum: #if serve_first='player 1' this is the first branch that is initially run
            if simGame(player1_fsp,player1_fswp,player1_ssp,player1_sswp,p1_strategy):#sim player 1 service game
                p1_games+=1 #if player1 wins, update his game total
            else:
                p2_games+=1 #if player 2 wins, update his game total
        else: #this branch is run everytime player2 is serving. If modNum=1, this branch will be run as the first game in the set
            if simGame(player2_fsp,player2_fswp,player2_ssp,player2_sswp,p2_strategy): #sim player 2 service match
                p2_games+=1 #update player 2 game total if server wins
            else:
                p1_games+=1 #update player 2 game total if returner wins
        loopNum+=1
                
    if loopNum%2==0: #first who served last and who would serve in a second set
                     #if number of games played is even, the initial server is the next server
        if serve_first=='player_1': 
            nextPlayer='player_1'
        else:
            nextPlayer='player_2'
    else:           #if number of games played is odd, whoever served first will not serve the next set first
        if serve_first=='player_1':
            nextPlayer='player_2'
        else:
            nextPlayer='player_1'
    
    #if the set simulation loop ended with p1_games=p2_games=6, simulate a tiebreaker
    if p1_games==p2_games:
        if modNum==0: #if player 1 started serving, he will start serving the tiebreaker as well
            result=simTieBreaker(player1_fsp,player1_fswp,player1_ssp,player1_sswp,\
                  player2_fsp,player2_fswp,player2_ssp,player2_sswp,p1_strategy,p2_strategy)
            #if player 1 win tiebreaker, return true
        else: #otherwise player 2 starts tiebreaker
            result=not simTieBreaker(player2_fsp,player2_fswp,player2_ssp,player2_sswp,\
                  player1_fsp,player1_fswp,player1_ssp,player1_sswp,p2_strategy,p1_strategy)
            #if player 2 wins tiebreaker, then return False
        return (result,nextPlayer)
    
    elif p1_games>p2_games: #if no tiebreaker is needed, if p1 has won more games, he wins the set
        return (True,nextPlayer)
    else:
        return (False,nextPlayer)
    
    
""" simMatch:   function that simulates a match
        
              sets_to_win: number of sets needed to win match, either 3 or 5 in ATP
              player1_fsp: initial server's first serve make percentage
              player1_fswp: initial server's first serve winning percentage
              player1_ssp: initial server's second serve make percentage
              player1_sswp: initial server's second serve winning percentage
              
              player2_fsp: second server's first serve make percentage
              player2_fswp: second server's first serve winning percentage
              player2_ssp: second server's second serve make percentage
              player2_sswp: second server's second serve winning percentage

              p1_strategy, p2_strategy: players' serving strategy 
                        'timid'- means player hits standard second serve
                        'bold'- means player hits first serve as second serve
              
              return: (True) - player_1 wins
                      (False) - player_1 loses
"""
    
def simMatch (sets_to_win,player1_fsp,player1_fswp,player1_ssp,player1_sswp,\
                  player2_fsp,player2_fswp,player2_ssp,player2_sswp,p1_strategy,p2_strategy):
    p1_sets=0
    p2_sets=0
    
    #simulate coin flip at beginning of match to decide first server
    if random.random()<=.5:
        set_player_start='player_1'
    else:
        set_player_start='player_2'
        
    while (p1_sets<sets_to_win and p2_sets<sets_to_win):
        set_result=simSet(player1_fsp,player1_fswp,player1_ssp,player1_sswp,\
                  player2_fsp,player2_fswp,player2_ssp,player2_sswp,set_player_start,p1_strategy,p2_strategy)
        if set_result[0]==True:
            p1_sets+=1 #if player 1 wins first set update his set total
        else:
            p2_sets+=1       #if player 2 wins first set update his set total
        set_player_start=set_result[1] #update who starts serving the next set
    
    if p1_sets==sets_to_win:
        return True
    else:
        return False
        
""" MonteCarlo:  simulates a specify number of matches between two players using serving data from their matchup history
        
                player 1: string of player 1 name
                player 2: string of player 2 name
                dataFrame: dataFrame containing player matchup data
                num_sets: number of sets required to win a match
                num_trials: number of times to simulate matchup
                num_sims_per_trial: number of matches to simulate in each trial

                p1_strategy, p2_strategy: players' serving strategy 
                        'timid'- means player hits standard second serve
                        'bold'- means player hits first serve as second serve
              
              return: trial_results: win percentage for player 1 in each trial
"""

def MonteCarlo(player1,player2,dataFrame,num_sets,num_trials,num_sims_per_trial,player1_strategy='timid',player2_strategy='timid'):
    
    player1_id=name_to_id[player1] #get player ids
    player2_id=name_to_id[player2]
    player1_fsp=player_serve_info[player1_id][0] #get first/second serve make percentages for each player
    player1_ssp=player_serve_info[player1_id][1]
    player2_fsp=player_serve_info[player2_id][0]
    player2_ssp=player_serve_info[player2_id][1]
    
    p1_serve_data=dataFrame.loc[player1_id,player2_id]['Serve percentages'] #get fswp and sswp in player matchup for each player from dataframe 
    player1_fswp=p1_serve_data[1]
    player1_sswp=p1_serve_data[3]
    p2_serve_data=dataFrame.loc[player2_id,player1_id]['Serve percentages']
    player2_fswp=p2_serve_data[1]
    player2_sswp=p2_serve_data[3]
    

    trial_results=[]
    for i in range(num_trials):
        player_1_wins=0 #keep track of player 1 wins
        for num in range(num_sims_per_trial):
            if simMatch(num_sets,player1_fsp,player1_fswp,player1_ssp,player1_sswp,\
                        player2_fsp,player2_fswp,player2_ssp,player2_sswp,player1_strategy,player2_strategy):
                player_1_wins+=1 #if player 1 wins the match, update his win total
        trial_results.append(player_1_wins/num_sims_per_trial) #append match winning percentage to list
        
    return trial_results #return list
              
player_pairs=list(df.index) #get all player pairs in dataFrame
SeriesList=[] #dataSeries will be appended to this empty list and eventually used to construct a dataframe
numPairs=len(player_pairs)
for i,pair in enumerate(player_pairs): #run a MC simulation for each player matchup
    
    if i%10==0:
        print(100*i/numPairs," % completed.......") #keep track of progress
        
    player1=id_to_name[pair[0]] #get player names
    player2=id_to_name[pair[1]]
    
    bold_list=MonteCarlo(player1,player2,df,3,10,1000,'bold','timid') #simulate matches when player 1 goes 'bold'
    timid_list=MonteCarlo(player1,player2,df,3,10,1000,'timid','timid') # simulate matches when player_1 goes 'timid'
    bold_mean=np.mean(bold_list) #store the means
    timid_mean=np.mean(timid_list)
    real_life_wins=df.loc[pair[0],pair[1]].iloc[-2] #store the actual, real-life number of wins by player 1 in matchup
    real_life_num_matches=df.loc[pair[0],pair[1]].iloc[-5] #store the actual, real-life total number of matches in matchup
    
    #now store various metric is a series 
    new_data={'Player 1 (P1)':pair[0], 'Player 2 (P2)':pair[1], \
                       'Player 1 Name':player1, \
                       'Player 2 Name':player2, \
                       'Bold MC results': bold_list,\
                       'Timid MC results': timid_list,\
                       'Bold MC win percentage':bold_mean,\
                       'Timid MC win percentage': timid_mean,\
                       'Delta MC Results':bold_mean-timid_mean, \ #difference in expected win percentage obtained from switching strategies
                       'Real life win percentages': real_life_wins/real_life_num_matches, \
                       'Real life number of matches': real_life_num_matches}
    SeriesList.append(pd.Series(new_data))

MC_df=pd.DataFrame(SeriesList).set_index(['Player 1 (P1)','Player 2 (P2)']).sort_index()
MC_df.to_pickle(r'MC_results.pkl') #save results
        
        
        
    
    

