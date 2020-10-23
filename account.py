#! C:\Python38-32\python.exe

import mysql.connector as mysql
from connectlib import connect_db
from cookielib import get_cookie


def find_account():
    """
    Searches for a user by using the uname cookie
    """
    uname = get_cookie()  # gets the username of the user

    # Prepare SELECT statements
    prep_select = "SELECT uname, fname, lname, age, addr, city, state, zipCode, poliAffil FROM accounts WHERE uname = %s"

    # A tuple should always be used when binding placeholders (%s)
    cursor.execute(
        prep_select, (uname,)  # you use (value,) when searching for a single value
    )

    result = cursor.fetchall()  # returns a list of tuples

    if result:
        return result[0]
    else:
        return ("", "", "", "", "", "", "", "", "")


# Connects to the database
db = connect_db()

cursor = db.cursor(prepared=True)  # allows the prepare statement to be used
values = find_account()

(
    uname,
    fname,
    lname,
    age,
    addr,
    cty,
    st,
    zipcode,
    polaffil,
) = values  # unpacks the tuple

print("Content-Type: text/html\n")

print("<!DOCTYPE html>")
print('<html lang="en">')
print("  <head>")
print("    <title>Account</title>")
print('    <meta name="viewport" content="width=device-width, initial-scale=1.0">')
print('    <link rel="stylesheet" href="css/main-styles.css" />')
print("  </head>")
print("  <body>")
print('    <div id="container">')
print('      <form name="update" method="post" action="update.py">')
print('        <label class="heading"><b>Account</b></label>\n')
print('        <div class="row">')
print('          <div class="col-25">')
print('            <label for="fname">Firstname</label>')
print('            <input name="fname" type="text" value="' + fname + '"/>')
print("          </div>\n")
print('          <div class="col-25">')
print('            <label for="lname">Lastname</label>')
print('            <input name="lname" type="text" value="' + lname + '" />')
print("          </div>\n")
print('          <div class="col-25">')
print('            <label for="age">Age</label>')
print('            <input name="age" type="number" value="' + str(age) + '" />')
print("          </div>\n")
print('          <div class="col-25">')
print('            <label for="polAffil">Political Affiliation</label>')
print('            <select id="polAffli" name="polaffil">')
print('              <option value=""></option>')

parties = ("Democrat", "Independent", "Republican")

# Loop for printing all political parties
for party in parties:
    if polaffil == party:
        print(
            '              <option value="'
            + party
            + '" selected>'
            + party
            + "</option>"
        )
    else:
        print('              <option value="' + party + '">' + party + "</option>")

# HTML code that is always printed
print("            </select>")
print("          </div>")
print("        </div>\n")
print('        <div class="row">')
print('          <div class="col-25">')
print('            <label for="addr">Address</label>')
print('            <input name="addr" type="text" value="' + addr + '" />')
print("          </div>\n")
print('          <div class="col-25">')
print('            <label for="cty">City</label>')
print('            <input name="cty" type="text" value="' + cty + '" />')
print("          </div>\n")
print('          <div class="col-25">')
print('            <label for="st">State</label>')
print('            <select id="st" name="st">')
print('              <option value=""></option>')

states = (
    "Alabama",
    "Alaska",
    "Arizona",
    "Arkansas",
    "California",
    "Colorado",
    "Connecticut",
    "Delaware",
    "Florida",
    "Georgia",
    "Hawaii",
    "Idaho",
    "Illinois",
    "Indiana",
    "Iowa",
    "Kansas",
    "Louisiana",
    "Maine",
    "Maryland",
    "Massachusetts",
    "Michigan",
    "Minnesota",
    "Mississippi",
    "Missouri",
    "Montana",
    "Nebraska",
    "Nevada",
    "New Hampshire",
    "New Jersey",
    "New Mexico",
    "New York",
    "North Carolina",
    "North Dakota",
    "Ohio",
    "Oklahoma",
    "Pennsylvania",
    "Rhode Island",
    "South Carolina",
    "South Dakota",
    "Tennessee",
    "Utah",
    "Vermont",
    "Virginia",
    "Washington",
    "West Virginia",
    "Wisconsin",
    "Wyoming",
)

# Loop that prints all 50 US states
for state in states:
    if state == st:
        print(
            '              <option value="'
            + state
            + '" selected>'
            + state
            + "</option>"
        )
    else:
        print('              <option value="' + state + '">' + state + "</option>")

# HTML code that is always printed
print("            </select>")
print("          </div>\n")
print('          <div class="col-25">')
print('            <label for="zip">Zip Code</label>')
print('            <input name="zip" type="number" value="' + zipcode + '" />')
print("          </div>")
print("        </div>\n")
print('        <div class="row">')
print('          <div class="col-75">')
print('            <label for="email">Email Address</label>')
print("            <input")
print('              name="email"')
print('              type="email"')
print(
    '              title="Note: You can leave this field and the password fields blank if you wish to not change these fields"'
)
print("            />")
print("          </div>")
print("        </div>\n")
print('        <div class="row">')
print('          <div class="col-25">')
print('            <label for="uname">Username</label>')
print("            <input")
print('              name="uname"')
print('              type="text"')
print('              value="' + uname + '"')
print(
    '              title="Note: Any extra whitespace characters (such as spaces) will be removed"'
)
print("            />")
print("          </div>\n")
print('          <div class="col-25">')
print('            <label for="psw1">Password</label>')
print("            <input")
print('              name="psw1"')
print('              type="password"')
print(
    '              title="Note: Any extra whitespace characters (such as spaces) will be removed"'
)
print("            />")
print("          </div>\n")
print('          <div class="col-25">')
print('            <label for="psw2">Re-Enter Password</label>')
print("            <input")
print('              name="psw2"')
print('              type="password"')
print(
    '              title="Note: Any extra whitespace characters (such as spaces) will be removed"'
)
print("            />")
print("          </div>")
print("        </div>\n")
print('        <div class="row">')
print('          <div class="col-50">')
print('            <input type="submit" value="Update" title="Update" \>\n')
print("          </div>")
print('          <div class="col-50">')
print('            <a href="delete.py" class="delete" title="Delete">Delete</a>\n')
print("          </div>")
print("        </div>\n")
print('        <div class="separate">')
print('          <a href="index.html" class="cancel" title="Cancel">Cancel</a>')
print("        </div>")
print("      </form>")
print("    </div>")
print("  </body>")
print("</html>")