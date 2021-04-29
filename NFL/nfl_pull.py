from bs4 import BeautifulSoup

URL = 'https://www.espn.com/nfl/scoreboard/_/year/YEAR/seasontype/TYPE/week/WEEK'

def get_chrome_data(url, driver):
	driver.get(url)
	return driver.page_source

def nfl_fix_dates_for_data(week, year, stype):
	#form dates into YYYYWW, e.g. 201001 for 2010 week 1
	new_week = week if stype == '2' else str(int(week) + 17)
	new_week = new_week if len(new_week) == 2 else "0" + new_week
	return year + new_week 

def scrape_scores(week, year, stype, driver):
	#scrape the scores from a single week
	print(nfl_fix_dates_for_data(week, year, stype))
	day_stats = []
	url = URL.replace("WEEK", week).replace("YEAR", year).replace("TYPE", stype)
	data = get_chrome_data(url, driver)
	tables = BeautifulSoup(data,'html.parser').find_all("tbody")
	for table in tables:
		rows = table.find_all('tr')
		stats = []
		for row in rows:
			stats.append(row.find("span", {"class": "sb-team-short"}).text)
			if len(row.find_all('td', {"class": "score"})) == 0: break
			stats += [int(stat.text) for stat in row.find_all('td', {"class": "score"})]
			stats.append(int(row.find('td', {"class": "total"}).text))
		if len(stats) < 12: continue
		day_stats.append(stats + [nfl_fix_dates_for_data(week, year, stype)])
	
	return day_stats