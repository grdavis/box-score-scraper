import datetime

NORMAL_COLS = 11 #if no OTs, we expect this many columns
MAX_OTS = 1 #there will be at most this many OT columns in the game for both teams
COL_BASE = cols = ['Away', 'AP1', 'AP2', 'AP3'] + ['AOT%s' % str(i) for i in range(1, MAX_OTS + 1)] + ['Away_Final', 'Home', 'HP1', 'HP2', 'HP3'] + ['HOT%s' % str(i) for i in range(1, MAX_OTS + 1)] + ['Home_Final', 'Date']

def extend_rows(data):
	#those with overtimes have more columns - make every game have a uniform number
	new_data = []
	for row in data:
		row = [i if len(i) >= 3 or i == '' else int(i) for i in row]
		if type(row[5]) != int: #game has no overtimes
			new_data.append(row[:4] + [0]*MAX_OTS + row[4:9] + [0]*MAX_OTS + row[9:NORMAL_COLS])
		else: #game has overtimes
			new_data.append(row)
	return new_data

def add_cumulatives(df):
	#add columns calculating the scoring margin for the eventual winning team at the end of each period
	#also add final combined total score and difference between home score and away score
	additions = {'P1M': [], 'P2M': [], 'P3M': [], 'FinalMargin': [], 'FinalTotal': [], 'HomeMargin': []}
	for index, row in df.iterrows():
		if row['Home_Final'] > row['Away_Final']:
			additions['P1M'].append(row['HP1'] - row['AP1'])
			additions['P2M'].append(row['HP1'] + row['HP2'] - row['AP1'] - row['AP2'])
			additions['P3M'].append(row['HP1'] + row['HP2'] + row['HP3'] - row['AP1'] - row['AP2'] - row['AP3'])
			additions['FinalMargin'].append(row['Home_Final'] - row['Away_Final'])
		else:
			additions['P1M'].append(row['AP1'] - row['HP1'])
			additions['P2M'].append(row['AP1'] + row['AP2'] - row['HP1'] - row['HP2'])
			additions['P3M'].append(row['AP1'] + row['AP2'] + row['AP3'] - row['HP1'] - row['HP2'] - row['HP3'])
			additions['FinalMargin'].append(row['Away_Final'] - row['Home_Final'])
		additions['FinalTotal'].append(row['Home_Final'] + row['Away_Final'])
		additions['HomeMargin'].append(row['Home_Final'] - row['Away_Final'])
	df['P1M'] = additions['P1M']
	df['P2M'] = additions['P2M']
	df['P3M'] = additions['P3M']
	df['FinalMargin'] = additions['FinalMargin']
	df['FinalTotal'] = additions['FinalTotal']
	df['HomeMargin'] = additions['HomeMargin']
	return df

def add_metadata(df, team_facts, dist_matrix, seasons_list, start_season_list, playoff_start_list):
	#add columns for weekday, season, OT flag, playoffs flag, travel distance
	#potentially add days_of_rest between games for each team?
	def check_season_and_playoffs(datestring):
		for index in range(len(start_season_list)):
			if datestring < start_season_list[index]:
				return (seasons_list[index-1], 1 if datestring >= playoff_start_list[index-1] else 0)
		return (seasons_list[len(start_season_list)-1], 1 if datestring >= playoff_start_list[len(start_season_list)-1] else 0)

	df = df.sort_values(by = ['Date'])
	day, OT, season, distance, playoffs = [], [], [], [], []
	for index, row in df.iterrows():
		seasonp = check_season_and_playoffs(row['Date'])
		season.append(seasonp[0])
		playoffs.append(seasonp[1])
		day.append(datetime.datetime.strptime(row['Date'], "%Y%m%d").weekday())
		OT.append(0 if row['P3M'] == row['FinalMargin'] else 1)
		distance.append(dist_matrix[(team_facts[(row['Home'], int(seasonp[0]))][0], team_facts[(row['Away'], int(seasonp[0]))][0])])

	df['Season'] = season
	df['OT_Flag'] = OT
	df['Weekday'] = day
	df['TravelDist'] = distance
	df['Playoffs'] = playoffs
	return df