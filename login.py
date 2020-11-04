#! C:\Python38-32\python.exe -u

import cgi, cgitb, re, encryptionlib as enc, os, mysql.connector as mysql, http.cookies as c
from connectlib import connect_db


def valid_account(uname, psw):
    """
    Checks if a valid username and password was entered
    """
    errors = 0

    # Username validation
    if len(uname.strip()) == 0:
        errors += 1
        errmsgs.append("        <p>Username was not entered</p>")
    elif len(uname.strip()) < 4:
        errors += 1
        errmsgs.append("        <p>Username should be at least 4 characters long</p>")

    # Password validation
    wschar = re.search("\s{1,}", psw)  # checks for any whitespace characters
    digits = re.search("\d{1,}", psw)  # checks for 1 or more digits

    if len(psw.strip()) == 0:
        errors += 1
        errmsgs.append("        <p>Password was not entered</p>")
    elif len(psw.strip()) < 8 or wschar or not digits:
        errors += 1
        errmsgs.append(
            "        <p>Password should be at least 8 characters long and contain no whitespace characters and at least 1 digit</p>"
        )

    # Calls verify_account() when no errors occur
    if errors == 0:
        errors += verify_account(uname, psw)

    return errors


def verify_account(uname, psw):
    """
    Verifies that an account exists by searching for it in the database
    """
    errors = 0

    # Prepare SELECT statement
    prep_select = "SELECT pwd FROM accounts WHERE uname = %s"

    # A tuple should always be used for binding placeholders (%s)
    cursor.execute(
        prep_select, (uname,)  # you write (var,) when searching for one value
    )

    # Gets all the rows from the results
    result = cursor.fetchall()  # returns a list of tuples

    # Checks if no matches were found
    if not result:
        errors += 1
        errmsgs.append("        <p>The username that was entered doesn't exist</p>")
    else:
        # Converts the string value that is returned in find_salt() back to bytes
        salt = eval(find_salt())

        (hashed_psw,) = result[0]  # unpacks the tuple

        if not enc.verify_hash(hashed_psw, psw, salt):
            errors += 1
            errmsgs.append(
                "        <p>The password that was entered is not correct</p>"
            )

    return errors


def find_salt():
    """
    Determines which salt to use for verifying passwords
    """
    global cursor
    salt = ""  # returns nothing if invalid

    # Prepare SELECT statement
    prep_select = "SELECT salt FROM salt WHERE accId = %s"

    accid = find_accid()

    # A tuple is always use when binding placeholders (%s)
    cursor.execute(
        prep_select, (accid,)  # you write (var,) when searching for one value
    )
    result = cursor.fetchall()  # returns a list of tuples

    if result:
        (val_salt,) = result[0]  # unpacks the tuple
        salt = val_salt

    return salt


def find_accid():
    """
    Finds the id of an account in the Salt table
    """
    global cursor
    accid = 0

    # Prepare SELECT statement
    prep_select = "SELECT accId FROM accounts WHERE uname = %s"

    # A tuple is always use when binding placeholders (%s)
    cursor.execute(
        prep_select, (uname,)  # you write (var,) when searching for one value
    )
    result = cursor.fetchall()  # returns a list of tuples

    if result:
        (val_id,) = result[0]  # unpacks the tuple
        accid = int(val_id)

    return accid


cgitb.enable()  # for debugging

# Connects to the database
db = connect_db()

cursor = db.cursor(prepared=True)  # allows us to use prepare statements

# Intializes an empty list of error messages
errmsgs = []
errctr = 0  # keeps track of all the errors that have occurred

form = cgi.FieldStorage()

# Username and Password Validation
if "uname" not in form:
    uname = ""
else:
    uname = form.getvalue("uname")

if "psw" not in form:
    psw = ""
else:
    psw = form.getvalue("psw")

errctr += valid_account(uname, psw)

# Creates a cookie for storing a valid username
cookies = c.SimpleCookie()
cookies["uname"] = uname
print(cookies["uname"])  # prints "Set-Cookie: uname=value"

print("Content-Type: text/html")

# Checks if any errors occurred
if errctr == 0:
    # Sets the new location (URL) to the index.html page
    print("Location: http://localhost/vote-project/index.html\n")

    # For when the page is still redirecting
    print("<!DOCTYPE html>")
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
else:
    # Printed when invalid usernames and/or passwords are entered
    print()  # adds a blank line since a blank line needs to follow the Content-Type
    print("<!DOCTYPE html>")
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

    print('        <a href="login.html">Click here to fix your mistakes</a>')

# HTML code that is always printed
print("      </div>")
print("    </div>")
print("  </body>")
print("</html>")