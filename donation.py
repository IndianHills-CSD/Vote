#! C:\Python38-32\python.exe -u

import cgi, cgitb, re, encryptionlib as enc, os, mysql.connector as mysql, datetime as date, bitcoinlib as bc
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
        errmsgs.append(
            "        <p>The username that was entered doesn't exist, please consider creating an account</p>"
        )
    else:
        # Converts the string value that is returned in find_salt() back to bytes
        salt = eval(find_salt())

        (hashed_psw,) = result[0]  # unpacks the tuple

        if not enc.verify_hash(hashed_psw, psw, salt):
            errors += 1
            errmsgs.append(
                "        <p>The password that was entered is not correct for the username that was entered</p>"
            )

    return errors


def find_salt():
    """
    Determines which salt to use for verifying passwords
    """
    salt = ""  # returns nothing if invalid

    # Prepare SELECT statement
    prep_select = "SELECT salt FROM accounts NATURAL JOIN salt WHERE accId = %s"

    accid = find_accid()

    cursor.execute(prep_select, (accid,))
    result = cursor.fetchall()  # returns a list of tuples

    if result:
        (val_salt,) = result[0]  # unpacks the tuple
        salt = val_salt

    return salt


def find_accid():
    """
    Finds the id of an account for the Salt and Donations tables
    """
    global uname
    accid = 0

    # Prepare SELECT statement
    prep_select = "SELECT accId FROM accounts WHERE uname = %s"

    cursor.execute(prep_select, (uname,))
    result = cursor.fetchall()  # returns a list of tuples

    if result:
        (val_id,) = result[0]  # unpacks the tuple
        accid = int(val_id)

    return accid


def valid_candidate(can):
    """
    Checks if a valid name for a candidate was entered
    """
    errors = 0

    # Regex pattern for validating candidates
    canformat = re.search("^([A-Z|a-z]{1,}[\s][A-Z|a-z]{1,})$", can)

    if len(can.strip()) == 0:
        errors += 1
        errmsgs.append("        <p>No candidate was entered</p>")
    elif not canformat:
        errors += 1
        errmsgs.append(
            "        <p>The name of a candidate should include their firstname and lastname</p>"
        )

    if errors == 0:
        errors += verify_candidate(can)

    return errors


def verify_candidate(can):
    """
    Verifies that a candidate exists by searching the database
    """
    errors = 0

    # Prepare SELECT statement
    prep_select = "SELECT candidate FROM votes WHERE candidate = %s"

    # A tuple should always be used for binding placeholders (%s)
    cursor.execute(prep_select, (can,))  # you write (var,) when searching for one value
    result = cursor.fetchall()  # returns a list of tuples

    if not result:
        errors += 1
        errmsgs.append("        <p>An unknown candidate was entered</p>")

    return errors


def valid_amt(amt):
    """
    Checks if a valid donation amout was entered
    """
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
    errors = 0  # keeps track of all the errors that have occured

    # Regex pattern for validating credit card numbers
    ccnumformat = re.search("([\d]{3,6}[-][\d]{4,5}[-][\d]{4,5}([-][\d]{4,5})?)", ccnum)

    if len(ccnum.strip()) == 0 and len(bitcoin) == 0:
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


def valid_bitcoin(bitcoin):
    """
    Verifies the bitcoin that was entered
    """
    errors = 0

    if bitcoin == "17wR7WdrmLH6R387xeA3ahYCo91Up9A34T":
        errors += 1
        errmsgs.append(
            "        <p>The Bitcoin that was entered should not match the recipient's Bitcoin</p>"
        )
    else:
        if not bc.check_bc(bitcoin):
            errors += 1
            errmsgs.append("        <p>The Bitcoin that was entered is invalid</p>")

    return errors


def insert_donation():
    """
    Stores the donation that was placed in the Donations table
    """
    global errctr

    try:
        accid = find_accid()  # gets an ID

        # Generates a random number of bytes to be used to create a new hash
        salt = os.urandom(64)

        if bitcoin == "":
            # Encrypts the credit card number and CVV that was entered
            enc_ccnum = enc.create_hash(ccnum, salt)
            enc_cvv = enc.create_hash(cvv, salt)

            # Prepare INSERT statement
            prep_insert = "INSERT INTO donations (accId, amount, credCardNum, cvv, credExpMon, credExpYr) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (accid, amt, enc_ccnum, enc_cvv, expm, expy)

            # A tuple should always be used for binding placeholders (%s)
            cursor.execute(prep_insert, values)
        else:
            # Encrypts the Bitcoin address that was entered
            enc_bitcoin = enc.create_hash(bitcoin, salt)

            # Prepare INSERT statement
            prep_insert = (
                "INSERT INTO donations (accId, amount, bitcoin) VALUES (%s, %s, %s)"
            )

            # A tuple should always be used for binding placeholders (%s)
            cursor.execute(prep_insert, (accid, amt, enc_bitcoin))

        db.commit()  # saves changes

    except mysql.Error as e:
        errctr += 1
        msg = "        <p>" + e + "</p>"
        errmsgs.append(msg)


# Intializes an empty list of error messages
errmsgs = []

# Connects to the database
db = connect_db()

cursor = db.cursor(prepared=True)  # allows the prepare statement to be used

errctr = 0  # keeps track of all errors
form = cgi.FieldStorage()

# Account Validation
if not "uname" in form and not "psw" in form:
    errctr += 1
    errmsgs.append("        <p>No account was entered</p>")
else:
    if "uname" in form:
        uname = form.getvalue("uname")
    else:
        uname = ""

    if "psw" in form:
        psw = form.getvalue("psw")
    else:
        psw = ""

    errctr += valid_account(uname, psw)

# Donation Information Validation
if "can" in form and "amt" in form:
    can = form.getvalue("can")
    valid_candidate(can)
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

# Bitcoin Validation
if "sender" in form:
    bitcoin = form.getvalue("sender")
else:
    bitcoin = ""

if bitcoin == "":
    errctr += valid_creditcard(ccnum, cvv, expm, expy)
else:
    errctr += valid_bitcoin(bitcoin)

# Checks if any errors have occured up to this point
if errctr == 0:
    insert_donation()

print("Content-Type: text/html\n")

# HTML code that is always printed
print("<!DOCTYPE html>")
print('<html lang="en">')
print("  <head>")
print("    <title>Donation</title>")
print("    <link rel='stylesheet' href='css/main-styles.css'>")
print("  </head>")
print("  <body>")
print('    <div id="container">')
print('      <div id="content">')

# Checks if any errors occured
if errctr == 0:
    # Printed when a valid donation was placed
    print("         <h1>Thank you for donating!</h1>")
    print("         <p>Your donation was accepted!</p>")
    print('         <a href="index.html">Click here to return to the home page</a>')
else:
    # Printed when invalid donation information is entered
    print("        <h1>Error</h1>")

    # Prints any error messages when errors occur
    for i in range(errctr):
        print(errmsgs[i])

    print('        <a href="donation.html">Click here to fix your mistakes</a>')

# More HTML code that is always printed
print("      </div>")
print("    </div>")
print("  </body>")
print("</html>")