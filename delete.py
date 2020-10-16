#! C:\Python38-32\python.exe -u

import mysql.connector as mysql, http.cookies as c
from cookielib import get_cookie
from connectlib import connect_db


def delete_account():
    """
    Deletes the current account that is being used
    """
    global err, errmsg
    uname = get_cookie()  # gets the current username that is being used

    try:
        # Prepared DELETE statement
        prep_delete = "DELETE FROM accounts WHERE uname = %s"

        # A tuple should always be used for binding placeholders (%s)
        cursor.execute(
            prep_delete, (uname,)  # you use (value,) when searching for a single value
        )

        delete_salt()

        db.commit()  # saves changes
    except mysql.Error as e:
        errmsg = "        <p>" + str(e) + "</p>"
        err = True


def delete_salt():
    """
    Deletes the salt that was used to encrypt data from the Salt table
    """
    accid = find_accid()  # gets an ID

    # Prepare DELETE statement
    prep_delete = "DELETE FROM salt WHERE accid = %s"

    # A tuple should always be used for binding placeholders (%s)
    cursor.execute(
        prep_delete, (accid,)  # you use (value,) when searching for a single value
    )

    db.commit()  # saves changes


def find_accid():
    """
    Finds the ID of an account for the Salt table
    """
    # The "uname" cookie is used so the original "username" is always used
    uname = get_cookie()
    accid = 0

    # Prepare SELECT statement
    prep_select = "SELECT accId FROM accounts WHERE uname = %s"

    # A tuple should always be used to bind placeholders
    cursor.execute(prep_select, (uname,))
    result = cursor.fetchall()  # returns a list of tuples

    if result:
        # Should only return one row
        (val_accid,) = result[0]  # unpacks the tuple
        accid = val_accid

    return accid


# Connects to database
db = connect_db()

errmsg = ""  # used to display error messages

err = False  # used to determine if an account was deleted

cursor = db.cursor(prepared=True)  # allows for prepare statements to be used
delete_account()

# Clears the "uname" cookie
uname_cookie = c.SimpleCookie()
uname_cookie["uname"] = ""
print(uname_cookie)  # prints Set-Cookie: uname=""

print("Content-Type: text/html\n")

# HTML code that is always printed
print("<!DOCTYPE html>")
print('<html lang="en">')
print("  <head>")
print("    <title>Delete Account</title>")
print('    <link rel="stylesheet" href="css/main-styles.css" />')
print("  </head>")
print("  <body>")
print('    <div id="container">')
print('      <div id="content">')

if err:
    print("        <h1>Error</h1>")
    print(errmsg)
else:
    print("        <h1>Your account was deleted!</h1>")
    print("        <p>Your account has been successfully deleted</p>")
    print('        <a href="login.html">Click here to continue</a>')

print("      </div>")
print("    </div>")
print("  </body>")
print("</html>")