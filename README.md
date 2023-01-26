# Go to a URL according to a schedule

This script reads schedule from a JSON file and opens a URL in a web browser, according to the current time and date.

The original purpose of the script was to semi-automate the process of searching the link to the scheduled weekly online meeting, when its host doesn't bother to change it every time. Obviously, it can be useful to the participants of remote education.

## Features
* The schedule can have items that occurs once per two weeks

## Usage

The default Python interpreter installed on your system (don't forget to check if it is installed before running the script) will be enough to use this script. I used Python 3.10.6 on Windows 10 64-bit. No external packages needed.

Also, you will need a `schedule.json` file located in the same directory with the script. This repository contains a [folder](schedule_examples) with detailed description of the file structure.

### Suggested features

Those features may be added in the future, if somebody would like to do it.

* Use schedule file located elsewhere and named anylike. *As I see it, the path to the file could be either asked from the user of accepted as an startup argument (ex. `$ main.py -f C:\Users\admin\Downloads\1-A.json`)*  
* Visual schedule editor
* Add unit tests
* Automatic URL fetching from RSS feed or an online messaging app
* Automate URL opening. *But there is already a Task Scheduler on Windows*
* Desktop executable or smartphone app. *I guess, it should be another project*
* Other crazy schedule setups support. *It is fortunately though I haven't seen anything like that*