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
            user="root",    # uses the default username and password
            password="",
            database="vote",
        )
        return conn

    except Error as e:
        # Displays a custom Error page when unable to connect to the database
        print("Content-Type: text/html\n")

        print("<!DOCTYPE html>")
        print('<html lang="en">')
        print("  <head>")
        print("    <title>Database Error</title>")
        print("  </head>")
        print("  <body>")
        print("    <h1>Error: Unable to connect to the database</h1>")
        print(
            "    <p>Please wait until this issue is resolved before visiting this website</p>"
        )

        # Displays the error that occured and a message in the console
        print('    <script>console.error("' + str(e) + '");</script>')
        print(
            '    <script>console.log("Please check the connectlib.py file to resolve this error");</script>'
        )

        print("  </body>")
        print("</html>")
        sys.exit()  # ends the Python script that is using this method early