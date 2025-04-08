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

name = sys.argv[1]

### Queries

FIND_PERSON_QUERY = """
   SELECT
      id
   FROM people p
   WHERE
      p.name = %s
"""

WRITTEN_FILMS_QUERY = """
   SELECT
      p.id
   FROM people p 
   JOIN principals pp ON p.id = pp.person
   WHERE
      pp.job = 'writer'
      AND p.name = %s
   ORDER BY p.id
"""


GET_FILMS_QUERY = """
   SELECT
      m.title,
      m.year
   FROM people p 
   JOIN principals pp ON p.id = pp.person
   JOIN movies m ON pp.movie = m.id
   WHERE
      p.id = %s
      AND pp.job = 'writer'

   ORDER BY m.year, m.title
"""


### Manipulating database
try:
   db = psycopg2.connect("dbname=ass2")
   # your code goes here 
   cur = db.cursor()

   # finding if person exists
   cur.execute(FIND_PERSON_QUERY, [name])

   people = cur.fetchall()

   # there was one person returned -> Not a writer

   # there was multiple people returned -> ALL not writers

   if not people:
      print("No such person")
      exit(0)

   cur.execute(WRITTEN_FILMS_QUERY, [name])

   writer = cur.fetchone()

   if len(people) == 1 and not writer:
      print(f"{name} has not written any films")
      exit(0)

   if len(people) > 1 and not writer: 
      print(f"None of the people called {name} have written any films")
      exit(0)

   cur.execute(GET_FILMS_QUERY, [writer])

   films = cur.fetchall()

   for title, year in films:
      print(f"{title} ({year})")
   
   
except Exception as err:
   print("DB error: ", err)
finally:
   if db:
      db.close()

