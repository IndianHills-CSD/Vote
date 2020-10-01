#! C:\Python38-32\python.exe -u

import cgi, cgitb, re, hashlib, os, mysql.connector as mysql


def valid_name(fname, lname):
    """
    Checks if a valid firstname and lastname was entered
    """
    global errmsgs
    errors = 0  # keeps track of all the errors that have been

    if len(fname.strip()) == 0:
        errors += 1
        errmsgs.append("        <p>Firstname was not entered</p>")
    elif not fname.isalpha():
        errors += 1
        errmsgs.append("        <p>Firstname should only contain letters</p>")

    if len(lname.strip()) == 0:
        errors += 1
        errmsgs.append("        <p>Lastname was not entered</p>")
    elif not lname.isalpha():
        errors += 1
        errmsgs.append("        <p>Lastname should only contain letters</p>")

    return errors


def valid_age(age):
    """
    Checks if a valid age was entered
    """
    global errmsgs
    errors = 0  # keeps track of all the errors

    if not age.isdigit():
        errors += 1
        errmsgs.append("        <p>Age was not entered</p>")
    elif int(age) < 18 or int(age) > 127:
        errors += 1
        errmsgs.append("         <p>Age should be between 18 and 127</p>")

    return errors


def valid_pol_affil(polaffil):
    """
    Checks if a valid political affiliation was selected
    """
    global errmsgs
    errors = 0  # keeps track of all the errors

    if len(polaffil.strip()) == 0:
        errors += 1
        errmsgs.append("        <p>No politcal party was selected</p>")

    return errors


def valid_address(addr, cty, st, zip):
    """
    Checks if a valid address, city, zip code was entered and checks if a valid state was selected
    """
    global errmsgs
    errors = 0  # keeps track of all errors
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
    global errmsgs
    errors = 0  # keeps track of all the errors
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
    Checks if a valid username and password was entered and checks if the same password was re-entered
    """
    global errmsgs
    errors = 0  # keeps track of all errors

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
    except AttributeError:
        errors += 1
        errmsgs.append("        <p>Username was not entered</p>")

    try:
        wschar = re.search("\s{1,}", psw2)  # checks for any whitespace characters
        digits = re.search("\d{1,}", psw2)  # checks for 1 or more digits

        # Password validation
        if psw1 != psw2:
            errors += 1
            errmsgs.append(
                "        <p>The password that was re-entered does not match the original password that was entered</p>"
            )
        else:
            if len(psw2.strip()) == 0:
                errors += 1
                errmsgs.append("        <p>Password was not entered</p>")
            elif len(psw2.strip()) < 8 or wschar or not digits:
                errors += 1
                errmsgs.append(
                    "        <p>Password should be at least 8 characters long and contain no whitespace characters and at least 1 digit</p>"
                )
    except AttributeError:
        errors += 1
        errmsgs.append("        <p>Password was not entered</p>")

    return errors


# function for MySQL database processing code goes here


cgitb.enable()  # for debugging
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

errctr = valid_name(fname, lname)

# Age Validation
if "age" in form:
    age = form.getvalue("age")
else:
    age = ""

errctr = valid_age(age)

# Political Affiliation Validation
if "polaffil" in form:
    polaffil = form.getvalue("polaffil")
else:
    polaffil = ""

errctr = valid_pol_affil(polaffil)

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

errctr = valid_address(addr, cty, st, zipcode)

# Email Validation
if "email" in form:
    email = form.getvalue("email")
else:
    email = ""

errctr = valid_email(email)

# Username and Password Validation
if "uname" in form:
    uname = form.getvalue("uname")
else:
    uname = ""

if "psw" in form:
    psw = form.getlist("psw")
else:
    psw = ["", ""]

errctr = valid_account(uname, psw[0], psw[1])

print("Content-Type: text/html")

if errctr == 0:
    # Sets the new location (URL) to the login.html page
    print("Location: http://localhost/vote-project/login.html")
    print()

    # call to MySQL database processing function

    # For when the page is being redirecting
    print("<!DOCTYPE html5>")
    print('<html lang="en">')
    print("  <head>")
    print("    <title>Create Account</title>")
    print('    <link rel="stylesheet" href="css/login.css" />')
    print("  </head>")
    print("  <body>")
    print('    <div id="container">')
    print('      <div id="content">')
    print("        <h1>Redirecting...</h1>")
    print(
        '        <a href="login.html">Click here if you are still being redirected</a>'
    )
    print("      </div>")
    print("    </div>")
    print("  </body>")
    print("</html>")
else:
    # Printed when invalid usernames and/or passwords are entered
    print()  # adds a blank line since a blank line needs to follow the Content-Type
    print("<!DOCTYPE html5>")
    print('<html lang="en">')
    print("  <head>")
    print("    <title>Create Account</title>")
    print('    <link rel="stylesheet" href="css/login.css" />')
    print("  </head>")
    print("  <body>")
    print('    <div id="container">')
    print('      <div id="content">')
    print("        <h1>Error</h1>")

    # Prints any error messages when an invalid username or password is entered
    for i in range(len(errmsgs)):
        print(errmsgs[i])

    print('        <a href="create.html">Click here fix your mistakes</a>')
    print("      </div>")
    print("    </div>")
    print("  </body>")
    print("</html>")