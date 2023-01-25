import json
import time

TIME_FORMAT = "%H:%M"
FIELD_UNTIL = "until"
FIELD_NAME = "name"
FIELD_URL = "url"


def load_file():
    """
    Returns deserialized JSON with schedule
    """
    with open("schedule.json", 'r', encoding="UTF-8") as fin:
        file_data = json.load(fin)

    return file_data["start_date"], file_data["schedule"]


def get_today_day_of_week():
    """
    Returns the number of today's day of the week in str
    """
    return str(time.localtime().tm_wday)


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


def find_nearest_item(schedule, target_time: time.struct_time):
    """
    Returns the nearest item to the given time
    """
    result = None

    for el in schedule:
        if target_time < el[FIELD_UNTIL]:
            result = el

    return result


def main():
    start_date, schedule = load_file()
    day_of_week = get_today_day_of_week()
    today_schedule = schedule[day_of_week]
    parse_time(today_schedule)
    sort_by_time(today_schedule)

    nearest_item = find_nearest_item(today_schedule, get_current_time())
    print(nearest_item[FIELD_NAME])


if __name__ == '__main__':
    main()