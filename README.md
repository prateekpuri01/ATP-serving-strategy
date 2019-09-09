# ATP serving strategy analysis

Tennis is a sport in which players alternate serving. Each server is allowed two attempts to make a serve before being penalized a point for what is known as a 'double fault'. The conventional is for a server to first hit a difficult, high-speed 'first serve' and then to hit a safer, lower-speed 'second serve' if his/her first serve did not go in. While this strategy is sound for many players, this project aims to identify head-to-head player matchups in which it may be beneficial for players to elect for a riskier strategy in which two first serves are attempted on all service points. The hope is the results of this study can be used to guide player strategies and optimize match performance.

# Data statement
All data that this project was based on was retrieved from Jeff Sackmann's wonderful ATP data repository available at: https://github.com/JeffSackmann/tennis_atp

The data files contain information on ATP matches from 1991-2019, and thus my analysis is retricted to this subset. Further, matches with players with fewer than 50 career ATP matches were cut from the dataset in order to further restrict my analysis to players with significant ATP experience. Lastly, matches in which each player hit fewer than 20 first serves or fewer than 10 second serves were excluded from the dataset to effectively remove matches decided by player retirement or other unusual circumstances. 

This dataset exclusively contains information on ATP matches (not WTA matches), and thus any conclusions drawn will be most relevant to ATP players. 

# Framing the problem

The goal of this analysis project is to determine what the optimal serving strategy is for a given player. 
To frame this problem, let us first define a few parameters for each player:

**First serve percentage (FSP)**: The percentage of times a server makes his/her first serve <br/>
**First serve winning percentage (FSWP)**: The percentage of points that a server wins if his/her first serve lands in <br/>
**Second serve percentage (SSP)**: The percentage of times that a server makes his/her second serve <br/>
**Second serve winning percentage (SSWP)**: The percentage of points that a server wins if his/her second serve lands in <br/>

To get feel for how these parameters vary across the ATP, we can plot both serve winning percentage (FSWP,SSWP) and serve make percentage (FSP,SSP) for all ATP players in our dataset. 

![](/data_visualizations/serve_make_percentages_hist.png?raw=true)
![](/data_visualizations/serve_winning_percentages_hist.png?raw=true)

There are two main trends to observe here. Firstly, first serves are more difficult to make than second serves, as expected, with an average ATP FSP of 60% as compared to a SSP average of 89%. However, the ease of making second serves comes at a price. Namely, second serve points are harder to win than first serve points, with an ATP average SSWP of just 46% as compared to an average FSWP of 66%. 

Moreover, how an ATP player peforms on his second serve is rather uncorrelated to how the player performs on his first serve, as demonstrated by the following graphs that plots FSWP vs. SSWP

![](/data_visualizations/first_serve_second_serve_wp_correaltion.png?raw=true)

The lack of strong correlation, demonstrated by a R^2 coefficient of 0.2, suggests that it may be difficult to globally apply an optimal serving strategy to all ATP players. Rather, serving strategies may need to be adjusted to each individual player to account for their first/second serve strengths and weaknesses. 

# Caveats

There a few assumptions that have been made throughout my modeling. Please see the bottom of this document for further details.

# Serving strategies

There are two serving strategies that are going to be analyzed here

**Strategy (1)**: Player hits a first serve and then a second serve if needed   <br/>
**Strategy (2)**: Player hits a first serve and then hits another first serve if needed  <br/>

Strategy (1) is fairly conventional and has been adopted by nearly all ATP players historically. Strategy (2), on the other hand, is extremely rare to see deployed and has more of a 'high risk/high reward' element than strategy (2). By hitting a first serve as a second serve, a player has a higher chance of winning a second serve point if the serve goes in, but he also has a higher risk of double faulting. However, depending on how weak the player's second serve is, the benefit of the strategy may be worth the risk. 

Strategies (1) and (2) are identical except for the second serve that is hit. Therefore, to asses the differences in probability (Delta P) of winning a service point under the two strategies, we need only look at difference in probability of winning the second serve point. To asses this, we can define the following quantity, labeled the 'enhancement metric' (EM):

EM = FSP x FSWP-SSP x SSWP

Let's break this down. Conceptually, we are saying that the probability of winning a second serve point is: <br/>
(chances of making the serve) x (probability of winning the point if the serve is in)

For strategy (1), this quantity is FSP x FSWP, whereas for strategy (2), this quantity is SSP x SSWP, and the EM factor simply is the difference in these quantities. 

Thus the EM factor is equivalent to the increase in probability of winning a service point associated with switching from strategy (1) to strategy (2). Therefore, an EM factor>0 may imply that strategy (2) would be advantagous over strategy (1) for a particular player, while a EM factor<0 would imply the opposite. 

# Analyzing the EM factor

The following plot is a histogram of the career EM factors for ATP players, averaged across all matches that they have played that are recorded in the ATP database

![](/data_visualizations/ATP_EM.png?raw=true)

