===========
cron_parser
===========


This is a command-line programm that aims to parse the cron string.


Description
===========

Usage
-----

Prerequisites
^^^^^^^^^^^^^
1. Python >= 3.4

Installation
^^^^^^^^^^^^
1. cd into the root directory
2. execute command: **python setup.py install**

Run program
^^^^^^^^^^^
usage: cron_parser [-h] [-v] [-vv] [String [String ...]]

positional arguments:
  STRING               String formed by cron string and the command

optional arguments:
  -h, --help             show this help message and exit
  --version              show program's version number and exit
  -v, --verbose          set loglevel to INFO
  -vv, --very-verbose    set loglevel to DEBUG

special character in arguements:
  \* needs to be escaped in command, please quote it when it is standalone in command.
  Example shows the usage.

Example
^^^^^^^
| >cron_parser */15 0 1,15 "*" 1-5 /usr/bin/find
| minute          0 15 30 45 
| hour            0 
| day of month    1 15 
| month           1 2 3 4 5 6 7 8 9 10 11 12 
| day of week     1 2 3 4 5 
| command         /usr/bin/find


Test
^^^^
Test can be carried out type in:
*python setup.py test* in the root directory 

Note
====

1. It is also recommended to run the commands in a clean virtual environment for python.
2. If there is any unexpected issue that the program cannot be installed by setuptools, the main.py is in <root>/src/gc_test and can be executed in <root>/src/ by **python3 -m gc_test.main**, which has the same usage as gcclac. This also depends requirements.txt. Command is **pip3 install -r requirements.txt**

