#! C:\Python38-32\python.exe -u

import cgi, cgitb, re, encryptionlib as enc, os, mysql.connector as mysql, http.cookies as c
from connectlib import connect_db
from cookielib import get_cookie


def valid_vote(party, can):
    """
    Checks if a vote that was entered is valid
    """
    global errmsgs
    errors = 0

    # Political Party Validation
    if len(party.strip()) == 0:
        errors += 1
        errmsgs.append("        <p>No political party was selected</p>")

    # Candidate Validation
    # Regex pattern for validating candidates
    canformat = re.search("^([A-Z|a-z]{1,}[\s][A-Z|a-z]{1,})$", can)

    if len(can.strip()) == 0:
        errors += 1
        errmsgs.append("        <p>No candidate was entered</p>")
    elif not canformat:
        errors += 1
        errmsgs.append(
            "        <p>The name of a candidate should include their first and last name</p>"
        )

    if errors == 0:
        insert_vote()

    return errors


def insert_vote():
    """
    Stores the vote that was place by the user
    """
    global errctr

    try:
        accid = find_accid()  # gets an id

        # Prepare INSERT statement
        prep_insert = (
            "INSERT INTO votes (accId, candidate, polParty) VALUES (%s, %s, %s)"
        )

        # A tuple should always be used to bind placeholders (%s)
        cursor.execute(prep_insert, (accid, can, party[0]))

        db.commit()  # saves changes
    except mysql.Error as e:
        errctr += 1
        msg = "        <p> " + e + " </p>"
        errmsgs.append(msg)


def find_accid():
    """
    Finds the id of an account for the Votes table
    """
    accid = 0

    uname = get_cookie()

    # Prepare SELECT statement
    prep_select = "SELECT accId FROM accounts WHERE uname = %s"

    cursor.execute(prep_select, (uname,))
    result = cursor.fetchall()  # returns a list of tuples

    if result:
        (val_id,) = result[0]  # unpacks the tuple
        accid = int(val_id)

    return accid


# Intializes an empty list of error messages
errmsgs = []

# Connects to the database
db = connect_db()

cursor = db.cursor(prepared=True)  # allows the prepare statement to be used

errctr = 0  # keeps track of all errors
form = cgi.FieldStorage()

# Vote Validation
if "party" in form and "can" in form:
    party = form.getlist("party")
    can = form.getvalue("can")
else:
    if "party" not in form:
        party = [""]
    else:
        party = form.getlist("party")
    if "can" not in form:
        can = ""
    else:
        can = form.getvalue("can")

errctr += valid_vote(party[0], can)

print("Content-Type: text/html\n")

# HTML code that is always printed
print("<!DOCTYPE html>")
print('<html lang="en">')
print("  <head>")
print("    <title>Vote</title>")
print("    <link rel='stylesheet' href='css/main-styles.css'>")
print("  </head>")
print("  <body>")
print('    <div id="container">')
print('      <div id="content">')

if errctr == 0:
    # For when the page is still redirecting
    print("         <h1>Thank you for voting!</h1>")
    print("         <p>Your vote was accepted!</p>")
    print('         <a href="index.html">Click here to return to the home page</a>')
else:
    # Printed when invalid data is entered
    print("        <h1>Error</h1>")

    # Prints any error messages when errors occur
    for i in range(errctr):
        print(errmsgs[i])

    print('        <a href="vote.html">Click here to fix your mistakes</a>')

# More HTML code that is always printed
print("      </div>")
print("    </div>")
print("  </body>")
print("</html>")
