import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime, date, timedelta


# # next: check if json file already exists
# # Retrieve all menu items
# url = "https://publicholidays.com.my/2020-dates/"
# response = requests.get(url)
# soup = BeautifulSoup(response.text, "lxml")
# rows = soup.find("tbody").find_all("tr", {"class": ["odd", "even"]})
# events = dict()
# 
# for row in rows:
#     cols = row.find_all("td")
#     events.update({datetime.strptime(cols[0].text + " 2020", "%d %b %Y").strftime("%Y-%m-%d %A"): \
#             {"event": cols[2].text, "scope": cols[3].text}}) # next: check for multiple events in one day
# 
# with open("data/holidays.json", "w") as json_file:
#     json.dump({"malaysia": events}, json_file)


delta = date(2020, 12, 31) - date(2020, 1, 1)
weekends = list()
for day in range(delta.days + 1):
    weekend = date(2020, 1, 1) + timedelta(days=day)
    weekend = weekend.strftime("%Y-%m-%d %A").split()
    if weekend[-1] in ["Saturday", "Sunday"]:
        weekends.append(weekend[0])

holidays = list()
with open("data/holidays.json") as json_file:
    for holiday in json.load(json_file).get("malaysia"):
        holidays.append(datetime.strptime(holiday, "%Y-%m-%d %A").strftime("%Y-%m-%d"))

holidays.extend(weekends)
holidays = list(set(holidays))
holidays.sort()
days = 0
from_date = 0
# Check for long holidays/weekends greater than or equal to three days
for day in holidays:
    days += 1
    if days == 1:
        from_date = day
    add = (datetime.strptime(day, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")
    if add not in holidays:
        to_date = datetime.strptime(add, "%Y-%m-%d") - timedelta(days=1)
        print(from_date, to_date, days)
        days = 0
