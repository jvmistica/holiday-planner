import os
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime, date, timedelta
from trello import create_board, create_list, create_card


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


weekends = get_weekends()
holidays = get_holidays("malaysia")
pairs = get_free_time(weekends, holidays)[0]
suggestions = []
a = 0
for from_date1, to_date1 in pairs:
    a += 1
    b = 0
    for from_date2, to_date2 in pairs:
        b += 1
        if b - a == 1:
            leaves = (from_date2 - to_date1).days
            if leaves <= 5: # the lesser, the better
                vacation_days = (to_date1 - from_date1).days + (to_date2 - from_date2).days + leaves
                if vacation_days - leaves > 1:
                    suggestions.append((vacation_days + 1, leaves, from_date1.strftime("%m/%d"), to_date2.strftime("%m/%d")))

board_id = create_board("Holidays")
first_four = create_list(board_id, "Jan - Apr", 1)
second_four = create_list(board_id, "May - Aug", 2)
last_four = create_list(board_id, "Sep - Dec", 3)
suggestions_list = create_list(board_id, "Suggested Leaves", 4)

# Get free time that requires no VLs
long_weekends = get_free_time(weekends, holidays)[1]
for from_date, to_date in long_weekends:
    vacation_days = (to_date - from_date).days + 1
    if from_date.month <= 4:
        create_card(first_four, "{0} days: {1} - {2}".format(vacation_days, from_date.strftime("%m/%d"), to_date.strftime("%m/%d")))
    elif 5 <= from_date.month <= 8:
        create_card(second_four, "{0} days: {1} - {2}".format(vacation_days, from_date.strftime("%m/%d"), to_date.strftime("%m/%d")))
    else:
        create_card(last_four, "{0} days: {1} - {2}".format(vacation_days, from_date.strftime("%m/%d"), to_date.strftime("%m/%d")))

# Get suggestions on when to file VLs
suggestions.sort(reverse=True)
for suggestion in suggestions:
    create_card(suggestions_list, "{0} days: {2} - {3} | {1} VL".format(*suggestion))
