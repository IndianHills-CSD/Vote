import http.cookies as c, os

# Custom Python module/library for retrieving the value of a cookie called "uname"

def get_cookie():
    """
    Gets the value of the "uname" cookie
    """
    if "HTTP_COOKIE" in os.environ:
        cookie_string = os.environ.get("HTTP_COOKIE")
        cookie = c.SimpleCookie()
        cookie.load(cookie_string)

    try:
        value = cookie["uname"].value
    except Exception:
        value = ""

    return value