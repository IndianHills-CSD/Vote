#! C:\Python38-32\python.exe -u
# The content above is called "shebang" which is used to determine which python.exe file to use

"""
Use this page as an example of how to create a form handler page
"""

import cgi, cgitb, http.cookies as c

cgitb.enable()  # used for debugging

# Gets all the data that was submitted
form = cgi.FieldStorage()

cookie = c.SimpleCookie()
if form.getvalue("data") != None:
    cookie["data"] = form.getvalue("data")
print(cookie["data"])

# Ensures that the code that is printed is treated as HTML code
print(
    "Content-Type: text/html\n"  # should have a blank line after the Content-Type is printed
)

# Prints the HTML code
print("<!DOCTYPE html>")
print('<html lang="en">')
print("  <head>")
print("    <title>Python Form Handling Example</title>")
print("  </head>")
print("  <body>")

# Uses the name attribute to identify if "data" contains any values when submitted
if "data" in form:
    data = form.getvalue(
        "data"  # sets the variable "data" to the data that was submitted
    )
    print("    <p>You submitted <b>" + data + "</b>!!</p>")
else:
    print("    <h1>Error</h1>")
    print("    <p>No data was entered</p>")

print('    <a href="example-form.py">Return</a>')
print("  </body>")
print("</html>")