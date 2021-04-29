NORMAL_COLS = 13
MAX_OTS = 1
COL_BASE = ['Away', 'AQ1', 'AQ2', 'AQ3', 'AQ4'] + ['AOT%s' % str(i) for i in range(1, MAX_OTS + 1)] + ['Away_Final', 'Home', 'HQ1', 'HQ2', 'HQ3', 'HQ4'] + ['HOT%s' % str(i) for i in range(1, MAX_OTS + 1)] + ['Home_Final', 'Date']

def extend_rows(data):
	#those with overtimes have more columns - make every game have a uniform number
	new_data = []
	for row in data:
		row_ots = (len(row) - NORMAL_COLS)//2
		row = [int(i) if len(i) < 3 else i for i in row]
		new_data.append(row[:(5 + row_ots)] + [0] * (MAX_OTS - row_ots) + [row[5+row_ots]] + row[(6 + row_ots):-2] + [0] * (MAX_OTS - row_ots) + row[-2:])
	return new_data

def add_cumulatives(df):
	#add columns calculating the scoring margin for the eventual winning team at the end of each period
	#also add final combined total score and difference between home score and away score
	additions = {'Q1M': [], 'Q2M': [], 'Q3M': [], 'FinalMargin': [], 'FinalTotal': [], 'HomeMargin': []}
	for index, row in df.iterrows():
		if row['Home_Final'] > row['Away_Final']:
			additions['Q1M'].append(row['HQ1'] - row['AQ1'])
			additions['Q2M'].append(row['HQ1'] + row['HQ2'] - row['AQ1'] - row['AQ2'])
			additions['Q3M'].append(row['HQ1'] + row['HQ2'] + row['HQ3'] - row['AQ1'] - row['AQ2'] - row['AQ3'])
			additions['FinalMargin'].append(row['Home_Final'] - row['Away_Final'])
		else:
			additions['Q1M'].append(row['AQ1'] - row['HQ1'])
			additions['Q2M'].append(row['AQ1'] + row['AQ2'] - row['HQ1'] - row['HQ2'])
			additions['Q3M'].append(row['AQ1'] + row['AQ2'] + row['AQ3'] - row['HQ1'] - row['HQ2'] - row['HQ3'])
			additions['FinalMargin'].append(row['Away_Final'] - row['Home_Final'])
		additions['FinalTotal'].append(row['Home_Final'] + row['Away_Final'])
		additions['HomeMargin'].append(row['Home_Final'] - row['Away_Final'])
	df['Q1M'] = additions['Q1M']
	df['Q2M'] = additions['Q2M']
	df['Q3M'] = additions['Q3M']
	df['FinalMargin'] = additions['FinalMargin']
	df['FinalTotal'] = additions['FinalTotal']
	df['HomeMargin'] = additions['HomeMargin']
	return df

def final_clean(df):
	#team name change
	df = df.replace("Redskins", "Washington")
	return df

def add_metadata(df, team_facts, dist_matrix, seasons_list, start_season_list, playoff_start_list):
	#add columns for season, week, playoffs flag, away team off a bye, home team off a bye,
	#intraconference flag, intradivision flag, and away team travel distance
	class Team:
		def __init__(self, city, conference, division):
			self.city = city
			self.conference = conference
			self.division = division	

	team_facts_classes = {} #(team, year) -> Team object
	for t in team_facts:
		res = team_facts[t]
		team_facts_classes[t] = Team(res[0], res[1], res[2])

	df = final_clean(df).sort_values(by = ['Date'])
	last_game_tracker = {} # map 'team': 'Week' of last game
	season, week, playoffs, home_off_bye, away_off_bye, conference, division, travel_dist = [], [], [], [], [], [], [], []
	for index, row in df.iterrows():
		date = row['Date']
		date_int = int(date)
		season.append(int(date[:4]))
		this_week = int(date[-2:])
		if this_week > 17:
			playoffs.append(1)
		else:
			playoffs.append(0)
		week.append(this_week)

		if date_int - last_game_tracker.get(row['Home'], 0) == 2:
			home_off_bye.append(1)
		else:
			home_off_bye.append(0)
		if date_int - last_game_tracker.get(row['Away'], 0) == 2:
			away_off_bye.append(1)
		else:
			away_off_bye.append(0)
		last_game_tracker[row['Home']], last_game_tracker[row['Away']] = date_int, date_int

		homeTeam = team_facts_classes[(row['Home'], season[-1])]
		awayTeam = team_facts_classes[(row['Away'], season[-1])]
		travel_dist.append(int(dist_matrix[(homeTeam.city, awayTeam.city)]))
		conference.append(1 if homeTeam.conference == awayTeam.conference else 0)
		division.append(1 if homeTeam.division == awayTeam.division else 0)
	
	df['Season'] = season
	df['Week'] = week
	df['Playoffs'] = playoffs
	df['AwayBye'] = away_off_bye
	df['HomeBye'] = home_off_bye
	df['Intraconference'] = conference
	df['Intradividion'] = division
	df['TravelDist'] = travel_dist
	return df




