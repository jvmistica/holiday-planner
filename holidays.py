import requests
from bs4 import BeautifulSoup
from datetime import datetime


# Retrieve all menu items
url = "https://publicholidays.com.my/2020-dates/"
response = requests.get(url)
soup = BeautifulSoup(response.text, "lxml")
rows = soup.find("tbody").find_all("tr", {"class": ["odd", "even"]})

for row in rows:
    cols = row.find_all("td")
    print(cols[1].text, "-", datetime.strptime(cols[0].text + " 2020", "%d %b %Y"))

