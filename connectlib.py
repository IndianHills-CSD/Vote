import mysql.connector as mysql, sys
from mysql.connector import Error

# Custom Python module/library for connecting to the "Vote" database


def connect_db():
    """
    Connects to the "Vote" database
    """
    try:
        conn = mysql.connect(
            host="localhost",
            user="root",
            password="",
            database="vote",
        )
        return conn

    except Error as e:
        print("<!DOCTYPE html>")
        print('<html lang="en">')
        print("  <head>")
        print("    <title>Database Eror</title>")
        print("  </head>")
        print("  <body>")
        print("    <h1>Error: Unable to connect to the database</h1>")
        print(
            "    <p>Please wait until this issue is resolved before visiting this website</p>"
        )

        # Displays the error that occured
        print("    <script>console.log('", e, "')</script>")

        print("  </body>")
        print("</html>")
        sys.exit()  # ends the Python script early