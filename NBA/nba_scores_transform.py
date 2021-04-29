import datetime

NORMAL_COLS = 11
MAX_OTS = 4
COL_BASE = ['Away', 'AQ1', 'AQ2', 'AQ3', 'AQ4'] + ['AOT%s' % str(i) for i in range(1, MAX_OTS + 1)] + ['Home', 'HQ1', 'HQ2', 'HQ3', 'HQ4'] + ['HOT%s' % str(i) for i in range(1, MAX_OTS + 1)] + ['Date']

def extend_rows(data):
	#those with overtimes have more columns - make every game have a uniform number
	new_data = []
	for row in data:
		row = [str(i) if len(i) >= 3 or i == '' else int(i) for i in row]
		if type(row[5]) != int: #game has no overtimes
			new_data.append(row[:5] + [0]*MAX_OTS + row[5:10] + [0]*MAX_OTS + [row[NORMAL_COLS - 1]])
		elif type(row[6]) != int: #game has 1OT
			new_data.append(row[:6] + [0]*(MAX_OTS - 1) + row[6:12] + [0]*(MAX_OTS - 1) + [row[NORMAL_COLS + 1]])
		elif type(row[7]) != int: #game has 2OT
			new_data.append(row[:7] + [0]*(MAX_OTS - 2) + row[7:14] + [0]*(MAX_OTS - 2) + [row[NORMAL_COLS + 3]])
		elif type(row[8]) != int: #game has 3OT
			new_data.append(row[:8] + [0]*(MAX_OTS - 3) + row[8:16] + [0]*(MAX_OTS - 3) + [row[NORMAL_COLS + 5]])
		else: #game has 4OTs
			new_data.append(row)
	return new_data

def add_cumulatives(df):
	#add columns calculating the scoring margin for the eventual winning team at the end of each period
	#also add final combined total score and difference between home score and away score
	#final scores for both teams are not included in the scraped data, so calculate here
	home_cols = []
	away_cols = []
	for i in df.columns:
		if 'H' in i and i != "Home": home_cols.append(i)
		if 'A' in i and i != "Away": away_cols.append(i)
	df['Away_Final'] = df[away_cols].sum(axis = 1)
	df['Home_Final'] = df[home_cols].sum(axis = 1)

	additions = {'Q1M': [], 'Q2M': [], 'Q3M': [], 'Q4M': [], 'FinalMargin': [], 'FinalTotal': [], 'HomeMargin': []}
	for index, row in df.iterrows():
		if row['Home_Final'] > row['Away_Final']:
			additions['Q1M'].append(row['HQ1'] - row['AQ1'])
			additions['Q2M'].append(row['HQ1'] + row['HQ2'] - row['AQ1'] - row['AQ2'])
			additions['Q3M'].append(row['HQ1'] + row['HQ2'] + row['HQ3'] - row['AQ1'] - row['AQ2'] - row['AQ3'])
			additions['Q4M'].append(row['HQ1'] + row['HQ2'] + row['HQ3'] + row['HQ4'] - row['AQ1'] - row['AQ2'] - row['AQ3'] - row['AQ4'])
			additions['FinalMargin'].append(row['Home_Final'] - row['Away_Final'])
		else:
			additions['Q1M'].append(row['AQ1'] - row['HQ1'])
			additions['Q2M'].append(row['AQ1'] + row['AQ2'] - row['HQ1'] - row['HQ2'])
			additions['Q3M'].append(row['AQ1'] + row['AQ2'] + row['AQ3'] - row['HQ1'] - row['HQ2'] - row['HQ3'])
			additions['Q4M'].append(row['AQ1'] + row['AQ2'] + row['AQ3'] + row['AQ4'] - row['HQ1'] - row['HQ2'] - row['HQ3'] - row['HQ4'])
			additions['FinalMargin'].append(row['Away_Final'] - row['Home_Final'])
		additions['FinalTotal'].append(row['Home_Final'] + row['Away_Final'])
		additions['HomeMargin'].append(row['Home_Final'] - row['Away_Final'])
	df['Q1M'] = additions['Q1M']
	df['Q2M'] = additions['Q2M']
	df['Q3M'] = additions['Q3M']
	df['Q4M'] = additions['Q4M']
	df['FinalMargin'] = additions['FinalMargin']
	df['FinalTotal'] = additions['FinalTotal']
	df['HomeMargin'] = additions['HomeMargin']
	return df

def final_clean(df):
	#the Nets moved from 'New Jersey' to 'Brooklyn'
	df = df.replace('New Jersey', 'Brooklyn')
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
		if row['Q4M'] != 0:
			OT.append(0)
		elif row['HOT4'] + row['AOT4'] > 0:
			OT.append(4)
		elif row['HOT3'] + row['AOT3'] > 0:
			OT.append(3)
		elif row['HOT2'] + row['AOT2'] > 0:
			OT.append(2)
		else:
			OT.append(1)
		distance.append(dist_matrix[(team_facts[(row['Home'], int(seasonp[0]))][0], team_facts[(row['Away'], int(seasonp[0]))][0])])

	df['Season'] = season
	df['OTs'] = OT
	df['Weekday'] = day
	df['TravelDist'] = distance
	df['Playoffs'] = playoffs
	return final_clean(df)