#! C:\Python38-32\python.exe -u

import cgi, cgitb, mysql.connector as mysql, encryptionlib as enc, re, os, http.cookies as c
from cookielib import get_cookie
from connectlib import connect_db


def valid_name(fname, lname):
    """
    Checks if a valid firstname and lastname was entered
    """
    errors = 0

    if len(fname.strip()) == 0 or len(lname.strip()) == 0:
        errors += 1
        errmsgs.append("        <p>Name is either incomplete or was not entered</p>")
    elif not fname.isalpha() or not lname.isalpha():
        errors += 1
        errmsgs.append(
            "        <p>The name that was entered should only contain letters</p>"
        )

    return errors


def valid_age(age):
    """
    Checks if a valid age was entered
    """
    errors = 0

    if not age.isdigit():
        errors += 1
        errmsgs.append("        <p>Age was not entered</p>")
    elif int(age) < 18 or int(age) > 120:
        errors += 1
        errmsgs.append("         <p>Age should be between 18 and 120</p>")

    return errors


def valid_pol_affil(polaffil):
    """
    Checks if a valid political affiliation was selected
    """
    errors = 0

    if len(polaffil.strip()) == 0:
        errors += 1
        errmsgs.append("        <p>No politcal party was selected</p>")

    return errors


def valid_address(addr, cty, st, zip):
    """
    Checks if a valid address, city, zip code was entered and checks if a valid state was selected
    """
    errors = 0
    # Regex Pattern for Addresses
    addrformat = re.search(
        "^([\d]{1,3}[\s][A-Z|a-z|\d](([\d|\s|A-Z|a-z])?){1,})$", addr
    )
    # Regex Pattern for Cities
    ctyformat = re.search("^([A-Z|a-z]{1,}([\s][A-Z|a-z]{1,})?)$", cty)

    if len(addr.strip()) == 0:
        errors += 1
        errmsgs.append("        <p>Address was not entered</p>")
    else:
        if not addrformat:
            errors += 1
            errmsgs.append(
                "        <p>Address is not in the correct format, it should looke something like this: 123 North Street</p>"
            )

    if len(cty.strip()) == 0:
        errors += 1
        errmsgs.append("        <p>City was not entered</p>")
    if not ctyformat:
        errors += 1
        errmsgs.append("        <p>City should only contain letters and spaces</p>")

    if len(st.strip()) == 0:
        errors += 1
        errmsgs.append("        <p>No state was selected</p>")

    if not zipcode.isdigit():
        errors += 1
        errmsgs.append("        <p>Zip code should only contain digits</p>")
    elif int(zipcode) < 10000 or int(zipcode) > 99999:
        errors += 1
        errmsgs.append("        <p>Zip code should be only 5 digits long</p>")

    return errors


def valid_email(email):
    """
    Checks if a valid email was entered
    """
    errors = 0
    # Regex Pattern for Emails
    emailformat = re.search("^([\S]{1,}[@][\w]{4,}[\.][a-z]{2,4})$", email)

    if len(email.strip()) == 0:
        errors += 1
        errmsgs.append("        <p>Email was not entered</p>")
    elif not emailformat:
        errors += 1
        errmsgs.append(
            "        <p>Email is not in the correct format, it should look something like this: example@gmail.com</p>"
        )
    return errors


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
            "        <p>Password should be at least 8 characters long, contain no whitespace characters, and contain at least 1 digit</p>"
        )
        val_psws = False

    if val_psws:
        if psw1.strip() != psw2.strip():
            errors += 1
            errmsgs.append(
                "        <p>The password that was re-entered does not match the original password that was entered</p>"
            )

    return errors


def select_account():
    """
    Checks if an account that was entered contains any new data
    """
    errors = 0
    enc_repeat = (
        False  # used to determine if the same email and/or password was re-entered
    )

    try:
        enc_values = find_encdata()
        salt = eval(
            find_salt()  # converts the salt that is returned from find_salt() back to bytes
        )
        (enc_psw, enc_email) = enc_values

        if enc.verify_hash(enc_psw, psw1, salt) or enc.verify_hash(
            enc_email, email, salt
        ):
            enc_repeat = True

        # Prepare SELECT statement
        prep_select = "SELECT * FROM accounts WHERE uname = %s AND fname = %s AND lname = %s AND age = %s AND addr = %s AND city = %s AND state = %s AND zipCode = %s AND poliAffil = %s"

        values = (
            uname,
            fname,
            lname,
            age,
            addr,
            cty,
            st,
            zipcode,
            polaffil,
        )

        # A tuple should always be used when binding placeholders (%s)
        cursor.execute(prep_select, values)

        result = cursor.fetchall()  # returns a list of tuples

        if not result or not enc_repeat:
            update_account()
        else:
            errors += 1
            errmsgs.append("        <p>Account did not change</p>")

    except mysql.Error as e:
        errors += 1
        msg = "        <p>" + str(e) + "</p>"
        errmsgs.append(msg)

    return errors


