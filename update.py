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
                '        <div class="center">\n\t\t  <p>Address is not in the correct format, it should looke something like this: 123 North Street</p>\n\t\t  </div>'
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
    elif len(zipcode) != 5:
        errors += 1
        errmsgs.append("        <p>Zip code should be 5 digits long</p>")

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
    val_psws = True  # determines if psw1 and psw2 should be checked for equality

    if len(psw1.strip()) == 0 or len(psw2.strip()) == 0:
        errors += 1
        errmsgs.append(
            '       <div class="center">\n\t\t  <p>Password was either not entered at all or not re-entered</p>\n\t\t  </div>'
        )
        val_psws = False
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


def valid_username(uname):
    """
    Checks if a valid username was entered
    """
    errors = 0  # keeps track of all errors

    if len(uname.strip()) == 0:
        errors += 1
        errmsgs.append("        <p>Username was not entered</p>")
    elif len(uname.strip()) < 4:
        errors += 1
        errmsgs.append("        <p>Username should be at least 4 characters long</p>")

    return errors


def select_account():
    """
    Checks if an account that was entered contains any new data
    """
    errors = 0
    # Determines if the same password or email was re-entered
    enc_repeat = False

    try:
        enc_values = find_encdata()  # returns a tuple
        (enc_psw, enc_email) = enc_values  # unpacks the tuple
        salt = eval(
            find_salt()  # converts the salt that is returned from find_salt() back to bytes
        )

        # Checks if the user decided to reuse a password or email address
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
        elif enc_repeat:
            errors += 1
            errmsgs.append(
                "        <p>A new password and/or email should be entered</p>"
            )
        else:
            errors += 1
            errmsgs.append("        <p>New information needs to be entered</p>")

    except mysql.Error as e:
        errors += 1
        msg = "        <p>" + str(e) + "</p>"
        errmsgs.append(msg)

    return errors


def find_encdata():
    """
    Searches the Accounts table for the user's encrypted password and email address
    """
    # The "uname" cookie is used in order to ensure that the original username is always used
    uname_cookie = get_cookie()  # gets the value of the "uname" cookie

    # Prepare SELECT statement
    prep_select = "SELECT pwd, email FROM accounts WHERE uname = %s"

    # A tuple should always be used when binding placeholders (%s)
    cursor.execute(
        prep_select,
        (uname_cookie,),  # you use (value,) when searching for a single value
    )

    result = cursor.fetchall()  # returns a list of tuples

    if result:
        return result[0]
    else:
        return ("", "")


def check_donations():
    """
    Checks if the user donated to any candidates
    """
    # The "uname" cookie is used in order to ensure that the original username is always used
    uname_cookie = get_cookie()  # gets the value of the "uname" cookie

    # Prepare SELECT statement
    prep_select = (
        "SELECT credCardNum, cvv FROM donations NATURAL JOIN accounts WHERE uname = %s"
    )

    # A tuple should always be used when binding placeholders (%s)
    cursor.execute(
        prep_select,
        (uname_cookie,),  # you use (value,) when searching for a single value
    )

    result = cursor.fetchall()  # returns a list of tuples

    if result:
        return True
    else:
        return False


def find_salt():
    """
    Determines which salt to use for verifying passwords and email addresses
    """
    salt = ""  # used to return nothing if no salt is found

    accid = find_accid()  # gets an ID

    # Prepare SELECT statement
    prep_select = "SELECT salt FROM salt WHERE accId = %s"

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
    # The "uname" cookie is used in order to ensure that the original username is always used
    uname_cookie = get_cookie()  # gets the value of the "uname" cookie
    accid = 0

    # Prepare SELECT statement
    prep_select = "SELECT accId FROM accounts WHERE uname = %s"

    # A tuple should always be used to bind placeholders
    cursor.execute(prep_select, (uname_cookie,))
    result = cursor.fetchall()  # returns a list of tuples

    if result:
        # Should only return one row
        (val_accid,) = result[0]  # unpacks the tuple
        accid = val_accid

    return accid


def update_account():
    """
    Updates accounts using the prepare statement
    """
    # Determines if the salt used by an account in the Salt table should be updated
    new_salt = False
    accid = find_accid()  # gets an ID

    # Gets the original encrypted values to use for defaulting data
    enc_values = find_encdata()  # returns a tuple
    (pwd, email_addr) = enc_values  # unpacks the tuple

    # Checks if the password and email address that were submitted should be encrypted
    if psw1 != "" or email != "":
        salt = os.urandom(64)  # generates a new salt value
        new_salt = True

        if psw1 != "":
            enc_psw = enc.create_hash(psw1, salt)
        else:
            # Re-encrypts data so validation still works
            enc_psw = enc.create_hash(pwd, salt)

        if email != "":
            enc_email = enc.create_hash(email, salt)
        else:
            # Re-encrypts data so validation still works
            enc_email = enc.create_hash(email_addr, salt)
    else:
        enc_psw = pwd
        enc_email = email_addr

    # Prepare UPDATE statement
    prep_update = "UPDATE accounts SET uname = %s, pwd = %s, fname = %s, lname = %s, email = %s, age = %s, addr = %s, city = %s, state = %s, zipCode = %s, poliAffil = %s WHERE accId = %s"

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

    if new_salt:
        update_salt(salt, accid)

    db.commit()  # saves changes


def update_salt(salt, accid):
    """
    Updates the salt value that is used to encrypt data using the prepare statement
    """
    # Prepare UPDATE statement
    prep_update = "UPDATE salt SET salt = %s, updated = %s WHERE accId = %s"

    cursor.execute(prep_update, (str(salt), "Y", accid))


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
    errctr += valid_email(email)
else:
    email = ""

# Username and Password Validation
if "uname" in form:
    uname = form.getvalue("uname")
else:
    uname = ""

# Sets default values
psw1 = ""
psw2 = ""

if "psw1" in form or "psw2" in form:
    if "psw1" in form:
        psw1 = form.getvalue("psw1")

    if "psw2" in form:
        psw2 = form.getvalue("psw2")

    errctr += valid_account(uname, psw1, psw2)
else:
    errctr += valid_username(uname)

# Determines if select_account() should be called
if errctr == 0:
    # Checks if the account that was entered already exists
    errctr += select_account()
    uname_cookie = get_cookie()  # gets the original username that was used

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

# Checks if any errors occurred
if errctr == 0:
    print("        <h1>Account was updated!</h1>")
    print("        <p>Your account has been successfully updated!</p>")
    print('        <a href="index.html">Click here to return to the Home page</a>')
else:
    print("        <h1>Error</h1>")

    # Loop that prints every error message in the "errmsgs" list
    for i in range(errctr):
        print(errmsgs[i])

    print('        <a href="account.py">Click here to fix your mistakes</a>')

# More HTML code that is always printed
print("  </body>")
print("</html>")