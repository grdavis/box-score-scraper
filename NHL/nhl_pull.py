from bs4 import BeautifulSoup

URL = 'https://www.espn.com/nhl/scoreboard/_/date/DATE'

def get_chrome_data(url, driver):
	driver.get(url)
	return driver.page_source

def fix_dates_for_data(date_obj):
	#make sure dates are in the format: 20210130
	new_month = str(date_obj.month) if len(str(date_obj.month)) == 2 else "0" + str(date_obj.month)
	new_day = str(date_obj.day) if len(str(date_obj.day)) == 2 else "0" + str(date_obj.day)
	return str(date_obj.year) + new_month + new_day 

def scrape_scores(date_obj, driver):
	#scrape the scores from a single day
	day_stats = []
	url = URL.replace("DATE", fix_dates_for_data(date_obj))
	data = get_chrome_data(url, driver)
	soup = BeautifulSoup(data,'html.parser')
	tables = soup.find_all("div", {"class": "ScoreboardScoreCell"})
	for table in tables:
		if (":" in table.find('div', {"class": "ScoreCell__Time"}).text) or (table.find('div', {"class": "ScoreCell__Time"}).text == "Postponed"): continue
		rows = table.find_all('li', {"class": "ScoreboardScoreCell__Item"})
		stats = []
		for row in rows:
			stats.append(row.find("div", {"class": "ScoreCell__Truncate"}).text)
			stats += [int(stat.text) for stat in row.find_all('div', {"class": "ScoreboardScoreCell__Value"})]
			if row.find('div', {"class": "ScoreCell__Score"}) == None: break
			stats.append(int(row.find('div', {"class": "ScoreCell__Score"}).text))
		if len(stats) < 10: continue
		day_stats.append(stats + [fix_dates_for_data(date_obj)])

	return day_stats

