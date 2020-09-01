from modules.scraper import get_weekends, get_holidays, get_free_time, scrape_holidays
from modules.trello import create_board, create_list, create_card


# Retrieve all suggested vacation days
url = "https://www.officeholidays.com/countries/<area_name>/2020"
area = "malaysia"
weekends = get_weekends()
scrape_holidays(url, area)
holidays = get_holidays(area)
pairs, long_weekends = get_free_time(weekends, holidays)
suggestions = []

for ndx, pair in enumerate(pairs):
    from_date, to_date = pair
    try:
        leaves = (pairs[ndx + 1][0] - to_date).days
        if leaves <= 5:
            vacation_days = (to_date - from_date).days + (pairs[ndx + 1][1] - pairs[ndx + 1][0]).days + leaves
            if vacation_days - leaves > 1:
                suggestions.append((vacation_days + 1, leaves, from_date.strftime("%m/%d"), \
                                    pairs[ndx + 1][1].strftime("%m/%d")))
    except IndexError:
        pass

# Spread the vacation days across different Trello boards
board_id = create_board("Holidays")
first_four = create_list(board_id, "Jan - Apr", 1)
second_four = create_list(board_id, "May - Aug", 2)
third_four = create_list(board_id, "Sep - Dec", 3)
suggestions_list = create_list(board_id, "Suggested Leaves", 4)

# Get suggestions on when to file vacation leaves
suggestions.sort(reverse=True)
for suggestion in suggestions:
    create_card(suggestions_list, "{0} days: {2} - {3} | {1} VL".format(*suggestion))

# Get free time that requires no filing of vacation leaves
for from_date, to_date in long_weekends:
    vacation_days = (to_date - from_date).days + 1
    start = from_date.strftime("%m/%d")
    end = to_date.strftime("%m/%d")
    content = f"{vacation_days} days: {start} - {end}"

    if from_date.month <= 4:
        create_card(first_four, content)
    elif 5 <= from_date.month <= 8:
        create_card(second_four, content)
    else:
        create_card(third_four, content)
