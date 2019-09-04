# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 12:47:38 2019

In this file, I am going to compare my Monte Carlo results to the real-life-win percentages in different player matchups
This will allow me to estimate the expected real life win probability change that would occur if players were to switch
serving strategies

@author: Prateek Puri
"""

import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt    
from scipy import stats
import pandas as pd
import pickle
import os
import csv
import matplotlib.pylab as pylab

#set plot parameters
params = {'legend.fontsize': 'xx-large',
          'figure.figsize': (15, 5),
         'axes.labelsize': 'x-large',
         'axes.titlesize':'xx-large',
         'xtick.labelsize':'xx-large',
         'ytick.labelsize':'xx-large'}
pylab.rcParams.update(params)

# pip install uncertainties, if needed
try:
    import uncertainties.unumpy as unp
    import uncertainties as unc
except:
    try:
        from pip import main as pipmain
    except:
        from pip._internal import main as pipmain
    pipmain(['install','uncertainties'])
    import uncertainties.unumpy as unp
    import uncertainties as unc

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

    
with open('active_players.csv', 'r') as f:
    reader = csv.reader(f)
    player_list = list(reader)
active_player_list=[''.join(x) for x in list(filter(lambda a: a != [], player_list))]    


os.chdir('C:/Users/Anjana Puri/Documents/Python/TennisProject/JosephSackmann Data/tennis_atp-master/tennis_atp-master')
mc_df= pd.read_pickle('MC_results.pkl')

#%%

#first I'm going to take the 'timid' strategy MC results and compare them to real life head-to-head winning percentages
minMatches=10
plt.clf()
xlist=mc_df[mc_df['Real life number of matches']>=minMatches]["Timid MC win percentage"] #get timid MC winning percentages
ylist=mc_df[mc_df['Real life number of matches']>=minMatches]["Real life win percentages"]   #get real life winning percentages
errors=list(mc_df[mc_df['Real life number of matches']>=minMatches]["Timid MC results"].apply(lambda x: np.std(x))) #calculate spread in MC results

x = xlist
y = ylist
n = len(y)

def f(x, a, b): #fit function that will be used to map xlist to ylist
    return a*x + b

popt, pcov = curve_fit(f, x, y) #fit function to data

# retrieve parameter values
a = popt[0] #get fit parameters
b = popt[1]
print('Optimal Values')
print('a: ' + str(a))
print('b: ' + str(b))

# compute r^2
r2 = 1.0-(sum((y-f(x,a,b))**2)/((n-1.0)*np.var(y,ddof=1)))
print('R^2: ' + str(r2))

# calculate parameter confidence interval
a,b = unc.correlated_values(popt, pcov)
print('Uncertainty')
print('a: ' + str(a))
print('b: ' + str(b))

# plot data
plt.errorbar(list(xlist), list(ylist), xerr=errors, fmt='o',markersize=10,capsize=10,alpha=.5)
plt.xlim(-.05,1.05)
plt.ylim(-.05,1.05)
# calculate regression confidence interval
px = np.linspace(-.2, 1.2, 100)
py = a*px+b
nom = unp.nominal_values(py) 
std = unp.std_devs(py)

def predband(x, xd, yd, p, func, conf=0.95): #function that plots prediction bands
    # x = requested points
    # xd = x data
    # yd = y data
    # p = parameters
    # func = function name
    alpha = 1.0 - conf    # significance
    N = xd.size          # data sample size
    var_n = len(p)  # number of parameters
    # Quantile of Student's t distribution for p=(1-alpha/2)
    q = stats.t.ppf(1.0 - alpha / 2.0, N - var_n)
    # Stdev of an individual measurement
    se = np.sqrt(1. / (N - var_n) * \
                 np.sum((yd - func(xd, *p)) ** 2))
    # Auxiliary definitions
    sx = (x - xd.mean()) ** 2
    sxd = np.sum((xd - xd.mean()) ** 2)
    # Predicted values (best-fit model)
    yp = func(x, *p)
    # Prediction band
    dy = q * se * np.sqrt(1.0+ (1.0/N) + (sx/sxd))
    # Upper & lower prediction bands.
    lpb, upb = yp - dy, yp + dy
    return lpb, upb

lpb, upb = predband(px, x, y, popt, f, conf=0.95) #get upper and lower prediction bands

# plot the regression


# uncertainty lines (95% confidence)
plt.plot(px, nom - 1.96 * std, c='orange',\
         label='95% Confidence Region')
plt.plot(px, nom + 1.96 * std, c='orange')
plt.fill_between(px,nom-1.96*std,nom+1.96*std,alpha=.5,color='orange')
# prediction band (95% confidence)
plt.plot(px, lpb, 'k--',label='95% Prediction Band')
plt.plot(px, upb, 'k--')
plt.ylabel('Actual Win Fraction',fontsize=20)
plt.xlabel('Simulated Win Fraction',fontsize=20)
plt.legend(loc='best')
# save and show figure
plt.tight_layout()
plt.savefig('monte_carlo_calibration.png')
plt.show()


#%%

model_scale=a.nominal_value #redefine parameter values and errors for fit function
model_scale_std=a.std_dev
model_offset=b.nominal_value
model_offset_std=b.std_dev
mc_df= pd.read_pickle('MC_results.pkl')

def calculate_diff(WP1,WP2): #WP1 = MC winning percentage with strategy (x), WP2= MC winning percentage with strategy (y)
                            #return: expected difference in real-life win percentages according to earlier fit function
    return model_scale*(WP1-WP2)

def calculate_diff_errors(WP1,WP2): #calculates 68% confidence interval standard errors, againt according to fit function
    err1=((WP1**2)*(model_scale_std**2)+model_offset_std**2)**.5 #error associated with WP1
    err2=((WP2**2)*(model_scale_std**2)+model_offset_std**2)**.5 #error associated with WP2
    return (err1**2+err2**2)**.5 #quadruture sum error

def bar_graph_header(p1,p2): #return string tha reads 'p1 vs. p2' 
    return p1+ " vs. " + p2

mc_df=mc_df[mc_df['Real life number of matches']>=minMatches]
mc_df['Model differences']=list(map(calculate_diff,mc_df['Bold MC win percentage'],mc_df['Timid MC win percentage']))
mc_df['Model difference errors']=list(map(calculate_diff_errors,mc_df['Bold MC win percentage'],mc_df['Timid MC win percentage']))


#%%
all_matchups_list=mc_df.copy().reset_index()[['Player 1 Name','Player 2 Name','Model differences','Model difference errors']].sort_values(by='Model differences',ascending=False).iloc[:10]
matchup_labels = list(map(bar_graph_header,all_matchups_list['Player 1 Name'],all_matchups_list['Player 2 Name']))[::-1]
model_differences = list(all_matchups_list['Model differences'])[::-1]

fig, ax = plt.subplots()    
width = 0.75 # the width of the bars 
ind = np.arange(len(model_differences))  # the x locations for the groups

ax.barh(ind, model_differences, width, xerr=all_matchups_list['Model difference errors'],capsize=10,color="dodgerblue")
ax.set_yticks(ind+width/2)
ax.set_yticklabels(matchup_labels, minor=False)
plt.title('Post 1991 matchups')
plt.xlabel('Difference in match winning percentage',fontsize=20)
plt.ylabel('Player matchup',fontsize=20)      
for i, v in enumerate(model_differences):
    ax.text(v-.015, i-.20, str(round(v,3)), color='white', fontweight='bold')
plt.savefig(os.path.join('best_win_enhancement.png'), dpi=300, format='png', bbox_inches='tight') # use format='svg' or 'pdf' for vectorial pictures
plt.show()
#%%
all_matchups_list=mc_df.copy().reset_index()[['Player 1 Name','Player 2 Name','Model differences','Model difference errors']].sort_values(by='Model differences',ascending=True).iloc[:10]
matchup_labels = list(map(bar_graph_header,all_matchups_list['Player 1 Name'],all_matchups_list['Player 2 Name']))[::-1]
model_differences = list(all_matchups_list['Model differences'])[::-1]

fig, ax = plt.subplots()    
width = 0.75 # the width of the bars 
ind = np.arange(len(model_differences))  # the x locations for the groups
ax.barh(ind, model_differences, width, xerr=all_matchups_list['Model difference errors'],capsize=10,color="red")
ax.set_yticks(ind+width/2)
ax.set_yticklabels(matchup_labels, minor=False)
plt.title('Post 1991 matchups')
plt.xlabel('Difference in match winning percentage',fontsize=20)
plt.ylabel('Player matchup',fontsize=20)      
for i, v in enumerate(model_differences):
    ax.text(v+.015, i-.20, str(round(v,3)), color='white', fontweight='bold')
plt.savefig(os.path.join('worst_win_enhancement.png'), dpi=300, format='png', bbox_inches='tight') # use format='svg' or 'pdf' for vectorial pictures
plt.show()


#%%

active_matchup_list=mc_df.copy().reset_index()[['Player 1 (P1)','Player 2 (P2)','Player 1 Name','Player 2 Name','Model differences','Model difference errors']].sort_values(by='Model differences',ascending=False)
selection1=list(active_matchup_list['Player 1 (P1)'].apply(lambda x:  True if x in active_player_list else False))
active_matchup_list=active_matchup_list[selection1]
selection2=list(active_matchup_list['Player 2 (P2)'].apply(lambda x: True if x in active_player_list else False))
active_matchup_list=active_matchup_list[selection2][['Player 1 Name','Player 2 Name','Model differences','Model difference errors']].iloc[:10]

matchup_labels = list(map(bar_graph_header,active_matchup_list['Player 1 Name'],active_matchup_list['Player 2 Name']))[::-1]
model_differences = list(active_matchup_list['Model differences'])[::-1]

fig, ax = plt.subplots()    
width = 0.75 # the width of the bars 
ind = np.arange(len(model_differences))  # the x locations for the groups
ax.barh(ind, model_differences, width, xerr=active_matchup_list['Model difference errors'],capsize=10,color="dodgerblue")
ax.set_yticks(ind+width/2)
ax.set_yticklabels(matchup_labels, minor=False)
plt.title('Active player matchups',fontsize=20)
plt.xlabel('Difference in match winning percentage',fontsize=20)
plt.ylabel('Player matchup',fontsize=20)      
for i, v in enumerate(model_differences):
    ax.text(v-.015, i-.20, str(round(v,3)), color='white', fontweight='bold')
plt.savefig(os.path.join('active_players_best_win_enhancement.png'), dpi=300, format='png', bbox_inches='tight') # use format='svg' or 'pdf' for vectorial pictures
plt.show()


#%%
active_matchup_list=mc_df.copy().reset_index()[['Player 1 (P1)','Player 2 (P2)','Player 1 Name','Player 2 Name','Model differences','Model difference errors']].sort_values(by='Model differences')
selection1=list(active_matchup_list['Player 1 (P1)'].apply(lambda x:  True if x in active_player_list else False))
active_matchup_list=active_matchup_list[selection1]
selection2=list(active_matchup_list['Player 2 (P2)'].apply(lambda x: True if x in active_player_list else False))
active_matchup_list=active_matchup_list[selection2][['Player 1 Name','Player 2 Name','Model differences','Model difference errors']].iloc[:10]

matchup_labels = list(map(bar_graph_header,active_matchup_list['Player 1 Name'],active_matchup_list['Player 2 Name']))[::-1]
model_differences = list(active_matchup_list['Model differences'])[::-1]

fig, ax = plt.subplots()    
width = 0.75 # the width of the bars 
ind = np.arange(len(model_differences))  # the x locations for the groups
ax.barh(ind, model_differences, width, xerr=active_matchup_list['Model difference errors'],capsize=10,color="red")
ax.set_yticks(ind+width/2)
ax.set_yticklabels(matchup_labels , minor=False)
plt.title('Active player matchups')
plt.xlabel('Difference in match winning percentage',fontsize=20)
plt.ylabel('Player matchup',fontsize=20)      
for i, v in enumerate(model_differences):
    ax.text(v+.015, i-.20, str(round(v,3)), color='white', fontweight='bold')
plt.savefig(os.path.join('active_players_worst_win_enhancement.png'), dpi=300, format='png', bbox_inches='tight') # use format='svg' or 'pdf' for vectorial pictures
plt.show()