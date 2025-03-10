from webbrowser import open as open_in_browser
from json import load as load_json
import time
import re

itemFormat = dict[str, str | int]
dayScheduleFormat = list[itemFormat]
fullScheduleFormat = dict[str, dayScheduleFormat]

TIME_FORMAT = "%H:%M"
FIELD_START_DATE = "start_date"
FIELD_UNTIL = "until"
FIELD_NAME = "name"
FIELD_URL = "url"
FIELD_WEEK = "week"


def load_file() -> tuple[int, fullScheduleFormat]:
    """
    Returns deserialized JSON with schedule
    """
    with open("schedule.json", 'r', encoding="UTF-8") as fin:
        file_data: dict[str, int | fullScheduleFormat] = load_json(fin)

    if FIELD_START_DATE in file_data.keys():
        start_date: int = file_data[FIELD_START_DATE]
    else:
        start_date = 0
    schedule: fullScheduleFormat = file_data["schedule"]

    return start_date, schedule


def get_today_day_of_week() -> str:
    """
    Returns the number of today's day of the week in str
    """
    return str(time.localtime().tm_wday)


def get_today_week_number(start_date: int) -> int:
    """
    Returns the number of today's week
    """
    days_in_week = 7
    weeks_in_cycle = 2
    days_since_start = time.localtime().tm_yday - start_date
    day_in_cycle = days_since_start % (days_in_week * weeks_in_cycle)
    return day_in_cycle // days_in_week


def check_day_existence(schedule: fullScheduleFormat, day_of_week: str):
    """
    Stops execution if the today's day of week does not exist it the schedule
    """
    if day_of_week not in schedule.keys():
        print("There is no schedule for today")
        exit(0)


def parse_time(schedule: dayScheduleFormat):
    """
    Converts human time into time.struct_time for easy sorting
    """
    for el in schedule:
        el[FIELD_UNTIL] = time.strptime(el[FIELD_UNTIL], TIME_FORMAT)


def sort_by_time(schedule: dayScheduleFormat):
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


def get_current_time() -> time.struct_time:
    """
    Returns current time, ignoring the current day and year
    """
    return time.strptime(time.strftime(TIME_FORMAT, time.localtime()), TIME_FORMAT)


def exit_if_none(obj, reason: str):
    """
    Checks if the obj is None, prints reason and stops execution
    """
    if obj is None:
        print(reason)
        exit(0)


def find_nearest_item(
        schedule: dayScheduleFormat,
        target_time: time.struct_time,
        week_number: int) -> itemFormat:
    """
    Returns the nearest item to the given time
    """
    result = None

    for el in schedule:
        if FIELD_WEEK in el.keys() and el[FIELD_WEEK] != week_number:
            continue
        if target_time < el[FIELD_UNTIL]:
            result = el

    exit_if_none(result, "No scheduled items left for today.")
    return result


def parse_zoom_url(url: str) -> tuple | None:
    """
    If the given url is used to connect to a zoom meeting
    then returns the meeting's id and password.
    Else, returns None, None
    """
    match = re.fullmatch(r"https://.*\.?zoom\.us/j/(\d+)(?:\?pwd=(.+))?", url)

    if match is None:
        return None, None

    return match.group(1), match.group(2)


def rewrite_zoom_url(item: itemFormat) -> itemFormat:
    """
    Rewrites zoom url to zoomus:// format to open the Zoom meeting directly
    Doesn't touch url if it leads to another service
    """
    zoom_id, zoom_password = parse_zoom_url(item[FIELD_URL])
    if zoom_id is None:
        return item
    
    item[FIELD_URL] = f"zoomus://join?action=join&confno={zoom_id}"
    if zoom_password is not None:
        item[FIELD_URL] += f"&pwd={zoom_password}"
    return item


def main():
    start_date, schedule = load_file()
    day_of_week = get_today_day_of_week()
    week_number = get_today_week_number(start_date)
    check_day_existence(schedule, day_of_week)
    today_schedule = schedule[day_of_week]

    parse_time(today_schedule)
    sort_by_time(today_schedule)

    nearest_item = find_nearest_item(today_schedule, get_current_time(), week_number)
    nearest_item = rewrite_zoom_url(nearest_item)
    print(nearest_item[FIELD_NAME])
    open_in_browser(nearest_item[FIELD_URL])


if __name__ == '__main__':
    main()