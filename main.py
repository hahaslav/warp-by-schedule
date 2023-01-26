from webbrowser import open as open_in_browser
from json import load as load_json
import time

TIME_FORMAT = "%H:%M"
FIELD_UNTIL = "until"
FIELD_NAME = "name"
FIELD_URL = "url"
FIELD_WEEK = "week"


def load_file():
    """
    Returns deserialized JSON with schedule
    """
    with open("schedule.json", 'r', encoding="UTF-8") as fin:
        file_data = load_json(fin)

    return file_data["start_date"], file_data["schedule"]


def get_today_day_of_week():
    """
    Returns the number of today's day of the week in str
    """
    return str(time.localtime().tm_wday)


def get_today_week_number(start_date):
    """
    Returns the number of today's week
    """
    days_in_week = 7
    weeks_in_cycle = 2
    days_since_start = time.localtime().tm_yday - start_date
    day_in_cycle = days_since_start % (days_in_week * weeks_in_cycle)
    return day_in_cycle // days_in_week


def parse_time(schedule):
    """
    Converts human time into time.struct_time for easy sorting
    """
    for el in schedule:
        el[FIELD_UNTIL] = time.strptime(el[FIELD_UNTIL], TIME_FORMAT)


def sort_by_time(schedule):
    """
    Sorts the items in the schedule so the later items will be first
    """
    changed = True

    while changed:
        changed = False
        for i in range(len(schedule) - 1):
            if schedule[i][FIELD_UNTIL] < schedule[i + 1][FIELD_UNTIL]:
                schedule[i], schedule[i + 1] = schedule[i + 1], schedule[i]
                changed = True


def get_current_time():
    """
    Returns current time, ignoring the current day and year
    """
    return time.strptime(time.strftime(TIME_FORMAT, time.localtime()), TIME_FORMAT)


def find_nearest_item(schedule, target_time: time.struct_time, week_number):
    """
    Returns the nearest item to the given time
    """
    result = None

    for el in schedule:
        if FIELD_WEEK in el.keys() and el[FIELD_WEEK] != week_number:
            continue
        if target_time < el[FIELD_UNTIL]:
            result = el

    return result


def exit_if_none(obj, reason):
    """
    Checks if the obj is None, prints reason and stops execution
    """
    if obj is None:
        print(reason)
        exit(0)


def main():
    start_date, schedule = load_file()
    day_of_week = get_today_day_of_week()
    week_number = get_today_week_number(start_date)
    today_schedule = schedule[day_of_week]

    parse_time(today_schedule)
    sort_by_time(today_schedule)

    nearest_item = find_nearest_item(today_schedule, get_current_time(), week_number)
    exit_if_none(nearest_item, "No scheduled items left for today.")
    print(nearest_item[FIELD_NAME])
    open_in_browser(nearest_item[FIELD_URL])


if __name__ == '__main__':
    main()