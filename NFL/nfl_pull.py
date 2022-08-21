from bs4 import BeautifulSoup
import requests
import re
import json

URL = 'https://www.espn.com/nfl/scoreboard/_/year/YEAR/seasontype/TYPE/week/WEEK'

def nfl_fix_dates_for_data(week, year, stype):
	#form dates into YYYYWW, e.g. 201001 for 2010 week 1
	weeks_in_season = 17 if int(year) < 2021 else 18
	new_week = week if stype == '2' else str(int(week) + weeks_in_season)
	new_week = new_week if len(new_week) == 2 else "0" + new_week
	return year + new_week 

def scrape_scores(week, year, stype):
	#scrape the scores from a single week
	print(nfl_fix_dates_for_data(week, year, stype))
	day_stats = []
	url = URL.replace("WEEK", week).replace("YEAR", year).replace("TYPE", stype)
	data = requests.get(url).content
	souped = BeautifulSoup(data,'html.parser')

	times = [i.text for i in souped.find_all('div', {'class': 'ScoreboardScoreCell__Overview'})]
	team_names = [i.text for i in souped.find_all('div', {'class': 'ScoreCell__TeamName'})]
	final_scores = [i.text for i in souped.find_all('div', {'class': 'ScoreCell__Score'})]

	linescores = []
	linescores_souped = souped.find_all('div', {'class': 'ScoreboardScoreCell_Linescores'})
	for linescore in linescores_souped:
		scores = linescore.find_all('div', {'class': 'ScoreboardScoreCell__Value'})
		linescores.append([s.text for s in scores])

	#if a game got postponed, the team names will show up, but there will be no box scores
	cleaned_team_names = []
	for i in range(len(team_names)):
		if times[i//2] == '': continue
		cleaned_team_names.append(team_names[i])
	
	stats = []
	away = True
	for i in range(len(cleaned_team_names)):
		stats.append(cleaned_team_names[i])
		stats.extend(linescores[i])
		stats.append(final_scores[i])
		if not away:
			stats.append(nfl_fix_dates_for_data(week, year, stype))
			day_stats.append(stats)
			stats = []
		away = not away

	return day_stats