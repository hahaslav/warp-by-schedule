import json
import time


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


def main():
    start_date, schedule = load_file()
    day_of_week = get_today_day_of_week()


if __name__ == '__main__':
    main()