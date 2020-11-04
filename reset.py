#! C:\Python38-32\python.exe -u

import cgi, cgitb, mysql.connector, encryptionlib as enc, os, re
from connectlib import connect_db


def valid_account(uname, psw1, psw2):
    """
    Checks if a valid username and password was entered and checks if the same password was
    re-entered
    """
    errors = 0  # keeps track of all errors
    val_psws = True  # determines if psw1 and psw2 should be checked for equality

    # Username validation
    if len(uname.strip()) == 0:
        errors += 1
        errmsgs.append("        <p>Username was not entered</p>")
    elif len(uname.strip()) < 4:
        errors += 1
        errmsgs.append("        <p>Username should be at least 4 characters long</p>")

    # Password validation
    wschar = re.search("\s{1,}", psw1)  # checks for any whitespace characters
    digits = re.search("\d{1,}", psw1)  # checks for 1 or more digits
    wschar2 = re.search("\s{1,}", psw2)  # checks for any whitespace characters
    digits2 = re.search("\d{1,}", psw2)  # checks for 1 or more digits

    if len(psw1.strip()) == 0 or len(psw2.strip()) == 0:
        errors += 1
        errmsgs.append(
            "        <p>Password was either not entered at all or not re-entered</p>"
        )
        valPsws = False
    elif (
        len(psw1.strip()) < 8
        or wschar
        or not digits
        or len(psw2.strip()) < 8
        or wschar2
        or not digits2
    ):
        errors += 1
        errmsgs.append(
            '        <div class="center">\n\t\t  <p>Password should be at least 8 characters long, contain no whitespace characters, and contain at least 1 digit</p>\n\t\t  </div>'
        )
        val_psws = False

    if val_psws:
        if psw1.strip() != psw2.strip():
            errors += 1
            errmsgs.append(
                '        <div class="center">\n\t\t  <p>The password that was re-entered does not match the original password that was entered</p>\n\t\t  </div>'
            )

    return errors


def reset_psw(uname, psw):
    """
    Updates the user's password in the Accounts table
    """
    try:
        errors = 0
        errors += new_psw(uname, psw)

        # Deterimes if update_psw() should be called
        if errors == 0:
            update_psw(uname, psw)

    except mysql as e:
        errors += 1
        msg = "        <p>" + str(e) + "</p>"
        errmsgs.append(msg)

    return errors


def new_psw(uname, psw):
    """
    Checks if a new password was entered
    """
    errors = 0

    # Prepare SELECT statement
    prep_select = "SELECT pwd FROM accounts WHERE uname = %s"

    cursor.execute(prep_select, (uname,))
    results = cursor.fetchall()  # returns a list of tuples

    if results:
        (enc_psw,) = results[0]
        salt = eval(get_salt())  # converts the salt value back to bytes

        if enc.verify_hash(enc_psw, psw, salt):
            errors += 1
            errmsgs.append("        <p>This password has already been used</p>")
    else:
        errors += 1
        errmsgs.append("        <p>Account was not found</p>")

    return errors


def get_salt():
    """
    Gets a value salt or an empty string ("") to use for verifying encrypted passwords
    """
    accid = get_accid()  # gets an ID

    # Prepare SELECT statement
    prep_select = "SELECT salt FROM salt WHERE accId = %s"

    cursor.execute(prep_select, (accid,))

    result = cursor.fetchall()  # returns a list of tuples

    if result:
        (salt,) = result[0]
        return salt
    else:
        return ""


def get_accid():
    """
    Finds the ID of an account for the Salt table
    """
    accid = 0

    # Prepare SELECT statement
    prep_select = "SELECT accId FROM accounts WHERE uname = %s"

    # A tuple should always be used to bind placeholders
    cursor.execute(prep_select, (uname,))
    result = cursor.fetchall()  # returns a list of tuples

    # Checks if any rows were found
    if result:
        (val_accid,) = result[0]  # unpacks the tuple
        accid = val_accid

    return accid


def update_psw(uname, psw):
    """
    Updates the user's password in the Accounts table using the prepare statement
    """
    salt = eval(find_salt())  # converts the value returned back to bytes
    enc_psw = enc.create_hash(psw, salt)  # encrypts the new password that was entered

    # Prepare UPDATE statement
    prep_update = "UPDATE accounts SET pwd = %s WHERE uname = %s"

    # A tuple should always be used when binding placeholders (%s)
    cursor.execute(prep_update, (enc_psw, uname))

    db.commit()  # saves changes


def find_salt():
    """
    Determines which salt to use for encrypting passwords
    """
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


errctr = 0  # keeps track of the total number of errors that have been found
errmsgs = []  # intializes an empty list of error messages

# Connects to the database
db = connect_db()

cursor = db.cursor(prepared=True)  # allows the prepare statement to be used

form = cgi.FieldStorage()

# Username and Password Validation
if "uname" in form:
    uname = form.getvalue("uname")
else:
    uname = ""

if "psw1" in form:
    psw1 = form.getvalue("psw1")
else:
    psw1 = ""

if "psw2" in form:
    psw2 = form.getvalue("psw2")
else:
    psw2 = ""

errctr += valid_account(uname, psw1, psw2)

# Checks if no errors have occurred up to this point
if errctr == 0:
    errctr += reset_psw(uname, psw1)

print("Content-Type: text/html")

# Checks if no errors occurred at all
if errctr == 0:
    # Sets the new location (URL) to the login.html page
    print("Location: http://localhost/vote-project/login.html\n")

    # For when the page is still redirecting
    print("<!DOCTYPE html>")
    print('<html lang="en">')
    print("  <head>")
    print("    <title>Reset Password</title>")
    print('    <link rel="stylesheet" href="css/main-styles.css" />')
    print("  </head>")
    print("  <body>")
    print('    <div id="container">')
    print('      <div id="content">')
    print("        <h1>Redirecting...</h1>")
    print(
        '          <a href="login.html">Click here if you are still being redirected</a>'
    )
else:
    # Printed when invalid account information is entered
    print()  # adds a blank line since a blank line needs to follow the Content-Type
    print("<!DOCTYPE html>")
    print('<html lang="en">')
    print("  <head>")
    print("    <title>Reset Password</title>")
    print('    <link rel="stylesheet" href="css/main-styles.css" />')
    print("  </head>")
    print("  <body>")
    print('    <div id="container">')
    print('      <div id="content">')
    print("        <h1>Error</h1>")

    # Prints any error messages when errors occur
    for i in range(errctr):
        print(errmsgs[i])

    print('        <a href="reset.html">Click here to fix your mistakes</a>')

print("      </div>")
print("    </div>")
print("  </body>")
print("</html>")