def find_encdata():
    """
    Searches the Accounts table for the user's encrypted password and email address
    """
    uname_cookie = get_cookie()  # gets the value of the "uname" cookie

    # Prepare SELECT statement
    prep_select = "SELECT pwd, email FROM accounts WHERE uname = %s"

    # A tuple should always be used when binding placeholders (%s)
    cursor.execute(
        prep_select, (uname,)  # you use (value,) when searching for a single value
    )

    result = cursor.fetchall()  # returns a list of tuples

    if result:
        return result[0]
    else:
        return ("", "")


def find_salt():
    """
    Determines which salt to use for verifying passwords and email addresses
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


def update_account():
    """
    Used to update accounts
    """
    global errctr
    accid = find_accid()  # gets an id

    # Prepare UPDATE statement
    prep_update = "UPDATE accounts SET uname = %s, pwd = %s, fname = %s, lname = %s, email = %s, age = %s, addr = %s, city = %s, state = %s, zipCode = %s, poliAffil = %s WHERE accId = %s"

    salt = os.urandom(64)

    enc_psw = enc.create_hash(psw1, salt)
    enc_email = enc.create_hash(email, salt)

    values = (
        uname,
        enc_psw,
        fname,
        lname,
        enc_email,
        age,
        addr,
        cty,
        st,
        zipcode,
        polaffil,
        accid,
    )

    # A tuple should always be used when binding placeholders (%s)
    cursor.execute(prep_update, values)

    update_salt(salt, accid)

    db.commit()  # saves changes


def update_salt(salt, accid):
    """
    Updates the salt value that is used to encrypt data using the prepare statement
    """
    # Prepare INSERT statement
    prep_update = "UPDATE salt SET salt = %s WHERE accId = %s"

    cursor.execute(prep_update, (str(salt), accid))

    db.commit()  # saves changes


cgitb.enable()  # for debugging

# Connects to the database
db = connect_db()

cursor = db.cursor(prepared=True)  # allows the prepare statement to be used

errctr = 0  # keeps track of all the errors that were found

# Intializes an empty list of error messages
errmsgs = []

form = cgi.FieldStorage()

# Name Validation
if "fname" in form:
    fname = form.getvalue("fname")
else:
    fname = ""

if "lname" in form:
    lname = form.getvalue("lname")
else:
    lname = ""

errctr += valid_name(fname, lname)

# Age Validation
if "age" in form:
    age = form.getvalue("age")
else:
    age = ""

errctr += valid_age(age)

# Political Affiliation Validation
if "polaffil" in form:
    polaffil = form.getvalue("polaffil")
else:
    polaffil = ""

errctr += valid_pol_affil(polaffil)

# Address, City, State, and Zip Code Validation
if "addr" in form:
    addr = form.getvalue("addr")
else:
    addr = ""

if "cty" in form:
    cty = form.getvalue("cty")
else:
    cty = ""

if "st" in form:
    st = form.getvalue("st")
else:
    st = ""

if "zip" in form:
    zipcode = form.getvalue("zip")
else:
    zipcode = ""

errctr += valid_address(addr, cty, st, zipcode)

# Email Validation
if "email" in form:
    email = form.getvalue("email")
else:
    email = ""

errctr += valid_email(email)

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

# Determines if select_account() should be called
if errctr == 0:
    # Checks if the account that was entered is already exists
    errctr += select_account()

    uname_cookie = get_cookie()  # gets the original "username"

    # Sets the "uname" cookie to a new value if a new username was submitted
    if uname_cookie != uname:
        uname_cookie = c.SimpleCookie()  # resets the cookie
        uname_cookie["uname"] = uname
        print(uname_cookie)  # prints Set-Cookie: uname=value

print("Content-Type: text/html\n")

# HTML code that is always printed
print("<!DOCTYPE html>")
print('<html lang="en">')
print("  <head>")
print("    <title>Update Account</title>")
print('    <link rel="stylesheet" href="css/main-styles.css" />')
print("  </head>")
print("  <body>")
print('    <div id="container">')
print('      <div id="content">')

# Checks if any errors occured
if errctr == 0:
    print("        <h1>Account was updated!</h1>")
    print("        <p>Your account has been successfully updated!</p>")
    print('        <a href="index.html">Click here to return to the Home page</a>')
else:
    print("        <h1>Error</h1>")

    # Prints any error messages when errors occur
    for i in range(errctr):
        print(errmsgs[i])

    print('        <a href="account.py">Click here to fix your mistakes</a>')

# More HTML code that is always printed
print("  </body>")
print("</html>")