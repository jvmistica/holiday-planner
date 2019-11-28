import os
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime, date, timedelta


def scrape_holidays(url, area):
    filename = f"data/{area}.json"
    if area not in os.listdir("data"):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "lxml")
        rows = soup.find("tbody").find_all("tr", {"class": ["odd", "even"]})
        content = dict()
        
        for row in rows:
            cols = row.find_all("td")
            holidate = datetime.strptime(cols[0].text + " 2020", "%d %b %Y").strftime("%Y-%m-%d %A")
            if holidate not in content:
                events = []
            if len(cols) > 3:
                events.append({"event": cols[2].text, "scope": cols[3].text})
                content.update({holidate: events})
            else:
                events.append({"event": cols[2].text})
                content.update({holidate: events})
        
        with open(filename, "w") as json_file:
            json.dump({area: content}, json_file)


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


def get_long_weekends(weekends, holidays):
    holidays.extend(weekends)
    holidays = sorted(list(set(holidays)))
    days = 0
    ranges = []

    # Check for long holidays/weekends greater than or equal to three days
    for day in holidays:
        days += 1
        if days == 1:
            from_date = day
        next_day = (datetime.strptime(day, "%Y-%m-%d") + timedelta(days=1)).date()
        if str(next_day) not in holidays:
            to_date = next_day - timedelta(days=1)
            if days >= 3:
                ranges.append((str(from_date.replace(" 00:00:00", "")), str(to_date).replace(" 00:00:00", "")))
            days = 0
    return ranges


def get_potential_VL(weekends, holidays):
    holidays.extend(weekends)
    holidays = sorted(list(set(holidays)))
    days = 0
    ranges = []

    # Check for long holidays/weekends greater than or equal to three days
    for day in holidays:
        days += 1
        if days == 1:
            from_date = day
        next_day = (datetime.strptime(day, "%Y-%m-%d") + timedelta(days=1)).date()
        if str(next_day) not in holidays:
            to_date = next_day - timedelta(days=1)
            ranges.append((str(from_date.replace(" 00:00:00", "")), str(to_date).replace(" 00:00:00", "")))
            days = 0
    return ranges


weekends = get_weekends()
holidays = get_holidays("malaysia")
holidays.extend(weekends)
holidays = sorted(list(set(holidays)))

pairs = get_potential_VL(weekends, holidays)
a = 0

for from_date1, to_date1 in pairs:
    a += 1
    b = 0
    for from_date2, to_date2 in pairs:
        b += 1
        if b - a == 1:
            difference = (datetime.strptime(from_date2, "%Y-%m-%d") - datetime.strptime(to_date1, "%Y-%m-%d")).days
            if difference <= 3: # the lesser, the better
                total = (datetime.strptime(to_date1, "%Y-%m-%d") - datetime.strptime(from_date1, "%Y-%m-%d")).days
                total += (datetime.strptime(to_date2, "%Y-%m-%d") - datetime.strptime(from_date2, "%Y-%m-%d")).days
                total += difference
                print("HOLIDAY 1:", from_date1, to_date1)
                print("HOLIDAY 2:", from_date2, to_date2)
                print("BETWEEN:", difference, "VL(s) needed. Total of", total, "vacation days.")

# Compute value by how many total vacation days can be achieved in how little VL needed to be filed.








