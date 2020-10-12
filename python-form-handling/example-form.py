#! C:\Python38-32\python.exe -u
# The content above is called "shebang" which is used to determine which python.exe file to use

"""
Use this page as an example of how to create the Account page
"""

import mysql.connector as mysql, http.cookies as c, os

# Read cookie
def get_cookie():
    """
    Gets the value of the cookie
    """
    if "HTTP_COOKIE" in os.environ:
        cookie_string = os.environ.get("HTTP_COOKIE")
        cookie = c.SimpleCookie()
        cookie.load(cookie_string)

    try:
        val = cookie["data"].value
    except Exception:
        val = ""

    return val


data = get_cookie()


# Ensures that the code that is printed below is treated as HTML code
print(
    "Content-Type: text/html\n"  # should have a blank line after the Content-Type is printed
)

# Prints the HTML code
print("<!DOCTYPE html>")
print('<html lang="en">')
print("  <head>")
print("    <title>Example Python HTML Page</title>")
print("  </head>")
print("  <body>")
print("    <h1>Form Handling Example</h1>")
print('    <form name="example" action="example-handling.py">')
print('      <label for="data">Enter Some Text</label><br>')
print('      <input type="text" name="data" value="' + data + '" />')
print("    </form>")
print("  </body>")
print("</html>")