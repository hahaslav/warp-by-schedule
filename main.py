import json


def load_file():
    """
    Returns deserialized JSON with schedule
    """
    with open("schedule.json", 'r', encoding="UTF-8") as fin:
        file_data = json.load(fin)

    return file_data["start_date"], file_data["schedule"]


if __name__ == '__main__':
    start_date, schedule = load_file()