As can been seen from the dotted line, the average EM factor is < 0, implying that strategy (1) may be optimal for most players; however, there seems to several players with EM factors>0. We can list the players with the highest EM factors averaged over their career. **All tables in the remainder of this document will refer to player's who have been ranked in the top 30 at least once in their career**. 

![](/data_visualizations/career_top_EM.png?raw=true)

We can also restrict this table to active players (I note that as of the writing of this document, Julien Benneteau's retirement status in unclear and thus he will be considered active)

![](/data_visualizations/active_players_top_career_EM.png?raw=true)

As we can see, there are certain players who could expect to win over 5% more service points, on average, by switching from strategy (1) to strategy (2). 

Qualitatively, what determines whether a player will benefit from a strategy switch? Many of the players listed in these tables are known for having powerful first serves, which makes strategy (2) beneficial for them since it allows them to put as many first serves in play as possible. Further, many of these players are also not known for being particularly adept in lengthy baseline exchanges, which can frequently occur during second serves since the return is put into play at a higher rate in these points than it is with first serve points. This second factor serves to decrease these players' SSWP and make strategy (2) further favorable. 

The above tables display serving statistics averaged across all recorded career matches. However, in reality, a player's FSWP and SSWP will depend on who they are playing. Is it always advantageous for a player with a career EM Factor>0 to employ serving strategy (2)? Perhaps not. As a case study, look at Goran Ivanisevic's EM versus all opponents he's played at least **5 matches** with. 

![](/data_visualizations/Goran_Ivanisevic_matchup_EM.png?raw=true)

Even though Ivanisevic's career EM is quite high (.028), we see that his EM factor against certain opponent varies substantially. Even though, on average, he would appear to benefit from strategy (2), against certain opponents strategy (1) is clearly preferable. 

Certain opponents simply return first/second serves better than other opponents, and these effects will guide which strategy is optimal when playing them. Therefore, we can reconstruct the above tables while restricting ourselves to a player's serving statistics against a particular player. Here, we will restrict ourselves to players who have played each other a minimum of **10 times** so that we may have a resonable amount of data to sample.

In these tables, the first name refers to the player who is serving and the second name refers the player whom they are serving against

![](/data_visualizations/top_EM_matchups.png?raw=true)

Once again we can also restrict ourselves to active player matchups

![](/data_visualizations/active_players_top_EM_matchups.png?raw=true)

What are the qualitative similarities in these matchups? These tables, for the most part, are again filled with players with powerful first serves who are playing opponents known for strong baseline games. Their opponent's crafty baseline game may limit the server's ability to win second serve points; therefore, the server can benefit from hitting their more powerful first serve more often, even at the expense of additional double faults. 

We can take Patrick Rafter vs. Andre Agassi as a case study. According to the above table, Sampras coud have won roughly 7% more service points by switching to strategy (2) from strategy (1). Why? Agassi's strong return game gave him a 57% chance of winning a second serve point against After; however this dropped to just 28% when Rafter made his first serve. Rafter's high EM factor against Agassi results suggests that he may have been able to nullify Agassi's strong return game by putting his first serve in play more often. 

# Modeling how strategy switches can modify match outcomes

The above analysis informs us that certain players may win more service points by switching from strategy (1) to strategy (2). But how is this going to affect how often they win the match? After all, whether they win or not is the most important statistic of them all. One way to approach this problem is to perform Monte Carlo simulations of matches between two players, taking into account their serving statistics against one another. By determining each player's FSWP and SSWP percentages against their opponent, service points can be simulated for each player, which allows games, sets, and eventually matches to be simulated as well. Further, we can perform the simulations assuming a player uses strategy (1) during the match and then reperform the simulations assuming the player follows strategy (2), and finally, we can compare the differences. 

First question: How trustworthy are Monte Carlo (MC) simulations at predicting match outcomes? To assess this question, I performed my MC analysis on all head-to-head player matchups with a match history of **at least 5 matches** (10000 simulations per matchup, best-of-5 set matches). I then compared by MC results to each real life head-to-head win-loss record. In this initial MC simulation, I assumed each player obeyed strategy (1), as is overwhelmingly the case with ATP players.

In each simulation, each server's FSP and SSP was determined by randomly sampling from the server's distribution of FSP/SSP values acquired over all recorded matches in the player's career. This helps account for the fact that player serve make percentages are not static and do vary from match to match. On the other hand, each server's FSWP/SSWP was set by each quantity's average value against their opponent in the matchup being studied. In reality, each player's FSWP/SSWP also vary match-to-match; however, since such values are opponent-dependent and there are a relatively small number of matches in each matchup (<10), the average values were used as an approximation. 

Here are the results (x-error bars represent 68% confidence intervals), along with confidence and prediction bands to a linear fit to the data

![](/data_visualizations/monte_carlo_calibration.png?raw=true)

The MC simulations appear to be a reasonable predictor of head-to-head match winning percentage. The noise in the fit can be attributed to a few different reasons. 

1) Player matchups depend on surface type. In tennis, there are three main surfaces: clay, grass, and hard court. If two players have played a majority of their matches on clay, their head-to-head serving statistics will be dominated by their clay court encounters. However, these percentages may not apply well to a matchup on grass, for example. My MC simulation does not explicity account for surface type, and thus may inaccurately predict match outcomes for surfaces that have only been played on sparingly in a given player matchup. An updated model that directly accounts for surface type would be an improvement. 

