# Willson Financial --- Milestone #2 (Setup + Display)

## What's in this folder

-   `willson_db_init.sql`\
    Creates the `willson_financial` database, tables, and inserts sample
    data (run once).

-   `willson_db_display.py`\
    Connects to the database and prints the contents of each table (run
    anytime).

-   `requirements.txt`\
    Python packages needed for the display script.

-   `.env`\
    Database connection settings (you create this locally).

------------------------------------------------------------------------

## 1) Create and activate a virtual environment

From inside `module-9`:

``` powershell
python -m venv .venv
.\.venv\Scripts\activate
```

Install requirements:

``` powershell
pip install -r requirements.txt
```

------------------------------------------------------------------------

## 2) Create your `.env` file (local only)

Create a file named `.env` in `module-9/`:

``` txt
USER=user
PASSWORD=pass
HOST=127.0.0.1
DATABASE=willson_financial
```

Note: Do not commit `.env` to GitHub.

------------------------------------------------------------------------

## 3) Run the SQL setup script (one time)

Open **MySQL Command Line Client**, then run:

``` sql
SOURCE Path/to/your/file/csd310/module-9/willson_init.sql;
```

(Adjust the path if your folder location is different.)

------------------------------------------------------------------------

## 4) Display the table data (anytime)

From inside `module-9`:

``` powershell
python .\willson_display.py
```

This prints the contents of: - client - employee - client_transaction -
appointment
