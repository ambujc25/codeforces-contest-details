import os
import requests
import datetime
from requests_html import HTML
import pandas as pd

url = 'https://codeforces.com/contests'
base_dir = os.path.dirname(__file__)
path = os.path.join(base_dir,'data')
os.makedirs(path,exist_ok=True)


def get_data(url):
	data = requests.get(url)
	html_text = data.text
	html_data = HTML(html=html_text)

	return html_data

def parse_html(html_data):
	table = html_data.find('table')[0]
	rows = table.find('tr')
	table_data = []

	for row in rows[1:]:
		name = row.find('td')[0].text
		date = row.find('td')[2].text.split(" ")
		
		minutes = int(date[1].split(":")[1])
		hours = int(date[1].split(":")[0])

		hours = (hours+2+(minutes+30)//60)%24
		minutes = (minutes+30)%60

		if minutes < 10:
			times = f"{hours}:0{minutes}"
		else:
			times = f"{hours}:{minutes}"
		
		table_data.append([name,date[0],times])

	return table_data

def export_csv(table_data):
	headers = ['Name','Date','Time']
	df = pd.DataFrame(table_data,columns=headers)
	filepath = os.path.join('data','contests.csv')
	df.to_csv(filepath,index=False)
	return df


df = export_csv(parse_html(get_data(url)))
print(df.head(df.shape[0]))