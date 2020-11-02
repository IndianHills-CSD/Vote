#! C:\Python38-32\python.exe -u

import cgi, cgitb, re, encryptionlib as enc, os, mysql.connector as mysql, datetime as date
from connectlib import connect_db
from bitcoinlib import check_bc
from cookielib import get_cookie


def valid_account(uname, psw):
    """
    Checks if a valid username and password was entered
    """
    errors = 0

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

    except mysql.Error as e:
        errors += 1
        errmsgs.append("<p>" + str(e) + "</p>")

    return errors


def verify_account(uname, psw):
    """
    Checks if the account entered is the current account that is being used and calls a function for
    searching for the account that was entered in the database
    """
    errors = 0  # keeps track of all the errors that have been found
    val_uname = get_cookie()  # gets the username the user logged in with

    if val_uname != uname:
        errors += 1
        errmsgs.append(
            "        <p>The username that was entered doesn't match the one that is currently being used</p>"
        )
    else:
        errors += select_account(uname, psw)

    return errors


def select_account(uname, psw):
    """
    Verifies the username and password that was entered using a prepare statement
    """
    errors = 0  # keeps track of all the errors that have occurred

    # Prepare SELECT statement
    prep_select = "SELECT pwd FROM accounts WHERE uname = %s"

    # A tuple should always be used for binding placeholders (%s)
    cursor.execute(
        prep_select, (uname,)  # you write (value,) when searching for one value
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

        # Checks if the password that was entered is incorrect
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
    prep_select = "SELECT salt FROM salt WHERE accId = %s"

    accid = find_accid()

    # A tuple should always be used for binding placeholders (%s)
    cursor.execute(
        prep_select, (accid,)  # you write (value,) when searching for one value
    )

    result = cursor.fetchall()  # returns a list of tuples

    if result:
        (val_salt,) = result[0]  # unpacks the tuple
        salt = val_salt

    return salt


def find_accid():
    """
    Finds the ID of an account for the Salt, Donations, and VoteDonate tables
    """
    accid = 0

    # Prepare SELECT statement
    prep_select = "SELECT accId FROM accounts WHERE uname = %s"

    # A tuple should always be used for binding placeholders (%s)
    cursor.execute(
        prep_select, (uname,)  # you write (value,) when searching for one value
    )

    result = cursor.fetchall()  # returns a list of tuples

    if result:
        (val_id,) = result[0]  # unpacks the tuple
        accid = val_id

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
    elif len(cvv) != 3:
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

    # Determines if verify_creditcard() should be called
    if errors == 0:
        errors += verify_creditcard(ccnum, cvv)

    return errors


def verify_creditcard(ccnum, cvv):
    """
    Checks if a similar credit card has been used by a previous user
    """
    errors = 0  # keeps track of all the errors that have been found
    accid = find_accid()  # gets an ID

    try:
        # Prepare SELECT statement
        # Note: MySQL uses "!=" and "<>" as not equal operators
        prep_select = "SELECT DISTINCT credCardNum, cvv, salt FROM donations NATURAL JOIN accounts NATURAL JOIN salt WHERE accId != %s AND credCardNum IS NOT NULL AND cvv IS NOT NULL"

        # A tuple should always be used for binding placeholders (%s)
        cursor.execute(
            prep_select, (accid,)  # you write (value,) when searching for one value
        )

        results = cursor.fetchall()  # returns a list of tuples

        if results:
            # Loops thru the tuples in the list
            for i in range(len(results)):
                # Unpacks a tuple in the list
                (enc_ccnum, enc_cvv, str_salt) = results[i]

                # Converts the value of str_salt back to bytes
                salt = eval(str_salt)

                # Checks if the data that was entered is used by another user
                if enc.verify_hash(enc_ccnum, ccnum, salt) and enc.verify_hash(
                    enc_cvv, cvv, salt
                ):
                    errors += 1
                    errmsgs.append(
                        "        <p>This credit card contains information that is too similar to another user's credit card information</p>"
                    )
                    break

            # Determines if cred_needs_updated() should be called
            if errors == 0:
                cred_needs_updated(ccnum, cvv, salt)

    except Exception as e:
        errors += 1
        msg = "        <p>" + str(e) + "</p>"
        errmsgs.append(msg)

    return errors


def cred_needs_updated(ccnum, cvv, salt):
    """
    Determines if the credit card number and CVV for this user's credit card should be re-encrypted
    """
    accid = find_accid()  # gets an ID
    updated = True  # used to determine if the credit card number and CVV needs to be re-encrypted

    # Prepare SELECT statement
    prep_select = "SELECT DISTINCT credCardNum, cvv, salt, updated FROM donations NATURAL JOIN accounts NATURAL JOIN salt WHERE accId = %s AND credCardNum IS NOT NULL AND cvv IS NOT NULL"

    # A tuple should always be used for binding placeholders (%s)
    cursor.execute(
        prep_select, (accid,)  # you write (value,) when searching for one value
    )

    results = cursor.fetchall()  # returns a list of tuples

    if results:
        (enc_ccnum, enc_cvv, str_salt, update) = results[0]  # unpacks the tuple

        # Converts the value of str_salt back to bytes
        salt = eval(str_salt)

        # Checks if the data that was entered should be re-encrypted
        if update == "Y":
            if enc.verify_hash(enc_ccnum, ccnum, salt) and enc.verify_hash(
                enc_cvv, cvv, salt
            ):
                updated = False

        if updated:
            update_cred(ccnum, cvv, salt)


def update_cred(ccnum, cvv, salt):
    """
    Re-Encrypts the credit card number and CVV that was entered
    """
    accid = find_accid()  # gets an ID

    # Encrypts the credit card number and the CVV
    enc_ccnum = enc.create_hash(ccnum, salt)
    enc_cvv = enc.create_hash(cvv, salt)

    # Prepare UPDATE statement
    prep_update = "UPDATE donations SET credCardNum = %s, cvv = %s WHERE accId = %s"

    # A tuple should always be used when binding placeholders (%s)
    cursor.execute(prep_update, (enc_ccnum, enc_cvv, accid))

    db.commit()  # saves changes


def valid_bitcoin(bitcoin):
    """
    Verifies the bitcoin that was entered
    """
    errors = 0  # keeps track of all the errors that have been found

    if bitcoin == "17wR7WdrmLH6R387xeA3ahYCo91Up9A34T":
        errors += 1
        errmsgs.append(
            "        <p>The Bitcoin that was entered should not match the recipient's Bitcoin</p>"
        )
    else:
        if not check_bc(bitcoin):
            errors += 1
            errmsgs.append("        <p>The Bitcoin that was entered is invalid</p>")

    if errors == 0:
        errors += verify_bitcoin(bitcoin)

    return errors


def verify_bitcoin(bitcoin):
    """
    Checks if the bitcoin address that was entered has been used before
    """
    errors = 0  # keeps track of all the errors that have been found
    accid = find_accid()  # gets an ID

    try:
        # Prepare SELECT statement
        # Note: MySQL uses "!=" and "<>" as not equal operators
        prep_select = "SELECT DISTINCT bitcoin, salt FROM donations NATURAL JOIN accounts NATURAL JOIN salt WHERE accId != %s"

        # A tuple should always be used when binding placeholders (%s)
        cursor.execute(
            prep_select, (accid,)  # you use (value,) when searching for a single value
        )

        results = cursor.fetchall()  # returns a list of tuples

        if results:
            # Loops thru the tuples in the list
            for i in range(len(results)):
                (enc_bitcoin, str_salt) = results[i]  # unpacks a tuple in the list

                # Converts the value of str_salt back to bytes
                salt = eval(str_salt)

                # Checks if the data that was entered is used by another user
                if enc.verify_hash(enc_bitcoin, bitcoin, salt):
                    errors += 1
                    errmsgs.append(
                        "        <p>This Bitcoin address is too similar to another user's Bitcoin address</p>"
                    )
                    break

    except mysql.Error as e:
        errors += 1
        msg = "        <p>" + str(e) + "</p>"
        errmsgs.append(msg)

    return errors


def bitaddr_needs_updated(bitcoin):
    """
    Determines if the bitcoin address used by this user should be re-encrypted
    """
    update = True  # used to determine if the bitcoin address needs to be re-encrypted
    accid = find_accid()  # gets an ID

    # Prepare SELECT statement
    prep_select = "SELECT DISTINCT bitcoin, salt, updated FROM donations NATURAL JOIN accounts NATURAL JOIN salt WHERE accId = %s AND credCardNum IS NOT NULL AND cvv IS NOT NULL"

    # A tuple should always be used for binding placeholders (%s)
    cursor.execute(
        prep_select, (accid,)  # you write (value,) when searching for one value
    )

    results = cursor.fetchall()  # returns a list of tuples

    if results:
        (enc_bitcoin, str_salt, update) = results[0]  # unpacks the tuple

        # Converts the value of str_salt back to bytes
        salt = eval(str_salt)

        # Checks if the data that was entered should be re-encrypted
        if update == "Y":
            if enc.verify_hash(enc_bitcoin, bitcoin, salt):
                update = False

        if update:
            update_bitaddr(bitcoin, salt)


def update_bitaddr(bitcoin, salt):
    """
    Re-Encrypts the bitcoin address that was entered
    """
    accid = find_accid()  # gets an ID

    # Encrypts the credit card number and the CVV
    enc_bitcoin = enc.create_hash(bitcoin, salt)

    # Prepare UPDATE statement
    prep_update = "UPDATE donations SET bitcoin = %s WHERE accId = %s"

    # A tuple should always be used when binding placeholders (%s)
    cursor.execute(prep_update, (enc_bitcoin, accid))

    db.commit()  # saves changes


def insert_donation():
    """
    Stores the donation that was placed in the Donations table and uses a function to store donations
    in the VoteDonate table
    """
    global errctr
    accid = find_accid()  # gets an ID

    try:
        # Converts the string value that is returned in find_salt() back to bytes
        salt = eval(find_salt())

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

        insert_votedonate()

    except mysql.Error as e:
        errctr += 1
        msg = "        <p>" + str(e) + "</p>"
        errmsgs.append(msg)


def insert_votedonate():
    """
    Stores extra donation information in the VoteDonate table
    """
    voteid = find_voteid()  # gets IDs (foriegn keys)
    donatid = find_donatid()

    donatdate = date.date.today().strftime("%Y-%m-%d")  # gets the current date

    # Prepare INSERT statement
    prep_insert = (
        "INSERT INTO voteDonate (voteId, donatId, donatDate) VALUES (%s, %s, %s)"
    )

    # A tuple should always be used for binding placeholders (%s)
    cursor.execute(prep_insert, (voteid, donatid, donatdate))

    db.commit()  # saves changes


def find_voteid():
    """
    Retrieves the ID of the candidate that a donation was placed for
    """
    voteid = 0  # returns "0" when no ID is found
    accid = find_accid()
    voted = voted_can(accid)

    # Checks which SELECT statement should be used
    if voted:
        # Prepare SELECT statement with accid
        prep_select = "SELECT voteId FROM votes WHERE candidate = %s AND accId = %s"

        # A tuple should always be used when binding placeholders (%s)
        cursor.execute(prep_select, (can, accid))
    else:
        # Prepare SELECT statement without accid
        prep_select = "SELECT voteId FROM votes WHERE candidate = %s AND accId IS NULL"

        # A tuple should always be used when binding placeholders (%s)
        cursor.execute(
            prep_select, (can,)  # you use (value,) when searching for a single value
        )

    result = cursor.fetchall()  # returns a list of tuples

    if result:
        if len(result) == 1:
            (val_id,) = result[0]  # unpacks the tuple
        elif len(result) > 1:
            last = len(result) - 1  # calculates the index of the last tuple in the list
            (val_id,) = result[last]  # unpacks the last tuple in the list

        voteid = val_id

    return voteid


def voted_can(accid):
    """
    Checks if users donated to a candidate they did not vote for
    """
    # Prepare SELECT statement
    prep_select = "SELECT accId FROM accounts NATURAL JOIN votes WHERE accId = %s and candidate = %s"

    cursor.execute(prep_select, (accid, can))

    results = cursor.fetchall()

    if not results:
        insert_no_vote()
        return False
    else:
        return True


def insert_no_vote():
    """ "
    Inserts a row with no foriegn key (accId) to represent that a user donated to a candidate but
    didn't vote for them
    """
    prep_insert = "INSERT INTO votes (candidate, polParty) VALUES (%s, %s)"
    party = find_party()

    cursor.execute(prep_insert, (can, party))

    db.commit()  # saves changes


def find_party():
    """
    Finds the political party of a candidate
    """
    party = ""  # returns an empty string ("") when not found

    # Prepare SELECT statement
    prep_select = "SELECT polParty FROM votes WHERE candidate = %s"

    cursor.execute(prep_select, (can,))
    result = cursor.fetchall()

    if result:
        (polparty,) = result[0]
        party = polparty

    return party


def find_donatid():
    """
    Retrieves the ID of the donation that was placed
    """
    donatid = 0  # returns "0" when no ID is found
    accid = find_accid()

    # Prepare SELECT statement
    prep_select = "SELECT donatId FROM donations WHERE accId = %s"

    # A tuple should always be used when binding placeholders (%s)
    cursor.execute(
        prep_select, (accid,)  # you use (value,) when searching for a single value
    )

    result = cursor.fetchall()  # returns a list of tuples

    if len(result) == 1:
        (val_id,) = result[0]  # unpacks the tuple
    elif len(result) > 1:
        last = len(result) - 1  # calculates the index of the last tuple in the list
        (val_id,) = result[last]  # unpacks the last tuple in the list

    donatid = val_id

    return donatid


# Intializes an empty list of error messages
errmsgs = []

# Connects to the database
db = connect_db()

cursor = db.cursor(prepared=True)  # allows the prepare statement to be used

errctr = 0  # keeps track of all errors
form = cgi.FieldStorage()

# Account Validation
if "uname" not in form and "psw" not in form:
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
    errmsgs.append("        <p>A donation was not placed for any candidate</p>")


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
    print('         <a href="index.html">Click here to return to the Home page</a>')
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