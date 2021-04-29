# box-score-scraper
Finding high-quality, clean, interesting data that is publicly available can be a big challenge. Sometimes, it is easier to just scrape and clean the data yourself. I was interested in exploring the box scores from professional sporting events in the NBA, NHL, and NFL. I scraped NHL and NFL data from [ESPN](https://www.espn.com/) and NBA data from [Basketball Reference](https://www.basketball-reference.com/) for games occuring in the last 10 years. I then cleaned and added some extra metadata to hopefully make these datasets interesting to explore, but I also kept them relatively simple.

## Cleaned Data Contents
If looking for just the cleaned, final data, this repository contains the following:
* `NHL/nhl_cleaned.csv`: box scores for every NHL game between 10/7/2010 and 9/28/2020 (10 complete seasons)
* `NBA/nba_cleaned.csv`: box scores for every NBA game between 10/26/2010 and 10/11/2020 (10 complete seasons)
* `NFL/nfl_cleaned.csv`: box scores for every NFL game between 9/9/2010 and 2/7/2021 (11 complete seasons)

All files have similar fields. A brief description of each of the fields is provided below:
| Field | Description |
| --- | --- |
| Away | Away team according to box score |
| AQ1 or AP1 | Away team points scored in first quarter (or period for NHL) |
| AQ2 or AP2 | Away team points scored in second quarter (or period for NHL) |
| AQ3 or AP3 | Away team points scored in third quarter (or period for NHL) |
| AQ4 | Away team points scored in fourth quarter (NBA/NFL only) |
| AOT1 | Away team points scored in first OT (all OT points for NHL and NFL)* |
| AOT2 | Away team points scored in second OT (NBA only) |
| AOT3 | Away team points scored in second OT (NBA only) |
| AOT4 | Away team points scored in second OT (NBA only) |
| Away_Final | Final total points score by Away team |
| Home | Home team according to box score |
| HQ1 or HP1 | Home team points scored in first quarter (or period for NHL) |
| HQ2 or HP2 | Home team points scored in second quarter (or period for NHL) |
| HQ3 or HP3 | Home team points scored in third quarter (or period for NHL) |
| HQ4 | Home team points scored in fourth quarter (NBA/NFL only) |
| HOT1 | Home team points scored in first OT (all OT points for NHL and NFL)* |
| HOT2 | Home team points scored in second OT (NBA only) |
| HOT3 | Home team points scored in second OT (NBA only) |
| HOT4 | Home team points scored in second OT (NBA only) |
| Home_Final | Final total points score by Home team |


* note about OTs
