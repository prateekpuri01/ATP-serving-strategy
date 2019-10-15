# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 15:41:57 2019

File creates data visualization of relevant data metrics

@author: Prateek Puri
"""
import matplotlib
import matplotlib.pyplot as plt 
import pandas as pd
import numpy as np
import pickle
import csv
import os

path="C:\\Users\\Anjana Puri\\Documents\\Python\\TennisProject\\JosephSackmann Data\\tennis_atp-master\\tennis_atp-master"
os.chdir(path)
#%%

#set textstyles for plot
font = {'family' : 'normal',
        'weight' : 'normal',
        'size'   : 11}
matplotlib.rc('font', **font)

plt.rc('xtick',labelsize=20)
plt.rc('ytick',labelsize=20)

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

with open('active_players.csv', 'r') as f:
    reader = csv.reader(f)
    player_list = list(reader)
active_player_list=[''.join(x) for x in list(filter(lambda a: a != [], player_list))]

with open('top_30_players.csv', 'r') as f:
    reader = csv.reader(f)
    top_player_list = list(reader)
top_player_list=[''.join(x) for x in list(filter(lambda a: a != [], top_player_list))] 

#%%

#plot career EM factors for all ATP players in database
#
#EM_list=[]
#
#for x in top_player_list:
#    if x in active_player_list:
#        try:
#            EM_list.append(player_serve_info[x][-1])
#        except KeyError:
#            continue
EM_list=[i[-1] for i in list(player_serve_info.values())]
#number of histogram bins
num_bins=50
plt.clf()
plt.xlim([min(EM_list), max(EM_list)])
plt.hist(EM_list, bins=num_bins, alpha=0.5,color='c')
plt.title('Serve win percentage enhancement',fontsize=20)
plt.xlabel(r'$EM = FSP \times FSWP-SSP \times SSWP$', fontsize=20)
plt.ylabel('Count',fontsize=20)
#plot average as well
plt.axvline(x=np.mean(EM_list), linewidth=5, color='r', linestyle='dashed')
plt.text(np.mean(EM_list)+.05,150,'Mean: ' + str(round(np.mean(EM_list),3)),rotation=0,fontsize=15)
plt.tight_layout()
plt.savefig(os.path.join('ATP_EM.png'), dpi=300, format='png', bbox_inches='tight') # use format='svg' or 'pdf' for vectorial pictures

plt.show()

#%%

#now we want to display the players with the top 10 highest career EM factors who have 
#played at least 100 matches

min_matches=100
top10=sorted([(id_to_name[k],round(v[-1],3)) for k,v in player_serve_info.items() \
              if (num_matches[k]>min_matches) and (k in top_player_list)],key=lambda x:x[1],reverse=True)[:10][::-1]
    
players = [i[0] for i in top10]
percentages = [i[1] for i in top10]
fig, ax = plt.subplots()    
width = .75 # the width of the bars 
ind = np.arange(len(percentages)) # the x locations for the groups
ax.barh(ind, percentages, width, color="dodgerblue")
ax.set_yticks((ind+width/2)-.5)
ax.set_yticklabels(players, minor=False)
plt.xlabel('Career EM',fontsize=20)
plt.ylabel('Player',fontsize=20)       
for i, v in enumerate(percentages):
    ax.text(v-.0075, i-.20, str(round(v,3)), color='white', fontweight='bold')
ax.set_aspect(aspect=0.005)
plt.savefig(os.path.join('career_top_EM.png'), dpi=300, format='png', bbox_inches='tight') # use format='svg' or 'pdf' for vectorial pictures
plt.show()
    
#%%

#now we want to repeat the above plot for the bottom 10 career EM factors

bottom10=sorted([(id_to_name[k],round(v[-1],3)) for k,v in player_serve_info.items() \
              if (num_matches[k]>min_matches) and (k in top_player_list)],key=lambda x:x[1],reverse=True)[-10:][::-1]
    
players = [i[0] for i in bottom10]
percentages = [i[1] for i in bottom10]
fig, ax = plt.subplots()    
width = .75 # the width of the bars 
ind = np.arange(len(percentages)) # the x locations for the groups
ax.barh(ind, percentages, width, color="red")
ax.set_yticks((ind+width/2)-.5)
ax.set_yticklabels(players, minor=False)
plt.xlabel('Career EM',fontsize=20)
plt.ylabel('Player',fontsize=20)       
for i, v in enumerate(percentages):
    ax.text(v+.005, i-.20, str(round(v,3)), color='white', fontweight='bold')
ax.set_aspect(aspect=0.008)
plt.savefig(os.path.join('career_worst_EM.png'), dpi=300, format='png', bbox_inches='tight') # use format='svg' or 'pdf' for vectorial pictures
plt.show()
    

#%%

#lets repeat our top 10 plot for active players

top10_recent=sorted([(id_to_name[k],round(v[-1],3)) for k,v in player_serve_info.items() \
              if (num_matches[k]>min_matches) & (k in active_player_list)& (k in top_player_list)],key=lambda x:x[1],reverse=True)[:10][::-1]
    
players = [i[0] for i in top10_recent]
percentages = [i[1] for i in top10_recent]
fig, ax = plt.subplots()    
width = .75 # the width of the bars 
ind = np.arange(len(percentages)) # the x locations for the groups
ax.barh(ind, percentages, width, color="dodgerblue")
ax.set_yticks((ind+width/2)-.5)
ax.set_yticklabels(players, minor=False)
plt.xlabel('Active player career EM',fontsize=20)
plt.ylabel('Player',fontsize=20)      
for i, v in enumerate(percentages):
    ax.text(v-.0075, i-.20, str(round(v,3)), color='white', fontweight='bold')
ax.set_aspect(aspect=0.005)
plt.savefig(os.path.join('active_players_top_career_EM.png'), dpi=300, format='png', bbox_inches='tight') # use format='svg' or 'pdf' for vectorial pictures
plt.show()


#%%
#let's repeat our bottom 10 plot for active players

bottom10_recent=sorted([(id_to_name[k],round(v[-1],3)) for k,v in player_serve_info.items() \
              if (num_matches[k]>min_matches) & (k in active_player_list)& (k in top_player_list)],key=lambda x:x[1],reverse=True)[-10:][::-1]
    
players = [i[0] for i in bottom10_recent]
percentages = [i[1] for i in bottom10_recent]
fig, ax = plt.subplots()    
width = .75 # the width of the bars 
ind = np.arange(len(percentages)) # the x locations for the groups
ax.barh(ind, percentages, width, color="red")
ax.set_yticks((ind+width/2)-.5)
ax.set_yticklabels(players, minor=False)
plt.xlabel('Active player career EM',fontsize=20)
plt.ylabel('Player',fontsize=20)       
for i, v in enumerate(percentages):
    ax.text(v+.005, i-.20, str(round(v,3)), color='white', fontweight='bold')
ax.set_aspect(aspect=0.007)
plt.savefig(os.path.join('active_players_worst_career_EM.png'), dpi=300, format='png', bbox_inches='tight') # use format='svg' or 'pdf' for vectorial pictures
plt.show()

#%%
#Now we want to get a feel for how first/second serve make percentages vary across the ATP
plt.clf()

#extract first serve make percentages
FSP_list=[i[0] for i in list(player_serve_info.values())]
#extract second serve make percentages
SSP_list=[i[1] for i in list(player_serve_info.values())]
plt.xlim([min(FSP_list), max(SSP_list)])
plt.hist(FSP_list, bins=50, alpha=0.5,color='c',label='First serve')
plt.hist(SSP_list, bins=50, alpha=0.5,color='r',label='Second serve')
plt.legend()
plt.xlabel(r'Serve make percentages', fontsize=20)
plt.ylabel('Count',fontsize=20)


#calculate the averages of each
plt.axvline(x=np.mean(SSP_list), linewidth=5, color='r', linestyle='dashed')
plt.axvline(x=np.mean(FSP_list), linewidth=5, color='r', linestyle='dashed')
plt.text(np.mean(SSP_list)-.11,150,'Mean: ' + str(round(np.mean(SSP_list),2)),rotation=0,fontsize=20)
plt.text(np.mean(FSP_list)-.09,170,'Mean: ' + str(round(np.mean(FSP_list),2)),rotation=0,fontsize=20)
plt.tight_layout()
plt.savefig("serve_make_percentages_hist.png")
plt.show()


#%%

plt.clf()

#repeat the above plot with first/second serve winning percentage
FSWP_list=[i[2] for i in list(player_serve_info.values())]
SSWP_list=[i[3] for i in list(player_serve_info.values())]
plt.xlim([min(FSWP_list)-.1, max(SSWP_list)+.1])
plt.hist(FSWP_list, bins=50, alpha=0.5,color='c',label='First serve')
plt.hist(SSWP_list, bins=50, alpha=0.5,color='r',label='Second serve')
plt.legend()
plt.xlabel(r'Serve win percentages', fontsize=20)
plt.ylabel('Count',fontsize=20)
plt.axvline(x=np.mean(SSWP_list), linewidth=5, color='r', linestyle='dashed',label='Second Serve')
plt.axvline(x=np.mean(FSWP_list), linewidth=5, color='r', linestyle='dashed',label='First Serve')
plt.text(np.mean(SSWP_list)-.09,200,'Mean: ' + str(round(np.mean(SSWP_list),2)),rotation=0,fontsize=20)
plt.text(np.mean(FSWP_list)-.09,200,'Mean: ' + str(round(np.mean(FSWP_list),2)),rotation=0,fontsize=20)
plt.tight_layout()
plt.savefig("serve_winning_percentages_hist.png")
plt.show()


#%%
#now let's examine the correlation between players' fswp ans sswp
plt.clf()
fig, ax = plt.subplots()
plt.xlim([.3,1])
plt.ylim([.1, .8])
plt.xlabel(r'First serve win percentage', fontsize=20)
plt.ylabel(r'Second serve win percentage',fontsize=20)
fit=np.polyfit(FSWP_list, SSWP_list, 1)
fit_fun=np.poly1d(fit)
x=np.linspace(0,1,100)
lines=plt.plot(FSWP_list,SSWP_list,'o',x,fit_fun(x),'r--')
plt.setp(lines,linewidth=5.0)
#extract correlation coefficient
plt.text(.31,.77,r"Pearson's correlation coefficient: " + str(round(np.corrcoef(FSWP_list, SSWP_list)[0, 1],2)),fontsize=12)
ax.set_aspect(.75)
plt.tight_layout()
plt.savefig("first_serve_second_serve_wp_correaltion.png")
plt.show()

#%%


#let's look at the top 10 EM factors for a player against a particular opponent
# we will limit our study to matchups with a minimum number of matches of 10
#and store results into a labeled bar graph

"""bar_graph_header: function that takes two player names and creates a P1 vs. P2 output string

    l1=string for player 1
    l2=string for player 2
    
    return player 1 vs player 2
