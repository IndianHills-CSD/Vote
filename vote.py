#! C:\Python38-32\python.exe -u

import cgi, cgitb, re, encryptionlib as enc, os, mysql.connector as mysql, datetime as date
from connectlib import connect_db


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

    return errors


# MySQL database processing code here

# Intializes an empty list of error messages
errmsgs = []

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

if errctr == 0:
    # For when the page is still redirecting
    print("<!DOCTYPE html>")
    print('<html lang="en">')
    print("  <head>")
    print("    <title>Vote</title>")
    print("    <link rel='stylesheet' href='css/main-styles.css'>")
    print("  </head>")
    print("  <body>")
    print('    <div id="container">')
    print('      <div id="content">')
    print("         <h1>Thank you for voting!</h1>")
    print("         <p>Your vote was accepted!</p>")
    print('         <a href="index.html">Click here to return to the home page</a>')
    print("      </div>")
    print("    </div>")
    print("  </body>")
    print("</html>")
else:
    # Printed when invalid data is entered
    print("<!DOCTYPE html>")
    print('<html lang="en">')
    print("  <head>")
    print("    <title>Vote</title>")
    print("    <link rel='stylesheet' href='css/main-styles.css'>")
    print("  </head>")
    print("  <body>")
    print('    <div id="container">')
    print('      <div id="content">')
    print("        <h1>Error</h1>")

    # Prints any error messages when errors occur
    for i in range(errctr):
        print(errmsgs[i])

    print('        <a href="vote.html">Click here fix your mistakes</a>')
    print("      </div>")
    print("    </div>")
    print("  </body>")
    print("</html>")