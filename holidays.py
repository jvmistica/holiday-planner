from scraper import get_weekends, get_holidays, get_free_time
from trello import create_board, create_list, create_card


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
                    suggestions.append((vacation_days + 1, leaves, from_date1.strftime("%m/%d"), \
                                        to_date2.strftime("%m/%d")))

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
        create_card(first_four, "{0} days: {1} - {2}".format(vacation_days, \
                    from_date.strftime("%m/%d"), to_date.strftime("%m/%d")))
    elif 5 <= from_date.month <= 8:
        create_card(second_four, "{0} days: {1} - {2}".format(vacation_days, \
                    from_date.strftime("%m/%d"), to_date.strftime("%m/%d")))
    else:
        create_card(last_four, "{0} days: {1} - {2}".format(vacation_days, \
                    from_date.strftime("%m/%d"), to_date.strftime("%m/%d")))

# Get suggestions on when to file VLs
suggestions.sort(reverse=True)
for suggestion in suggestions:
    create_card(suggestions_list, "{0} days: {2} - {3} | {1} VL".format(*suggestion))
