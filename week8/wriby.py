#!/usr/bin/python3

# Print a list of movies written by a given person

import sys
import psycopg2

### Globals

db = None
usage = f"Usage: {sys.argv[0]} FullName"

### Command-line args

if len(sys.argv) < 2:
   print(usage)
   exit(1)

# process the command-line args ...


### Queries


### Manipulating database
try:
   db = psycopg2.connect("dbname=ass2")
   # your code goes here 
   
except Exception as err:
   print("DB error: ", err)
finally:
   if db:
      db.close()

