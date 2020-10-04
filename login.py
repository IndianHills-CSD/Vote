#! C:\Python38-32\python.exe -u

import cgi, cgitb, re, encryptionlib as enc, os, mysql.connector as mysql

# from connectlib import connect_db
from mysql.connector import Error


def valid_account(uname, psw):
    """
    Checks if a valid username and password was entered
    """
    global errmsgs
    errors = 0  # keeps track of all errors

    try:
        # Username validation
        if len(uname.strip()) == 0:
            errors += 1
            errmsgs.append("        <p>Username was not entered</p>")
        elif len(uname.strip()) < 4:
            errors += 1
            errmsgs.append(
                "        <p>Username should be at least 4 characters long</p>"
            )
    except AttributeError:
        errors += 1
        errmsgs.append("        <p>Username was not entered</p>")

    try:
        wschar = re.search("\s{1,}", psw)  # checks for any whitespace characters
        digits = re.search("\d{1,}", psw)  # checks for 1 or more digits

        # Password validation
        if len(psw.strip()) == 0:
            errors += 1
            errmsgs.append("        <p>Password was not entered</p>")
        elif len(psw.strip()) < 8 or wschar or not digits:
            errors += 1
            errmsgs.append(
                "        <p>Password should be at least 8 characters long and contain no whitespace characters and at least 1 digit</p>"
            )
    except AttributeError:
        errors += 1
        errmsgs.append("        <p>Password was not entered</p>")

    # Calls verify_account() when no errors occur
    #   if errors == 0:
    #      errors += verify_account(uname, psw)

    return errors


def verify_account(uname, psw):
    """
    Verifies that an account exists by searching for it in the database
    """
    global errmsgs  # ,db
    errors = 0

    # cursor = db.cursor()

    # SELECT statement for verifying the username that was entered
    select_uname = "SELECT uname, psw FROM accounts WHERE uname = '%s'"
    value = uname

    # SELECT statement for checking the password
    select_psw = "SELECT psw FROM accounts"

    # Executes the select statements
    # cursor.execute(select_uname, value)
    # cursor.execute(select_psw)

    # Gets the first row of the results (should only return one row)
    # result1 = cursor.fetchone()

    # Gets all the rows from the results
    # result2 = cursor.fetchall()

    #for row in result2:
    #    enc.verify_hash(
    #        row,
    #        psw,
    #    )

    # Checks if no matches were found
    # if not result1 :
    #    errors += 1
    #    errmsgs.append(
    #       "        <p>The account that was entered doesn't exist, please consider creating an account</p>"
    #    )

    # return errors


cgitb.enable()  # for debugging

# Connects to the database
# db = connect_db()

# Intializes an empty list of error messages
errmsgs = []
errctr = 0  # keeps track of all the errors that have occurred

form = cgi.FieldStorage()

# Username and Password Validation
if "uname" in form and "psw" in form:
    uname = form.getvalue("uname")
    psw = form.getvalue("psw")
else:
    if "uname" not in form:
        uname = ""
        psw = form.getvalue("psw")
    if "psw" not in form:
        uname = form.getvalue("uname")
        psw = ""

errctr += valid_account(uname, psw)

print("Content-Type: text/html")

if errctr == 0:
    # Sets the new location (URL) to the index.html page
    print("Location: http://localhost/vote-project/index.html")
    print()

    # For when the page is still redirecting
    print("<!DOCTYPE html5>")
    print('<html lang="en">')
    print("  <head>")
    print("    <title>Login</title>")
    print('    <link rel="stylesheet" href="css/main-styles.css" />')
    print("  </head>")
    print("  <body>")
    print('    <div id="container">')
    print('      <div id="content">')
    print("        <h1>Redirecting...</h1>")
    print(
        '        <a href="index.html">Click here if you are still being redirected</a>'
    )
    print("      </div>")
    print("    </div>")
    print("  </body>")
    print("</html>")
else:
    # Printed when invalid usernames and/or passwords are entered
    print()  # adds a blank line since a blank line needs to follow the Content-Type
    print("<!DOCTYPE html5>")
    print('<html lang="en">')
    print("  <head>")
    print("    <title>Login</title>")
    print('    <link rel="stylesheet" href="css/main-styles.css" />')
    print("  </head>")
    print("  <body>")
    print('    <div id="container">')
    print('      <div id="content">')
    print("        <h1>Error</h1>")

    # Prints any error messages when an invalid username or password is entered
    for i in range(errctr):
        print(errmsgs[i])

    print('        <a href="login.html">Click here fix your mistakes</a>')
    print("      </div>")
    print("    </div>")
    print("  </body>")
    print("</html>")
