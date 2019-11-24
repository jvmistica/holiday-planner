import os
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime, date, timedelta


# def scrape_holidays(url, area):
#     filename = f"data/{area}.json"
#     if area not in os.listdir("data"):
#         response = requests.get(url)
#         soup = BeautifulSoup(response.text, "lxml")
#         rows = soup.find("tbody").find_all("tr", {"class": ["odd", "even"]})
#         content = dict()
#         
#         for row in rows:
#             cols = row.find_all("td")
#             holidate = datetime.strptime(cols[0].text + " 2020", "%d %b %Y").strftime("%Y-%m-%d %A")
#             if holidate not in content:
#                 events = []
#             if len(cols) > 3:
#                 events.append({"event": cols[2].text, "scope": cols[3].text})
#                 content.update({holidate: events})
#             else:
#                 events.append({"event": cols[2].text})
#                 content.update({holidate: events})
#         
#         with open(filename, "w") as json_file:
#             json.dump({area: content}, json_file)
# 
# scrape_holidays("https://publicholidays.ph/2020-dates/", "philippines")
# """
# URLS:
#   - https://publicholidays.com.my/2020-dates/
#   - https://publicholidays.ph/2020-dates/
#   - https://publicholidays.us/ohio/2020-dates/
# """

def get_weekends():
    days_in_year = (date(2020, 12, 31) - date(2020, 1, 1)).days
    weekends = list()
    for day in range(days_in_year + 1):
        weekend = date(2020, 1, 1) + timedelta(days=day)
        weekend = weekend.strftime("%Y-%m-%d %A").split()
        if weekend[-1] in ["Saturday", "Sunday"]:
            weekends.append(weekend[0])
    return weekends


def get_holidays(area):
    filename = f"data/{area}.json"
    holidays = list()
    with open(filename, "r") as json_file:
        for holiday in json.load(json_file).get(area):
            holidays.append(datetime.strptime(holiday, "%Y-%m-%d %A").strftime("%Y-%m-%d"))
    return holidays


weekends = get_weekends()
holidays = get_holidays("malaysia")
holidays.extend(weekends)
holidays = list(set(holidays))
holidays.sort()
days = 0
from_date = 0
total = 0
dates = []

# Check for long holidays/weekends greater than or equal to three days
for day in holidays:
    days += 1
    if days == 1:
        from_date = day
    next_day = (datetime.strptime(day, "%Y-%m-%d") + timedelta(days=1)).date()
    if str(next_day) not in holidays:
        to_date = next_day - timedelta(days=1)
        if days >= 3:
            total += days
            dates.append((str(days) + " days: " + str(from_date.replace(" 00:00:00", "")) + " - " + str(to_date).replace(" 00:00:00", "")).replace("-", "/"))
        days = 0

for dt in dates:
    print(dt.replace("2020/", "").replace(" / ", " - "))