2) Serve win percentage changes throughout matches. My MC simulation assumes a player's chances of winning a service point is static throughout a match, but in reality, these percentages may change more for some players than others due to physical fatigue, mental fraying, etc. 

3) Low statistics. It is quite rare for players to have played much more than 10 matches against one another. Therefore, it is not entirely unlikely that an actual player's winning percentage against a certain player has not yet regressed to the mean it would approach if they had played roughly a 1000 times, as is the case with the MC simulations. Further, due to the low match numbers between players, even incorrectly predicting a single match result can lead to nontrivial differences in winning percentage between the MC model predictions and the real-life results. 

# Final results

I can now repeat my Monte Carlo simulations when using two serving strategies: strategy (1) and strategy (2). After performing the simulations, I can convert the MC results to expected real life win percentages by using the linear fit calibration function that I calculated in the previous section.

The following table displays the largest expected increase in winning percentage expected from switching from strategy (1) to strategy (2) for both post-1991 (first table) and active (second table) player matchups. The error bars represent 68% confidence interval bands based on errors in the fit function in the previous section.

![](/data_visualizations/best_win_enhancement.png?raw=true)
![](/data_visualizations/active_players_best_win_enhancement.png?raw=true)

As can be seen from the tables, the results suggest that some players may be able to increase their expected win percentage by more than 10% against certain opponents by switching serving strategies. As expected, many player matchups from the earlier EM Factor table reappear in the MC tables, with a few exceptions.

# Conclusion

Tennis, in general, is a game of slim margins. Especially when playing an opponent who you are evenly matched against, small increases in point winning percentage may have large influences on match outcomes. The analysis conducted here suggests that for certain players whose first serve is quite strong and whose second serve may be a vulnerability against a particular opponent, changing serving tactics to an all-first-serve approach may in fact provide a slight edge in serve winning percentage and overall match winning percentage as well. 

In general, whether a strategy (1) or a strategy (2) approach is more successful depends both on the player and their opponent. However, in certain matchups, these results suggest players may be able to improve their winning percentage against their opponents by over 10% by switching to an all-first-serve strategy.

# Caveats and suggestions for improvement

The following assumptions are inherent to the modeling in this project

*Assumptions*

1) **Players serves percentages are static**

This may not always be the case. It's one thing to fire away first serves at the beginning of a match and quite another to do so at critical junctures. Under strategy (2), my modeling assumes that a player is able to serve with the same percentages in both situations. However, if a player is facing a match point, will they be able to hit first serves at the same percentage they have been all match? Further analysis is needed to address this concern fully. 

However, if such an effect does in fact prove to be significant, perhaps mental training or coaching could dampen the effect if a strategy (2) approach is desired.

2) **Fatigue is not an issue**

If pursuing a strategy (2) approach, hitting increased amounts of first serves may cause players to tire and thus to reduce their serving percentages over the course of a match. Data to assess this possibility has not been analyzed but the theory is certainly plausible. On the other hand, if electing to pursue strategy (2), the average point and game length will likely be shorter than when pursuing strategy (1) since first serve points tend to be shorter than second serve points. Perhaps these two effects cancel out and perhaps they do not, but further analysis should be conducted to address this. 

3) **All previous data was obtained from players employing strategy (1)**

I'm assuming that the FSP, FSWP, SSP, and SSWP metrics for each player that were used in the modeling were done by players using strategy (1) serving tactics. If players were using occasionally using strategy (2) tactics, than they would sometimes be hitting first serves as second serves, but this change would not be recorded as such in the match statistics. Therefore a player's SSP and SSWP percentages for those matches would be muddled with their FSP and FSWP percentages, rendering the modeling inaccurate. However, while certain players, such as Nick Krygrios, appear to utilize strategy (2) tactics occassionaly, these situations are rare; thus I do not expect this effect to be significant.

Further in the future, data that tracks the mph of each serve may be used to distinguish between 'first' and 'second' serves more accurately rather than relying solely on the order in which a serve was hit. 

*Room for improvment*

The Monte Carlo simulation proved to be an adequate tool for modeling player winning percentages; however, there was still a nontrivial amount of error associated with this mapping. In the future the Monte Carlo method may be replaced by a machine learning algorithm that may be able to more accurately predict player winning percentages and therefore be employed to more accurately asses the impact of serving strategy on player performance. 

Similarly, data splits based off of surface type and length of match (best of 3 sets vs. best of 5 sets) may also be incorporated into the modeling to more accurately predict player performance when using different strategies. 

Lastly, there are two options for each player in this study when hitting a second serve: hit their first serve again or hit their normal second serve. In reality, there is a continuum in between these poles, and for certain players, it may very well be that hitting a serve that is halfway in between these two extremes in speed may actually be the optimal strategy. In order to explore these alternative strategies, data on serve effectiveness vs. serve speed, as well as serve placement, would be very useful. 



















