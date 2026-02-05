# ---------------------------------------------------------------
# Author:       Zak Nizam
# Date:         February 05, 2026
# Course:       CSD310 - Database Development and Use
# Assignment:   Module 7.2 - Movies: Update & Deletes
#
# Purpose:
#   This script connects to the MySQL movies database and:
#     1) Displays films (joined to studio + genre names)
#     2) Inserts a new film (not Star Wars)
#     3) Updates Alien to Horror
#     4) Deletes Gladiator
#   Output is formatted to match expected assignment output.
# ---------------------------------------------------------------

import mysql.connector
from mysql.connector import errorcode
from dotenv import dotenv_values


# read DB login from module-5 .env 9 (change to)
secrets = dotenv_values("../module-5/.env")

# database connection configuration
config = {
    "user": secrets["USER"],
    "password": secrets["PASSWORD"],
    "host": secrets["HOST"],
    "database": secrets["DATABASE"],
    "raise_on_warnings": True
}


def get_column_type(cursor, table_name, column_name):
    """
    Returns the MySQL column type as a string, ex: 'date', 'varchar(20)', 'year'
    """
    cursor.execute(f"SHOW COLUMNS FROM {table_name} LIKE %s;", (column_name,))
    row = cursor.fetchone()
    if not row:
        return None
    return str(row[1]).lower()


def show_films(cursor, title):
    """
    Displays film data with INNER JOINs to show genre and studio names
    """
    print(f"\n  -- {title} --")

    query = """
        SELECT
            film.film_name,
            film.film_director,
            genre.genre_name,
            studio.studio_name
        FROM film
        INNER JOIN genre ON film.genre_id = genre.genre_id
        INNER JOIN studio ON film.studio_id = studio.studio_id
        ORDER BY film.film_name;
    """

    cursor.execute(query)
    films = cursor.fetchall()

    for film in films:
        print(f"  Film Name: {film[0]}")
        print(f"  Director: {film[1]}")
        print(f"  Genre Name: {film[2]}")
        print(f"  Studio Name: {film[3]}\n")


try:
    db = mysql.connector.connect(**config)
    cursor = db.cursor()

    # Optional: quick schema check so we don't fight date formatting errors
    release_type = get_column_type(cursor, "film", "film_releaseDate")
    if release_type is None:
        print("  Could not find film_releaseDate column in film table.")
    else:
        print(f"\n  film.film_releaseDate column type detected as: {release_type}")

    # 1) Display films
    show_films(cursor, "DISPLAYING FILMS")

    # 2) Insert a new film (NOT Star Wars)
    insert_query = """
        INSERT INTO film (film_name, film_releaseDate, film_runtime, film_director, studio_id, genre_id)
        VALUES (%s, %s, %s, %s,
            (SELECT studio_id FROM studio WHERE studio_name = %s),
            (SELECT genre_id FROM genre WHERE genre_name = %s)
        );
    """

    # Choose a release date value that fits your actual column type
    # If it's DATE/DATETIME/TIMESTAMP, use YYYY-MM-DD
    # If it's YEAR or a short varchar, use YYYY
    if release_type and ("date" in release_type or "time" in release_type):
        release_value = "2015-10-02"
    else:
        # safest fallback is just the year
        release_value = "2015"

    new_film = (
        "The Martian",          # film_name (choose any film except Star Wars)
        release_value,          # release date (auto-adjusts based on column type)
        144,                    # runtime (minutes)
        "Ridley Scott",         # director
        "20th Century Fox",     # existing studio
        "SciFi"                 # existing genre
    )

    cursor.execute(insert_query, new_film)
    db.commit()

    # Display after insert
    show_films(cursor, "DISPLAYING FILMS AFTER INSERT")

    # 3) Update Alien to Horror
    update_query = """
        UPDATE film
        SET genre_id = (SELECT genre_id FROM genre WHERE genre_name = 'Horror')
        WHERE film_name = 'Alien';
    """
    cursor.execute(update_query)
    db.commit()

    show_films(cursor, "DISPLAYING FILMS AFTER UPDATE - CHANGED ALIEN TO HORROR")

    # 4) Delete Gladiator
    delete_query = "DELETE FROM film WHERE film_name = 'Gladiator';"
    cursor.execute(delete_query)
    db.commit()

    show_films(cursor, "DISPLAYING FILMS AFTER DELETE")

    input("\n  Press any key to continue...")

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("  Invalid username or password.")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("  The database does not exist.")
    else:
        print(err)

finally:
    try:
        cursor.close()
    except Exception:
        pass

    try:
        db.close()
    except Exception:
        pass