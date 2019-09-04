# ATP serving strategy analysis

Tennis is a sport in which players alternate serving. Each server is allowed two attempts to make a serve before being penalized a point for what is known as a 'double fault'. The conventional strategy is for a server to first hit a difficult, high-speed 'first serve' and then to hit a safer, lower-speed 'second serve' if his/her first serve did not go in. While this strategy is sound for many players, this project aims to identify matchups in which it may be beneficial for players to elect for a riskier strategy in which two first serves are attempted on all service points. The hope is the results of this study can be used to guide player strategies in hopes of optimizing match performance.

# Data statement
All data that this project was based on was retrieved from Jeff Sackmann's wonderful ATP data repository available at: https://github.com/JeffSackmann/tennis_atp
The data contained information on matches from 1991-2019, and thus my analysis is retricted to this subset. Further, matches with players with fewer that 50 career ATP matches were cut from the dataset in order to further restrict my analysis to players with significant ATP experience. 

This data exclusively contains information on ATP matches (not WTA matches), and thus any conclusions drawn will be most relevant to ATP players. 

# Framing the problem

The goal of this analysis project is to determine what the most optimal serving strategy is for a given player. 
To frame this problem, let us first define a few parameters for each player:

First serve percentage (FSP): The percentage of times a server makes his/her first serve
First serve winning percentage (FSWP): The percentage of points that a server wins if his/her first serve lands in
First serve percentage (SSP): The percentage of times that a server makes his/her second serve
First serve winning percentage (SSWP): The percentage of points that a server wins if his/her second serve lands in

To get feel for how these parameters vary across the ATP, we can plot both serve winning percentage and serve make percentage for all ATP players in our dataset. 

![](/data_visualizations/serve_make_percentages_hist.png?raw=true)
![](/data_visualizations/serve_winning_percentages_hist.png?raw=true)

There are two main trends to observe here. Firstly, first serves are more difficult to make than second serves, as expected, with an average ATP FSP of 59% as compared to a SSP average of 89%. However, the ease of making second serves comes at a price; namely, second serve points are harded to win with an ATP average SSWP of just 48% as compared to an average FSWP of 68%. 

Moreover, how a player peforms on his/her second serve is rather uncorrelated to how the player performs on his/her first serve, as demonstrated by the following graphs that plots FSWP vs. SSWP

![](/data_visualizations/first_serve_second_serve_correaltion.png?raw=true)

The lack of strong correlation, demonstrated by the R^2 coefficient of 0.2, suggests that it may be difficult to globally apply an optimal serving strategy to all ATP players. Rather, serving strategies may need to be adjusted to each individual player to account for their first/second serve strengths and weaknesses. 

# Caveats

There a few assumptions that have been made throughout my modeling. Please see the bottom of this document for further details.

# Serving strategies

Now there are two serving strategies that are going to be analyzed here

(1) Player hit a first serve and then second serve if needed 
(2) Player hit a first serve and then hits another first serve if needed

Strategy (1) is fairly conventional and has been adopted by nearly all ATP players historically. Strategy (2), on the other hand, has more of a 'high risk/high reward' element. By hitting two first serves, the player has a higher chance of winning a servus point if one of his/her serves goes in, but he/she also has a higher risk of double faulting. However, depending on how weak the player's second serve is, this additional risk may still be advantageous. 

These strategies are identical except for the second serve that is hit. Therefore, to asses the differences in probability (Delta P) of winning a servus point under the two strategies we can define the following quantity, known as the 'enhancement metric':

EM = FSP x FSWP-SSP x SSWP

Conceptually, we are saying that the probability of winning a second serve is: 
(chances of making the serve) x (probability of winning point if serve is in)

For strategy (1), this quantity is FSP x FSWP, whereas for strategy (2), this quantity is SSP x SSWP, and the EM factor simply is the difference in these quantities. Thus the EM factor is equivalent to the increase in probability of winning a servus point obtained from switching from strategy (1) to strategy (2) (Delta P). 

Therefore, an EM factor>0 may imply that strategy (2) would be advantagous over strategy (1) for a particular player, while a EM factor<0 would imply the opposite. 

# Analyzing the EM factor

The following plot is a histogram of the EM factor for ATP players, averaged all matches that they have played that are recorded in the ATP database

![](/data_visualizations/ATP_EM.png?raw=true)

As can been seen, the average EM factor is < 0, implying that strategy (1) may be optimal for most players; however, there seems to several players with EM factors>0. We can list the players with the highest EM factors averaged over their career

![](/data_visualizations/career_top_EM.png?raw=true)

We can also restrict this table to active players

