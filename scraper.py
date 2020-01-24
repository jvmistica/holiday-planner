import json
import os
from datetime import datetime, date, timedelta
import requests
from bs4 import BeautifulSoup


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
            weekends.append(datetime.strptime(weekend[0], "%Y-%m-%d").date())
    return weekends


def get_holidays(area):
    filename = f"data/{area}.json"
    holidays = list()
    with open(filename, "r") as json_file:
        for holiday in json.load(json_file).get(area):
            holiday = datetime.strptime(holiday, "%Y-%m-%d %A").strftime("%Y-%m-%d")
            holidays.append(datetime.strptime(holiday, "%Y-%m-%d").date())
    return holidays


def get_free_time(weekends, holidays):
    holidays.extend(weekends)
    holidays = sorted(list(set(holidays)))
    days = 0
    free_time = []
    long_weekends = []

    # Check for long holidays/weekends greater than or equal to three days
    for day in holidays:
        days += 1
        if days == 1:
            from_date = day
        next_day = day + timedelta(days=1)
        if next_day not in holidays:
            to_date = next_day - timedelta(days=1)
            free_time.append((from_date, to_date))
            if days >= 3:
                long_weekends.append((from_date, to_date))
            days = 0
    return free_time, long_weekends
