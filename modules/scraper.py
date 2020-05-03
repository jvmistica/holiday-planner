import json
import os
from datetime import datetime, date, timedelta
from bs4 import BeautifulSoup
import requests


def scrape_holidays(url, area):
    """
    Scrapes a website for the holiday dates for a given country or state.
    Writes the scraped information to a JSON file in the data folder.

    :param url: The website listing the holiday dates.
    :param area: The country or state where the holidays occur.
    :returns: None
    """

    filename = f"data/{area}.json"
    if area not in os.listdir("data"):
        response = requests.get(url.replace("<area_name>", area))
        print(url.replace("<area_name>", area))
        soup = BeautifulSoup(response.text, "lxml")
        rows = soup.find("tbody").find_all("tr")
        content = {}

        for row in rows:
            cols = row.find_all("td")
            holidate = datetime.strptime(row.find("time").get("datetime"), "%Y-%m-%d")\
                    .strftime("%Y-%m-%d %A")
            if holidate not in content:
                events = []
            events.append({"event": cols[2].text})
            content.update({holidate: events})

        with open(filename, "w") as json_file:
            json.dump({area: content}, json_file)


def get_weekends(year=2020):
    """
    Checks which dates the weekends fall for a given year.

    :param year:
    :returns: The dates where Saturday and Sunday fall.
    """

    days_in_year = (date(year, 12, 31) - date(year, 1, 1)).days
    weekends = list()
    for day in range(days_in_year + 1):
        weekend = date(year, 1, 1) + timedelta(days=day)
        weekend = weekend.strftime("%Y-%m-%d %A").split()
        if weekend[-1] in ["Saturday", "Sunday"]:
            weekends.append(datetime.strptime(weekend[0], "%Y-%m-%d").date())
    return weekends


def get_holidays(area):
    """
    Looks for holiday dates from the JSON file for the specified area.

    :param area: The country or area to look for.
    :returns: The holiday dates for the specified area.
    """

    filename = f"data/{area}.json"
    holidays = list()
    with open(filename, "r") as json_file:
        for holiday in json.load(json_file).get(area):
            holiday = datetime.strptime(holiday, "%Y-%m-%d %A").strftime("%Y-%m-%d")
            holidays.append(datetime.strptime(holiday, "%Y-%m-%d").date())
    return holidays


def get_free_time(weekends, holidays):
    """
    Looks for all free time (holidays or weekends) and long weekends.

    :param weekends: The date exact dates for Saturdays and Sundays.
    :param holidays: The holiday dates.
    :returns: A list containing all free times and all long weekends.
    """

    holidays.extend(weekends)
    holidays = sorted(set(holidays))
    days = 0
    free_time = []
    long_weekends = []

    # Check for long holidays/weekends greater than or equal to three days
    for holiday in holidays:
        days += 1
        from_date = holiday if days == 1 else from_date
        if holiday + timedelta(days=1) not in holidays:
            to_date = holiday
            free_time.append((from_date, to_date))
            if days >= 3:
                long_weekends.append((from_date, to_date))
            days = 0

    return free_time, long_weekends
