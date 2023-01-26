# Before running the script, rename the file to `schedule.json`!

---

# About the structure of the schedule JSON file

The root object starts with "**start_date**" that equals to the `time.struct_time.tm_yday` of the first day of the week (ex. Monday) of the first week. Its purpose is to get the current number of the week, if the schedule has items that occur only once per two weeks. If you have the same schedule every week, you can skip this pair.

The schedule is located in the "**schedule**" object. It includes arrays with items, distributed by days of the week. Those days are labeled as numbers from 0 to 6, where 0 is Monday.

Those arrays contain objects that represent the items of the schedule. It consists from several fields. "**name**" will be printed to the console output to show the item that the script chose. "**until**" shows the time, until which that item is valid. "**url**" holds the URL, which will be opened it the system's default web browser. (Optional) "**week**" can be either 0 or 1. It tells on which week the item is valid.