# ---------------------------------------------------------------
# Author:       Zak Nizam
# Group:        4
# Members:      Zak Nizam, Caleb Schumacher
# Date:         February 20, 2026
# Course:       CSD310 - Database Development and Use
# Assignment:   Milestone #2 - Willson Financial (DB Display)
#
# Purpose:
#   Connects to the database and prints the contents of each table.
#   Safe to run anytime (read-only).
#
# Notes:
#   - Reads DB creds from ./root-folder/.env
# ---------------------------------------------------------------

import mysql.connector
from mysql.connector import errorcode
from dotenv import dotenv_values


secrets = dotenv_values("./.env")

config = {
    "user": secrets["USER"],
    "password": secrets["PASSWORD"],
    "host": secrets["HOST"],
    "database": secrets["DATABASE"],
    "raise_on_warnings": True
}


def show_table(cursor, table_name: str, title: str) -> None:
    print(f"\n  -- {title} --")
    cursor.execute(f"SELECT * FROM {table_name};")
    rows = cursor.fetchall()

    if not rows:
        print("  (no records found)")
        return

    for row in rows:
        print(f"  {row}")


try:
    db = mysql.connector.connect(**config)
    cursor = db.cursor()

    show_table(cursor, "client", "CLIENT TABLE")
    show_table(cursor, "employee", "EMPLOYEE TABLE")
    show_table(cursor, "client_transaction", "TRANSACTION TABLE")
    show_table(cursor, "appointment", "APPOINTMENT TABLE")

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
