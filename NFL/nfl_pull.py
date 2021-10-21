from bs4 import BeautifulSoup
import requests
import re
import json

URL = 'https://www.espn.com/nfl/scoreboard/_/year/YEAR/seasontype/TYPE/week/WEEK'

def nfl_fix_dates_for_data(week, year, stype):
	#form dates into YYYYWW, e.g. 201001 for 2010 week 1
	new_week = week if stype == '2' else str(int(week) + 17)
	new_week = new_week if len(new_week) == 2 else "0" + new_week
	return year + new_week 

def scrape_scores(week, year, stype):
	#scrape the scores from a single week
	print(nfl_fix_dates_for_data(week, year, stype))
	day_stats = []
	url = URL.replace("WEEK", week).replace("YEAR", year).replace("TYPE", stype)
	data = requests.get(url).content
	expression = re.compile('window.espn.scoreboardData*')
	games = BeautifulSoup(data,'html.parser').find('script', text = expression).string
	games = games[games.find('{'):games.find(';window')]
	nestedgames = json.loads(games)
	for game in nestedgames['events']:
		stats = []
		split = 0
		if 'linescores' not in game['competitions'][0]['competitors'][0]: continue
		for team in game['competitions'][0]['competitors']:
			stats.append(team['team']['shortDisplayName'])
			stats.extend([i['value'] for i in team['linescores']])
			stats.append(int(team['score']))
			if split == 0: split = len(stats)
		stats = stats[split:] + stats[:split] + [nfl_fix_dates_for_data(week, year, stype)]
		day_stats.append(stats)
	return day_stats