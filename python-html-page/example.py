#! C:\Python38-32\python.exe -u

# Use this page as an example of how to create the Account page

import cgi, cgitb

cgitb.enable()  # used for debugging

# Ensures that the code that is printed is treated as HTML code
print(
    "Content-Type: text/html\n"  # should have a blank line after the Content-Type is printed
)

print("<!DOCTYPE html>")
print('<html lang="en">')
print("  <head>")
print("    <title>Example Python HTML Page</title>")
print("  </head>")
print("  <body>")
print("    <h1>Heading</h1>")
print("    <p>Text</p>")
print("  </body>")
print("</html>")