![](/data_visualizations/active_player_top_career_EM.png?raw=true)

As we can see, there are certain players who could expect to win over 5% more servus points, on average, by switching from strategy (1) to strategy (2). The majority of players listed in these tables are known for having powerful first serves, which makes strategy (2) beneficial for them since it allows them to put as many first serves in play as possible. Further, many of these players are not known for being particularly adept in length baseline exchanges, which can frequently occur during second serves since the return is put in play at a high rate. The second factor serves to decrease their SSWP and further make strategy (2) more favorable. 

Now these tables averaged serving statistics across all recorded career matches. However, in reality, a player's FSWP and SSWP will depend on who they are playing. Is it always advantageous for a player with career EM Factors>0 to employ serving strategy (2)? Perhaps not. As a case study, look at Goran Ivanisevic's EM versus all opponents he's played at least **5 matches** with. 

![](/data_visualizations/Goran_Table.png?raw=true)

Even though Ivanisevic's career EM is quite high (.028), we see that his EM factor against certain opponent varies quite a bit. Even though on average, he would appear to benefit from strategy (2), against certain opponents strategy (1) is preferable. 

The simple fact is that certain players return first/second serves well against certain other players while others do not. Therefore, we can reconstruct the above tables while restricting ourselves to a player's serving statistics against a particular player. Here, we will restrict ourselves to players who have played each other a minimum of **10 times** so that we may have a resonable amount of data to sample.

In these tables, the first name refers to the player who is serving and the second serve refers the player whom he is serving against

![](/data_visualizations/top_EM_matchups.png?raw=true)

Once again we can also restrict ourself to active player matchups

![](/data_visualizations/active_player_top_EM_matchups.png?raw=true)

These tables, for the most part, are filled with players with powerful first serves who are playing opponents known for strong baseline games. Against these crafty baseline players, the servers do not have a high chance of winning their second serve points; therefore, they can benefit by hitting their more powerful serves more often, even at the expense of additional double faults. 

We can take Pete Sampras vs Andre Agassi as a case study. According to my results, Sampras coud have won roughly 6.1% more servus points by switching to strategy (2) from strategy (1). Why? Sampras is known for having an incredible serve; however, Agassi is also regarded as one of the best serve returners of all time. However, when these two forces collide on second serve points, Agassi has the advantage. His strong return game gave him a 54% chance of winning the point, however this dropped to just 20% when Sampras made his first serve. The EM factor results suggest that Sampras can nullify Agassi's strong return by putting his first serve in play more often.  i

# Modeling how strategy switches can modify match outcomes

The above analysis informs us that certain players may win more servus points by switching from strategy (1) to strategy (2). But how is this going to affect how often they win the match? After all, whether they win or not is the most important statistic of them all. One way to approach this problem is to perform roughly 1000 Monte Carlo simulations of matches between two players, taking into account their serve statistics against one another. By determining each player's FSWP and SSWP percentages against their opponent, points can be simulated, which allows games, sets, and eventually matches to be simulated as well. 

First question: How trust worthy are Monte Carlo (MC) simulations at predicting match outcomes. To assess this question, I performed my MC analysis on all head-t-head player matchups with a match history of at least five matches. I then compared by MC results to each players win-loss record against his opponent. In this initial Monte Carlo simulation, I assumed each player obeyed strategy (1), as an overwhelmingly the case with ATP players.

Here are the results, along with confidence and prediction bands to a linear fit to the data

![](/data_visualizations/monte_carlo_calibration.png?raw=true)

The Monte Carlo simulation appears to be a reasonable predictor of head-to-head winning percentage. The noise in the fit can be attributed to a couple different reasons. 

1) Player matchups depend on surface type. In tennis, there are three main surfaces: clay, grass, and hard court. If two players have played a majority of their matches on clay, their head-to-head serving statistics will be dominated by their clay court encounters. However, these percentages may not apply well to a matchup on grass, for example. My MC simulation does not explicity account for surface type. It indirectly accounts for it by weighting the surface that has played on the most often in the head-to-head serving statistics; however, an updated model that directly accounts for surface type would be an improvement. 

2) Winning percentages changes throughout matches. My MC simulation assumes a player's chances of winning a servus point is static throughout a match, but in reality, these percentages may change more for some players than others due to physical fatigue, mental toughness, etc. 

3) Low statistics. It is quite rare for players to have more than 10 matches against one another. Therefore, it is not entirely unlikely that an actual player's winning percentage against a certain player has not yet regressed to the mean it would approach if they had played roughly a 1000 times, as is the case with the MC simulations. 

# Final results

