import pandas as pd
import csv
import NHL.nhl_scores_transform as nhl
import NBA.nba_scores_transform as nba
import NFL.nfl_scores_transform as nfl

def read_csv(filepath):
	with open(filepath) as csvfile:
		return list(csv.reader(csvfile))

def prep_facts(league):
	#create mapping (team, year) -> City
	team_facts = {} 
	with open(league + '/team_facts.csv') as csvfile:
		facts_list = list(csv.reader(csvfile))[1:]
	for line in facts_list:
		for year in range(int(line[-2]), int(line[-1]) + 1):
			team_facts[(line[0], year)] = tuple(line[1:-2])
	return team_facts

def prep_dists():
	#create a mapping of (origin_city, destination_city) -> distance
	with open('Helpers/dist_cities.txt', "r") as txtfile:
		cities = txtfile.read().split('\n')

	with open('Helpers/dist.txt', "r") as txtfile:
		dists = txtfile.read().split(" ")

	clean_dists = []
	for d in dists:
		if d == '': continue
		clean_dists.append(d.strip())

	dist_matrix = {}
	i = 0
	for o in cities:
		for d in cities:
			dist_matrix[(o, d)] = clean_dists[i]
			i += 1
	return dist_matrix

def prep_season_facts(league):
	#create lists for season, starting date, and playoff starting date
	seasons_list, start_season_list, playoff_start_list = [], [], []
	with open(league + '/season_facts.csv') as csvfile:
		facts_list = list(csv.reader(csvfile))[1:]
	for row in facts_list:
		seasons_list.append(row[0][:4]) #make sure 2019.1 and 2019.2 still count as just 2019
		start_season_list.append(row[1])
		playoff_start_list.append(row[2])
	return seasons_list, start_season_list, playoff_start_list

def main(filepath, league_text, this_league):
	dirty_data = read_csv(filepath)
	extended = this_league.extend_rows(dirty_data)
	df = pd.DataFrame(extended, columns = this_league.COL_BASE)
	df = this_league.add_cumulatives(df)
	team_facts = prep_facts(league_text)
	dist_matrix = prep_dists()
	seasons_list, start_season_list, playoff_start_list = prep_season_facts(league_text)
	df = this_league.add_metadata(df, team_facts, dist_matrix, seasons_list, start_season_list, playoff_start_list)
	df.to_csv(league_text + '/' + league_text + '_cleaned.csv', index = False)

if __name__ == '__main__':
	# main("NHL/NHL_2010-2019.2_season.csv", "NHL", nhl)
	# main("NBA/NBA_2010-2019.2_season.csv", "NBA", nba)
	# main("NFL/NFL_2010-2020_season.csv", "NFL", nfl)
	pass