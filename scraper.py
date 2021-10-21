from datetime import timedelta
import datetime
import csv
from NBA.nba_pull import scrape_scores as nba_scrape
from NHL.nhl_pull import scrape_scores as nhl_scrape
from NFL.nfl_pull import scrape_scores as nfl_scrape

def save_data(filepath, data):
	with open(filepath, "w") as f:
		wr = csv.writer(f)
		for row in data:
			wr.writerow(row)

def read_csv(filepath):
	with open(filepath) as csvfile:
		return list(csv.reader(csvfile))

def scrape_season_by_day(scraper, start, end, save_name, all_data, ignore_dates):
	#repeatedly scrape scores for a every day in the defined date range
	#used for NHL and NBA scraping
	new_data = []
	i = start
	while i <= end:
		while i in ignore_dates: i += timedelta(days = 1)
		print(i)
		new_data.extend(scraper(i))
		i += timedelta(days = 1)
	print(len(new_data), "games recorded")
	all_data.extend(new_data)
	save_data(save_name, all_data)
	return all_data

def scrape_season_by_week(scraper, year, save_name, all_data):
	#repeatedly scrape scores for every week in the NFL season (only used for NFL)
	season_data = []
	for stype in ['2', '3']:
		for week in [str(i) for i in range(1, 18)]:
			if stype == '3' and week == '4': continue
			if stype == '3' and week > '5': break
			season_data.extend(scraper(week, year, stype))
	print(len(season_data), "games recorded")
	all_data.extend(season_data)
	save_data(save_name, all_data)
	return all_data

def main(league, scraper):
	#assumes starting from scratch - need to modify if some data already exists
	#an iterative, season-by-season approach prevents trying to scrape days in the off-season and saves data more frequently in case errors arise
	with open(league + '/season_facts.csv') as csvfile:
		facts_list = list(csv.reader(csvfile))[1:]
	all_data, ignore = [], []
	start_year = facts_list[0][0]
	if league == 'NFL':
		for row in facts_list:
			save_name = league + '/' + league + '_' + start_year + '-' + str(row[0]) + '_season.csv'
			scrape_season_by_week(scraper, row[0], save_name, all_data)
			all_data = read_csv(save_name)
	else:
		for row in facts_list:
			save_name = league + '/' + league + '_' + start_year + '-' + str(row[0]) + '_season.csv'
			start_date = datetime.datetime.strptime(row[1], "%Y%m%d")
			end_date = datetime.datetime.strptime(row[3], "%Y%m%d")
			if league == 'NHL':
				ignore = [datetime.datetime.strptime(row[4], "%Y%m%d")] if row[4] != '' else []
			scrape_season_by_day(scraper, start_date, end_date, save_name, all_data, ignore)
			all_data = read_csv(save_name)

if __name__ == '__main__':
	# main('NBA', nba_scrape)
	# main('NHL', nhl_scrape)
	# main('NFL', nfl_scrape)
	pass