I can now repeat my Monte Carlo simulations when using two serving strategies: strategy (1) and strategy (2). After performing the simulations, ising the linear fit function that I calculated in the previous section that calibrated MC results to real-life winning percentage, I can then translate the Monte Carlo results to expected real life win percentages. 

The following table displays the largest increase in winning percentages expected from switching from strategy (1) to strategy (2) for both post-1991 (first table) and active (second table) player matchups. The error bars represent 68% confidence interval bands based on errors to the fit function in the previous section.

![](/data_visualizations/best_win_enhancement.png?raw=true)
![](/data_visualizations/active_players_win_enhancement.png?raw=true)

As can be seen from the tables, there are some players who could increase their expected win percentage by more than 10% by switching serving strategies.

As expected, many matchup from the EM Factor table reappear with a few notable exceptions. For example, while Novak Djokovic was expected to win roughly 5% more servus points from switching strategies against Kei Nishikori, which was tops for active players, their matchup did not place in the top 10 in match winning percentage enhancement. This may attributed to the fact that Novak's head-to-head record against Kei is 16-2, or in other words, he doesn't have much room to improve. On the other hand, for the Monfils vs. Gasquet matchup, Monfils was also expected to win roughly 5% more servus points by switching strategies. However, he is just 10-7 against Gasquet, so that servus point win percentage increase was enough to catapault his expected match winning percentage by rougly 10%. 

# Conclusion

Tennis, in general, is a game of slim margins. Especially when playing an opponent who you are evenly matched against, small increases in point winning percentage may be able to push you over the edge and allow you to win matchups at non-trivially higher percentages. The analysis conducted here suggests that for certain players whose first serve is quite strong and whose second serve may be a vulnerability against certain opponents, changing serving tactics may in fact provide a slight edge in serve winning percentage and overall match winning percentage as well. 

In general, whether a strategy (1) or a strategy (2) approach is more successful depends both on the player and who he is facing. However, if certain cases, players may be able to improve their winning percentage against a particular opponents by over 10% by switching to an all-first-serve strategy.

# Caveats and suggestions for improvement

The following assumptions are inherent to the modeling in this project

*Caveats*

1) **Players serves percentages are static**

This may not always be the case. It's one thing to fire away first serves at the beginning of a match and quite another to do so when down three match points. My modeling assumes that a player is able to perform the same under strategy (2) in both situations. But if a player is facing a match point, will he be able to hit first serves at the same percentage he has been all match? Further analysis is needed to address this concern fully. 

However, if such an effect does in fact prove to be significant, perhaps mental training or coaching could dampen the effect if a strategy (2) approach is desired.

2) **Fatigue is not an issue**

If pursuing a strategy (2) approach, hitting increased amounts of first serves may cause players to tire and thus to reduce their serving percentages. It's unclear if this effect is significant. Further, if electing to pursue a strategy (2) approach, the average point and game length will likely be shorter than when pursuing a strategy (1) approach since first serve points tend to be shorter than second serve points. Perhaps these two effects cancel out and perhaps they do not, but further analysis should be conducted in this realm.

3) **All previous data was obtained from players employing strategy (1)**

I'm assuming that the FSP, FSWP, SSP, and SSWP for each player that were used in the modeling were done by players using strategy (1) serving tactics. If players were using occasionally using strategy (2) tactics, than their second serves and first serves would be equivalent for particular matches, and therefore the SSP and SSWP percentages would be muddled with the FSP and FSWP percentages, rendering the modeling inaccurate. While certain players, such as Nick Krygrios, appear to utilize strategy (2) tactics occassionaly, these situations are rare. 

Further in the future, data that tracks the mph of each serve may be used to distinguish between 'first' and 'second' serves rather than relying solely on the order in which a serve was hit. 

*Room for improvment*

The Monte Carlo simulation proved to be an adequate tool for modeling player winning percentage; however, there was still a nontrivial amount of error associated with this mapping. In the future the Monte Carlo method may be replaced by a machine learning algorithm that may be able to more accurately predict player winning percentages and therefore be employed to more accurately asses the impact of serving strategy on player performance. 

Similarly, data split based off of surface type of length of match (best of 3 sets vs. best of 5 sets) may also be incorporate to more accurately predict player performance when using different strategies. 

Lastly, there are two options for each player in this study: hit a first serve or hit a second serve. In reality, there is a continuum in between these poles, and for certain players, it may very well be that hitting a serve that is halfway in between these two extremes may actually be the optimal strategy. In order to explore these alternative strategies, data on serve effectiveness vs. serve speed, as well as serve placement, would be very useful. 



















