#! C:\Python38-32\python.exe -u

import cgi, cgitb, re, encryptionlib as enc, os, mysql.connector as mysql, datetime as date
from connectlib import connect_db

# mysql account verification code


# mysql candidate validation code


def valid_amt(amt):
    """
    Checks if a valid donation amout was entered
    """
    global errmsgs
    errors = 0  # keeps track of all the errors that have be

    if float(amt) > 9999.99:
        errors += 1
        errmsgs.append("        <p>Donations should not exceed $9,999.99</p>")
    elif float(amt) <= 0:
        errors += 1
        errmsgs.append("        <p>Donations should not be below $0.01</p>")

    return errors


def valid_creditcard(ccnum, cvv, expm, expy):
    """
    Checks if valid credit card information was entered
    """
    global errmsgs
    errors = 0  # keeps track of all the errors that have occured

    # Regex pattern for validating credit card numbers
    ccnumformat = re.search("([\d]{3,6}[-][\d]{4,5}[-][\d]{4,5}([-][\d]{4,5})?)", ccnum)

    if len(ccnum.strip()) == 0:
        errors += 1
        errmsgs.append("        <p>Credit card number was not entered</p>")
    elif not ccnumformat:
        errors += 1
        errmsgs.append(
            "        <p>Credit card number is in the incorrect format, it should look something like this: 1234-12345-12345</p>"
        )

    if len(cvv) == 0:
        errors += 1
        errmsgs.append("        <p>CVV was not entered</p>")
    elif int(cvv) < 100 or int(cvv) > 999:
        errors += 1
        errmsgs.append("        <p>CVV must be 3 digits long</p>")

    if len(expm.strip()) == 0 or len(expy.strip()) == 0:
        errors += 1
        errmsgs.append("        <p>The credit card expiration date is incomplete </p>")
    else:
        curryr = date.datetime.today().strftime("%Y")
        currmon = date.datetime.today().strftime("%m")
        monnum = date.datetime.strptime(str(expm), "%B").month

        if int(currmon) > monnum and int(curryr) > int(expy):
            errors += 1
            errmsgs.append(
                "        <p>This credit card can no longer be used, it has already expired</p>"
            )
        elif int(currmon) > monnum and int(curryr) == int(expy):
            errors += 1
            errmsgs.append(
                "        <p>This credit card can no longer be used, it has already expired</p>"
            )

    return errors


# MySQL validation for the candidate that was entered

# Intializes an empty list of error messages
errmsgs = []

errctr = 0  # keeps track of all errors
form = cgi.FieldStorage()

# Account Validation
if not "uname" in form or not "psw" in form:
    errctr += 1
    errmsgs.append("        <p>No account was entered</p>")

# Donation Information Validation
if "can" in form and "amt" in form:
    amt = form.getvalue("amt")
    valid_amt(amt)
else:
    errctr += 1
    errmsgs.append("        <p>A donation was not placed for any canidate</p>")

# Credit Card Information Validation
if "ccnum" in form:
    ccnum = form.getvalue("ccnum")
else:
    ccnum = ""

if "cvv" in form:
    cvv = form.getvalue("cvv")
else:
    cvv = ""

if "expm" in form:
    expm = form.getvalue("expm")
else:
    expm = ""

if "expy" in form:
    expy = form.getvalue("expy")
else:
    expy = ""

errctr += valid_creditcard(ccnum, cvv, expm, expy)

print("Content-Type: text/html\n")

if errctr == 0:
    # Printed when a valid donation was placed
    print("<!DOCTYPE html>")
    print('<html lang="en">')
    print("  <head>")
    print("    <title>Donation</title>")
    print("    <link rel='stylesheet' href='css/main-styles.css'>")
    print("  </head>")
    print("  <body>")
    print('    <div id="container">')
    print('      <div id="content">')
    print("         <h1>Thank you for donating!</h1>")
    print("         <p>Your donation was accepted!</p>")
    print('         <a href="index.html">Click here to return to the home page</a>')
    print("      </div>")
    print("    </div>")
    print("  </body>")
    print("</html>")
else:
    # Printed when invalid donation information is entered
    print("<!DOCTYPE html>")
    print('<html lang="en">')
    print("  <head>")
    print("    <title>Donation</title>")
    print("    <link rel='stylesheet' href='css/main-styles.css'>")
    print("  </head>")
    print("  <body>")
    print('    <div id="container">')
    print('      <div id="content">')
    print("        <h1>Error</h1>")

    # Prints any error messages when errors occur
    for i in range(errctr):
        print(errmsgs[i])

    print('        <a href="donation.html">Click here fix your mistakes</a>')
    print("      </div>")
    print("    </div>")
    print("  </body>")
    print("</html>")
