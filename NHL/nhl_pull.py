from bs4 import BeautifulSoup
import requests
import re
import json

URL = 'https://www.espn.com/nhl/scoreboard/_/date/DATE'

def fix_dates_for_data(date_obj):
	#make sure dates are in the format: 20210130
	new_month = str(date_obj.month) if len(str(date_obj.month)) == 2 else "0" + str(date_obj.month)
	new_day = str(date_obj.day) if len(str(date_obj.day)) == 2 else "0" + str(date_obj.day)
	return str(date_obj.year) + new_month + new_day 

def scrape_scores(date_obj):
	#scrape the scores from a single day
	day_stats = []
	url = URL.replace("DATE", fix_dates_for_data(date_obj))
	data = requests.get(url).content
	expression = re.compile("evts*")
	games = BeautifulSoup(data,'html.parser').find('script', text = expression).string
	games = "{" + games[games.find('\"evts\"'):games.find(',\"crntSzn\"')] + "}"
	nestedgames = json.loads(games)
	for game in nestedgames['evts']:
		stats = []
		if 'lnescrs' not in game: continue
		home, home_score = game['competitors'][0]['shortDisplayName'], game['competitors'][0]['score']
		away, away_score = game['competitors'][1]['shortDisplayName'], game['competitors'][1]['score']
		stats.append(away)
		stats.extend(game['lnescrs']['awy'])
		stats.append(away_score)
		stats.append(home)
		stats.extend(game['lnescrs']['hme'])
		stats.append(home_score)
		day_stats.append(stats + [fix_dates_for_data(date_obj)])
	return day_stats