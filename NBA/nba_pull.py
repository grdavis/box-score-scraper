from bs4 import BeautifulSoup
import requests

URL = 'https://www.basketball-reference.com/boxscores/?month=MONTH&day=DAY&year=YEAR'

def fix_dates_for_data(date_obj):
	#make sure dates are in the format: 20210130
	new_month = str(date_obj.month) if len(str(date_obj.month)) == 2 else "0" + str(date_obj.month)
	new_day = str(date_obj.day) if len(str(date_obj.day)) == 2 else "0" + str(date_obj.day)
	return str(date_obj.year) + new_month + new_day 

def scrape_scores(date_obj):
	#scrape the scores from a single day
	day, month, year = str(date_obj.day), str(date_obj.month), str(date_obj.year)
	day_stats = []
	url = URL.replace("DAY", day).replace("MONTH", month).replace("YEAR", year)
	data = requests.get(url).content
	table_divs = BeautifulSoup(data,'html.parser').find_all("div", {'class': 'game_summary'})
	for div in table_divs:
		tables = div.find_all('tbody')
		rows = tables[1].find_all('tr')
		stats = []
		for row in rows:
			stats += [stat.text.strip('\xa0') for stat in row.find_all('td')]
		day_stats.append(stats + [fix_dates_for_data(date_obj)])

	return day_stats