"""

minMatches=10

def bar_graph_header(l1,l2):
    return l1+ " vs. " + l2


plt.clf()

#make copy of dataframe
matchup_df=df.copy().reset_index()
matchup_df["Player 1 Name"]=matchup_df["Player 1 (P1)"].apply(lambda x: id_to_name[x])
matchup_df["Player 2 Name"]=matchup_df["Player 2 (P2)"].apply(lambda x: id_to_name[x])
matchup_df=matchup_df[matchup_df['Number of Matches']>minMatches]
matchup_df=matchup_df[matchup_df['Player 1 (P1)'].apply(lambda x: x in top_player_list) & matchup_df['Player 2 (P2)'].apply(lambda x: x in top_player_list)]
matchup_df=matchup_df.set_index(['Player 1 (P1)','Player 2 (P2)']).sort_values(by='P1 Global EM',ascending=False).reset_index()[['P1 Global EM','Player 1 Name','Player 2 Name']].iloc[:10]


matchup_string = list(map(bar_graph_header,matchup_df['Player 1 Name'],matchup_df['Player 2 Name']))[::-1]
matchup_EMs = list(matchup_df['P1 Global EM'])[::-1]

fig, ax = plt.subplots()    
width = 0.75 # the width of the bars 
ind = np.arange(len(matchup_EMs))  # the x locations for the groups

ax.barh(ind, matchup_EMs, width, color="dodgerblue")
ax.set_yticks(ind+width/2-.5)
ax.set_yticklabels(matchup_string, minor=False)
plt.title('Post 1991 matchups',fontsize=20)
plt.xlabel('Matchup EM',fontsize=20)
plt.ylabel('Player matchup',fontsize=20)      
ax.set_aspect(aspect=0.004)
for i, v in enumerate(matchup_EMs):
    ax.text(v-.0075, i-.25, str(round(v,3)), color='white', fontweight='bold')
plt.savefig(os.path.join('top_EM_matchups.png'), dpi=300, format='png', bbox_inches='tight') # use format='svg' or 'pdf' for vectorial pictures
plt.show()


    
#%%

#let's repeat the above analysis for the worst head-to-head EM factors in particular player matchups
matchup_df=df.copy().reset_index()
matchup_df=matchup_df[matchup_df['Number of Matches']>minMatches]
matchup_df["Player 1 Name"]=matchup_df["Player 1 (P1)"].apply(lambda x: id_to_name[x])
matchup_df["Player 2 Name"]=matchup_df["Player 2 (P2)"].apply(lambda x: id_to_name[x])
matchup_df=matchup_df[matchup_df['Player 1 (P1)'].apply(lambda x: x in top_player_list) & matchup_df['Player 2 (P2)'].apply(lambda x: x in top_player_list)]
matchup_df=matchup_df.set_index(['Player 1 (P1)','Player 2 (P2)']).sort_values(by='P1 Global EM',ascending=False).reset_index()[['P1 Global EM','Player 1 Name','Player 2 Name']].iloc[-10:]

matchup_string = list(map(bar_graph_header,matchup_df['Player 1 Name'],matchup_df['Player 2 Name']))[::-1]
matchup_EMs = list(matchup_df['P1 Global EM'])[::-1]

fig, ax = plt.subplots()    
width = 0.75 # the width of the bars 
ind = np.arange(len(matchup_EMs))  # the x locations for the groups

ax.barh(ind, matchup_EMs, width, color="red")
ax.set_yticks(ind+width/2-.5)
ax.set_yticklabels(matchup_string, minor=False)
plt.title('Post 1991 matchups',fontsize=20)
plt.xlabel('Matchup EM',fontsize=20)
plt.ylabel('Player matchup',fontsize=20)      
ax.set_aspect(aspect=0.007)
for i, v in enumerate(matchup_EMs):
    ax.text(v+.0075, i-.25, str(round(v,3)), color='white', fontweight='bold')
plt.savefig(os.path.join('worst_EM_matchups.png'), dpi=300, format='png', bbox_inches='tight') # use format='svg' or 'pdf' for vectorial pictures
plt.show()

#%%

#let's get the top 10 head-to-head EM's amongst active player matchups
matchup_df=df.copy().reset_index()
matchup_df=matchup_df[matchup_df['Number of Matches']>minMatches]
matchup_df["Player 1 Name"]=matchup_df["Player 1 (P1)"].apply(lambda x: id_to_name[x])
matchup_df["Player 2 Name"]=matchup_df["Player 2 (P2)"].apply(lambda x: id_to_name[x])
matchup_df=matchup_df[matchup_df['Player 1 (P1)'].apply(lambda x: x in top_player_list) & matchup_df['Player 2 (P2)'].apply(lambda x: x in top_player_list)]
matchup_df=matchup_df.set_index(['Player 1 (P1)','Player 2 (P2)']).sort_values(by='P1 Global EM',ascending=False).reset_index()[['P1 Global EM','Player 1 Name','Player 2 Name']]

recent_matchup_df=matchup_df[matchup_df["Player 1 Name"].apply(lambda x: name_to_id[x] in active_player_list) & \
                 matchup_df["Player 2 Name"].apply(lambda x: name_to_id[x] in active_player_list)][:10]

matchup_string = list(map(bar_graph_header,recent_matchup_df['Player 1 Name'],recent_matchup_df['Player 2 Name']))[::-1]
matchup_EMs = list(recent_matchup_df['P1 Global EM'])[::-1]

fig, ax = plt.subplots()    
width = 0.75 # the width of the bars 
ind = np.arange(len(matchup_EMs))  # the x locations for the groups

ax.barh(ind, matchup_EMs, width, color="dodgerblue")
ax.set_yticks(ind+width/2-.5)
ax.set_yticklabels(matchup_string, minor=False)
plt.title('Active player matchups',fontsize=20)
plt.xlabel('Matchup EM',fontsize=20)
plt.ylabel('Player matchup',fontsize=20)      
ax.set_aspect(aspect=0.004)
for i, v in enumerate(matchup_EMs):
    ax.text(v-.0075, i-.25, str(round(v,3)), color='white', fontweight='bold')
plt.savefig(os.path.join('active_players_top_EM_matchups.png'), dpi=300, format='png', bbox_inches='tight') # use format='svg' or 'pdf' for vectorial pictures
plt.show()


#%%

#let's get the bottom 10 head-to-head EM's amongst active player matchups

matchup_df=df.reset_index()
matchup_df=matchup_df[matchup_df['Number of Matches']>minMatches]
matchup_df["Player 1 Name"]=matchup_df["Player 1 (P1)"].apply(lambda x: id_to_name[x])
matchup_df["Player 2 Name"]=matchup_df["Player 2 (P2)"].apply(lambda x: id_to_name[x])
matchup_df=matchup_df[matchup_df['Player 1 (P1)'].apply(lambda x: x in top_player_list) & matchup_df['Player 2 (P2)'].apply(lambda x: x in top_player_list)]
matchup_df=matchup_df.set_index(['Player 1 (P1)','Player 2 (P2)']).sort_values(by='P1 Global EM',ascending=False).reset_index()[['P1 Global EM','Player 1 Name','Player 2 Name']]
recent_matchup_df=matchup_df[matchup_df["Player 1 Name"].apply(lambda x: name_to_id[x] in active_player_list) & \
                 matchup_df["Player 2 Name"].apply(lambda x: name_to_id[x] in active_player_list)][-10:]
matchup_string = list(map(bar_graph_header,recent_matchup_df['Player 1 Name'],recent_matchup_df['Player 2 Name']))[::-1]
matchup_EMs = list(recent_matchup_df['P1 Global EM'])[::-1]

fig, ax = plt.subplots()    
width = 0.75 # the width of the bars 
ind = np.arange(len(matchup_EMs))  # the x locations for the groups

ax.barh(ind, matchup_EMs, width, color="red")
ax.set_yticks(ind+width/2-.5)
ax.set_yticklabels(matchup_string, minor=False)
plt.title('Active player matchups',fontsize=20)
plt.xlabel('Matchup EM',fontsize=20)
plt.ylabel('Player matchup',fontsize=20)      
ax.set_aspect(aspect=0.007)
for i, v in enumerate(matchup_EMs):
    ax.text(v+.0075, i-.25, str(round(v,3)), color='white', fontweight='bold')
plt.savefig(os.path.join('active_players_worst_EM_matchups.png'), dpi=300, format='png', bbox_inches='tight') # use format='svg' or 'pdf' for vectorial pictures
plt.show()

#%%

#as a case study, I want to look at all the matchup EM's for Goran Ivanisevic for players he
#played at least 5 times
#this will give us an idea of how serving strategy can change against opponent for a particular 
#opponent

goran_df=df.copy().loc[name_to_id['Goran Ivanisevic']].reset_index()
#cut data to matchups with over 5 matches
goran_df=goran_df[goran_df['Number of Matches']>5]
#create column to store string version of opponent name
goran_df['Opponent Name']=goran_df['Player 2 (P2)'].apply(lambda x: id_to_name[x])
goran_df=goran_df[['Opponent Name','P1 Global EM']].sort_values(by='P1 Global EM',ascending=False)

EMs=list(goran_df['P1 Global EM'][::-1])
opp_names=list(goran_df['Opponent Name'][::-1])
colors=list(goran_df['P1 Global EM'].apply(lambda x: 'dodgerblue' if x>0 else 'red'))[::-1]

plt.clf()
plt.rc('xtick',labelsize=8)
fig, ax = plt.subplots()    
width = 3 # the width of the bars 
ind = np.arange(len(EMs))  # the x locations for the groups
ax.barh(5*ind, EMs, width, color=colors)
ax.set_yticks(5*ind+width/2-.5)
ax.set_yticklabels(opp_names, minor=False,fontsize=6)
plt.title('Goran Ivanisevic EM vs. Opponent',fontsize=8)
plt.xlabel('EM Factor',fontsize=8)
plt.ylabel('Opponent',fontsize=8)      
ax.set_aspect(aspect=0.001)
for i, v in enumerate(EMs):
    if v>=0:
        spacing=-.009
    else:
        spacing=.001
    if not (i==5 or i==6 or i==7):
        ax.text(v+spacing, 5*ind[i]-.5, str(abs(round(v,3))), color='white', fontsize=4,fontweight='bold')
plt.savefig(os.path.join('Goran_Ivanisevic_matchup_EM.png'), dpi=300, format='png', bbox_inches='tight') # use format='svg' or 'pdf' for vectorial pictures
plt.show()


#%%

plt.figure()
plt.clf()
plt.hist(df.loc[name_to_id['Fernando Verdasco'],name_to_id['Rafael Nadal']].iloc[2])

#%%

plt.figure()
plt.clf()
print(np.mean(df.copy().reset_index().set_index(['Player 1 (P1)']).loc[name_to_id['Fernando Verdasco']]['P1 Total EM Series'].sum())
plt.hist(df.copy().reset_index().set_index(['Player 1 (P1)']).loc[name_to_id['Fernando Verdasco']]['P1 Total EM Series'].sum())
