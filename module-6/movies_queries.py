# ---------------------------------------------------------------
# Author:       Zak Nizam
# Date:         January 29, 2026
# Course:       CSD310 - Database Development and Use
# Assignment:   Module 6.2 - Movies: Table Queries
#
# Purpose:
#   This script connects to the MySQL movies database
#   and runs several SELECT queries using Python.
# ---------------------------------------------------------------

# imports needed to connect to MySQL
import mysql.connector
from mysql.connector import errorcode

# imports for reading the .env file
from dotenv import dotenv_values


# load database credentials from .env file (stored in module-5)
secrets = dotenv_values("../module-5/.env")

# database connection configuration
config = {
    "user": secrets["USER"],
    "password": secrets["PASSWORD"],
    "host": secrets["HOST"],
    "database": secrets["DATABASE"],
    "raise_on_warnings": True
}


try:
    # attempt to connect to the database
    db = mysql.connector.connect(**config)
    cursor = db.cursor()

    print("\n-- DISPLAYING Studio RECORDS --")

    # Query 1: select all fields from studio table
    cursor.execute("SELECT studio_id, studio_name FROM studio")
    studios = cursor.fetchall()

    for studio in studios:
        print(f"Studio ID: {studio[0]}")
        print(f"Studio Name: {studio[1]}\n")


    print("\n-- DISPLAYING Genre RECORDS --")

    # Query 2: select all fields from genre table
    cursor.execute("SELECT genre_id, genre_name FROM genre")
    genres = cursor.fetchall()

    for genre in genres:
        print(f"Genre ID: {genre[0]}")
        print(f"Genre Name: {genre[1]}\n")


    print("\n-- DISPLAYING Short Film RECORDS --")

    # Query 3: films with runtime less than 120 minutes
    cursor.execute("""
        SELECT film_name, film_runtime
        FROM film
        WHERE film_runtime < 120
    """)
    films = cursor.fetchall()

    for film in films:
        print(f"Film Name: {film[0]}")
        print(f"Runtime: {film[1]}\n")


    print("\n-- DISPLAYING Director RECORDS in Order --")

    # Query 4: films grouped by director
    cursor.execute("""
        SELECT film_name, film_director
        FROM film
        ORDER BY film_director
    """)
    directors = cursor.fetchall()

    for director in directors:
        print(f"Film Name: {director[0]}")
        print(f"Director: {director[1]}\n")


    input("\nPress any key to continue...")

except mysql.connector.Error as err:
    # handle common database errors
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Invalid username or password.")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("The database does not exist.")
    else:
        print(err)

finally:
    # close database connection
    if 'db' in locals():
        db.close()