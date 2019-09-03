# ATP_serving_strategy
Analysis of ATP tennis serving strategies


Tennis is a sport in which players alternate serving. Each server is allowed two attempts to make a serve before being penalized a point for what is known as a 'double fault'. The conventional strategy is for a server to first hit a difficult, high-speed 'first serve' and then to hit a safer, lower-speed 'second serve' if his/her first serve did not go in. While this strategy is sound for many players, this project aims to identify matchups in which it may be beneficial for players to elect for a riskier strategy in which two first serves are attempted on all service points. The hope is the results of this study can be used to guide player strategies in hopes of optimizing match performance.

All data that this project was based on was retrieved from Jeff Sackmann's wonderful ATP data repository available at: https://github.com/JeffSackmann/tennis_atp
The data contained information on matches from 1991-2019, and thus my analysis is retricted to this subset. Further, matches with players with fewer that 50 career ATP matches were cut from the dataset in order to further restrict my analysis to players with significant ATP experience. 

This data exclusively contains information on ATP matches (not WTA matches), and thus any conclusions drawn will be most relevant to ATP players. 

# Framing the problem

To frame this problem, let us first define a few parameters for each player

First serve percentage (FSP): The percentage of times a server makes his/her first serve
First serve winning percentage (FSWP): The percentage of points that a server wins if his/her first serve lands in
First serve percentage (SSP): The percentage of times that a server makes his/her second serve
First serve winning percentage (SSWP): The percentage of points that a server wins if his/her second serve lands in

To get feel for how these parameters vary across the ATP, we can plot both serve winning percentage and serve make percentage for all ATP players in our dataset. 

![](/data_visualizations/serve_make_percentages_hist.png?raw=true)
![](/data_visualizations/serve_winning_percentages_hist.png?raw=true)

There are two main trends to observe here. Firstly, first serves are more difficult to make than second serves, as expected, with an average ATP FSP of 59% as compared to a SSP average of 89%. However, the ease of making second serves comes at a price; namely, second serve points are harded to win with an ATP average SSWP of just 48% as compared to an average FSWP of 68%. 

Now there are two serving strategies that are going to be analyzed here

(1) Player hits first serve and then second serve if needed 
(2) Player hits first server and then hits another first serve if needed

These strategies are identical except for the second serve that is hit. Therefore, to asses the differences in probability of winning a servus point under the two strategies we can define the following quantity, known as the 'enhancement metric':

EM = FSP*FSWP-SSP-SSWP

Conceptually, we are saying that the probability of winning a second serve is: 
(chances of making the serve) x (probability of winning point if serve is in)

For strategy (1), this quantity is FSP*FSWP, whereas for strategy (2), this quantity is SSP*SSWP, and the EM factor simply is the difference in these quantities. 

The following plot is a histogram of the EM factor for ATP players, averaged all matches that they have played that are recorded in the ATP database

![](/data_visualizations/ATP_EM.png?raw=true)





