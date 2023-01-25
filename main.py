import json
import time

FIELD_UNTIL = "until"


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
    return str(time.localtime()[6])


def parse_time(schedule):
    """
    Converts human time into time.struct_time for easy sorting
    """
    for el in schedule:
        el[FIELD_UNTIL] = time.strptime(el[FIELD_UNTIL], "%H:%M")


def main():
    start_date, schedule = load_file()
    day_of_week = get_today_day_of_week()
    today_schedule = schedule[day_of_week]
    parse_time(today_schedule)


if __name__ == '__main__':
    main()