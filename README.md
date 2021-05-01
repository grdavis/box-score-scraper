# box-score-scraper
Finding high-quality, clean, interesting data that is publicly available can be a big challenge. Sometimes, it is easier to just scrape and clean the data yourself. I was interested in exploring the box scores from professional sporting events in the NBA, NHL, and NFL. I scraped NHL and NFL data from [ESPN](https://www.espn.com/) and NBA data from [Basketball Reference](https://www.basketball-reference.com/) for games occuring in the last 10 years. I then cleaned and added some extra metadata to hopefully make these datasets interesting to explore, but I also kept them relatively simple.

## Workflow
There are effectively two steps in the process: scraping and cleaning. `scraper.py` implements the ability to scrape box score data for the NFL, NHL, or NBA in any range of time. For this project, the range was only 10 years, but the script could be used to go further back. `cleaner.py` can then be used on the raw, scraped data to create the final deliverable. The cleaning stage standardizes the box scores, and calculates scoring margins for each quarter/period and point totals. The cleaning also adds extra data:
* Flag for overtime game
* Flag for playoffs
* Estimate of distance traveled by Away team for the game (in miles). Source: [USCA312](https://people.sc.fsu.edu/~jburkardt/datasets/cities/cities.html)
* Intraconference/division matchup flag (NFL only)
* Away/Home team off a "bye-week" flag (NFL only)
* Week of the season (NFL only)
* Day of the week (NHL and NBA only)

## Cleaned Data Contents
This repository contains the following:
* `NHL/nhl_cleaned.csv`: box scores for every NHL game between 10/7/2010 and 9/28/2020 (10 complete seasons, 12563 games)
* `NBA/nba_cleaned.csv`: box scores for every NBA game between 10/26/2010 and 10/11/2020 (10 complete seasons, 12721 games)
* `NFL/nfl_cleaned.csv`: box scores for every NFL game between 9/9/2010 and 2/7/2021 (11 complete seasons, 2939 games)

## Data Fields
All files have similar fields. A brief description of each of the fields is provided below:
| Field | Description |
| --- | --- |
| Away | Away team according to box score |
| AQ1 or AP1 | Away team points scored in first quarter (or period for NHL) |
| AQ2 or AP2 | Away team points scored in second quarter (or period for NHL) |
| AQ3 or AP3 | Away team points scored in third quarter (or period for NHL) |
| AQ4 | Away team points scored in fourth quarter (NBA/NFL only) |
| AOT1 | Away team points scored in first OT (all OT points for NHL and NFL) |
| AOT2 | Away team points scored in second OT (NBA only) |
| AOT3 | Away team points scored in second OT (NBA only) |
| AOT4 | Away team points scored in second OT (NBA only) |
| Away_Final | Final total points score by Away team |
| Home | Home team according to box score |
| HQ1 or HP1 | Home team points scored in first quarter (or period for NHL) |
| HQ2 or HP2 | Home team points scored in second quarter (or period for NHL) |
| HQ3 or HP3 | Home team points scored in third quarter (or period for NHL) |
| HQ4 | Home team points scored in fourth quarter (NBA/NFL only) |
| HOT1 | Home team points scored in first OT (all OT points for NHL and NFL) |
| HOT2 | Home team points scored in second OT (NBA only) |
| HOT3 | Home team points scored in second OT (NBA only) |
| HOT4 | Home team points scored in second OT (NBA only) |
| Home_Final | Final total points score by Home team |
| Date | Specific date of game (NHL and NBA) or season and week (NFL) |
| Q1M or P1M | Eventual winner is up by this many points after first quarter (or period for NHL) |
| Q2M or P2M | Eventual winner is up by this many points after second quarter (or period for NHL) |
| Q3M or P3M | Eventual winner is up by this many points after third quarter (or period for NHL) |
| FinalMargin | Winner won by this many points |
| HomeMargin | Home team won (or lost if negative) by this many points |
| FinalTotal | Total points scored in the game |
| Season | Year of season start |
| Week | Week of the season (NFL only) |
| OTs/OT_Flag | Number of overtimes in game (NBA only) or flag for game went to OT (NHL only) |
| Weekday | Day of the week for game (NHL/NBA only). 0 = Sunday, 6 = Saturday |
| TravelDist | Estimated distance traveled by Away team for the game |
| Playoffs | Flag indicating if game is a playoff game |
| Intraconference | Flag for opponents in the same conference (NFL only) |
| Intradivision | Flag for opponents in the same division (NFL only) |
| AwayBye | Flag indicating Away team is coming off a bye week (NFL only) |
| HomeBye | Flag indicating Home team is coming off a bye week (NFL only) |
