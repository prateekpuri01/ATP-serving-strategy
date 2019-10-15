# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 20:11:17 2019

#File extracts list of player who have appeared in top 50 at some point in ATP career
"""
path="C:\\Users\\Anjana Puri\\Documents\\Python\\TennisProject\\JosephSackmann Data\\tennis_atp-master\\tennis_atp-master"
os.chdir(path)
f=open('atp_rankings_90s.csv','r')
years=list(range(1990,2019))
yeartrack=0
rankings=[[]]*len(years)
num_players_to_grab=29
len_years=len(years)

while not yeartrack==len_years:
    line=f.readline()
    try:
        current_year=int(line.split(",")[0][:4])
    except ValueError:
        continue
    except AttributeError:
        continue
    
    if current_year==years[yeartrack]:
        rankings[yeartrack].append(line.split(",")[2])
        for i in range(num_players_to_grab):
            line=f.readline()
            rankings[yeartrack].append(line.split(",")[2])
        yeartrack+=1   
     
    if yeartrack==len_years:
        break
       
    if years[yeartrack]==2000:
        f=open('atp_rankings_00s.csv','r')
        
    elif years[yeartrack]==2010:
        f=open('atp_rankings_10s.csv','r')
#
#%%
flat_list = list(set([item for sublist in rankings for item in sublist]))

with open('top_'+str(num_players_to_grab+1)+'_players.csv', 'w') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerows(flat_list)
csvFile.close()
       
    
    
