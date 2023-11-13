# Instaloader Auxiliar Scripts
* Here, you'll find some scripts that download an Instagram account's posts, stories, etc.

# INSTALLATION

```console
pip install -r requirements.txt
```

# Important
* Instaloader is constantly improving and evolving, and adapting its code to platform changes. This implies that some endpoints may change, and some of the scripts may stop working.

* The objective of this repository is to serve as an example, it has educational purposes, and in no case does it pretend to be perfect or fully functional.

* Please, see: [Instaloader](https://instaloader.github.io/)

# Usage

* Please make sure you don't use a VPN before running the script, because if you use VPN while running the script, this happens;

![Action Blocked](https://github.com/isPique/Instaloader-Scripts/assets/139041426/723a4edf-806b-4e69-85d6-c0c2499db226)

* Anyways. You'll need to set up a few things before running the script.

* Set your own Instagram username and password on `posts.py`, `stories.py` and `highlights.py` (personal account not recommended just create a new account). If you want to download your personal account's saved posts, you can use your personal account on `saved_posts.py`.

* If you get an error like `JSON Query to ANY_USERNAME_HERE/: Could not find "window._sharedData" in html response.` (which will happen with a 99% probability), you can login with your cookies.

* You can follow these steps to login with cookies;

* **1- Login to Instagram**: Login to Instagram in your browser with your username and password.

* **2- Open Developer Tools**: In most web browsers, you can access developer tools by right-clicking on a webpage and selecting "Inspect" or "Inspect Element." Alternatively, you can press F12 or Ctrl+Shift+I to open developer tools.

* **3- Navigate to the Application or Storage Tab**: In the developer tools window, there should be a tab called "Application" or "Storage" (the exact name may vary depending on the browser). Click on it.

* **4- Expand Cookies**: In the Application or Storage tab, you'll find a section for "Cookies" in the left sidebar. Expand this section by clicking on it.

* **5- Find the Cookie for Instagram**: Look for the https://www.instagram.com/ link. Click on it to view the cookies.

* **6- Find the Session ID and CSRF Token**: In the list of cookies you should see one labeled "Session ID" or something similar. The name of the session cookie may vary depending on the website or application you are using. The value of this cookie is your session ID. Likewise, in the list of cookies, you should see one labeled "CSRF Token" or something similar. The value of this cookie is your CSRF (Cross-Site Request Forgery) Token.

* After following all these steps you should see something like this;

![Cookies](https://github.com/isPique/Instaloader-Scripts/assets/139041426/987ffb87-79a1-4978-b0a5-dc1e1d583e7a)

* Set your own **username**, **password**, **Session ID**, **CSRF Token**, and the **username of the person who has the posts you want to download** in the script you intend to use and run the script. You'll see that the posts start to download in the directory where you run the script.

* Additionally, when you run the script, it saves your cookies to a text file named `cookies.txt`. This means you won't need to use your credentials in subsequent runs. The script logs in with the cookie file in second and subsequent executions.

# 

* If you're using the firefox browser, you can use the code below to get the `cookies.txt` file.

```py
from argparse import ArgumentParser
from glob import glob
from os.path import expanduser
from platform import system
from sqlite3 import OperationalError, connect

try:
    from instaloader import ConnectionException, Instaloader
except ModuleNotFoundError:
    raise SystemExit("Instaloader not found.\n  pip install [--user] instaloader")


def get_cookiefile():
    default_cookiefile = {
        "Windows": "~/AppData/Roaming/Mozilla/Firefox/Profiles/*/cookies.sqlite",
        "Darwin": "~/Library/Application Support/Firefox/Profiles/*/cookies.sqlite",
    }.get(system(), "~/.mozilla/firefox/*/cookies.sqlite")
    cookiefiles = glob(expanduser(default_cookiefile))
    if not cookiefiles:
        raise SystemExit("No Firefox cookies.sqlite file found. Use -c COOKIEFILE.")
    return cookiefiles[0]


def import_session(cookiefile, sessionfile):
    print("Using cookies from {}.".format(cookiefile))
    conn = connect(f"file:{cookiefile}?immutable=1", uri=True)
    try:
        cookie_data = conn.execute(
            "SELECT name, value FROM moz_cookies WHERE baseDomain='instagram.com'"
        )
    except OperationalError:
        cookie_data = conn.execute(
            "SELECT name, value FROM moz_cookies WHERE host LIKE '%instagram.com'"
        )
    instaloader = Instaloader(max_connection_attempts=1)
    instaloader.context._session.cookies.update(cookie_data)
    username = instaloader.test_login()
    if not username:
        raise SystemExit("Not logged in. Are you logged in successfully in Firefox?")
    print("Imported session cookie for {}.".format(username))
    instaloader.context.username = username
    instaloader.save_session_to_file(sessionfile)


if __name__ == "__main__":
    p = ArgumentParser()
    p.add_argument("-c", "--cookiefile")
    p.add_argument("-f", "--sessionfile")
    args = p.parse_args()
    try:
        import_session(args.cookiefile or get_cookiefile(), args.sessionfile)
    except (ConnectionException, OperationalError) as e:
        raise SystemExit("Cookie import failed: {}".format(e))
```

* Example usage:
```console
python whatever_you_named_your_file.py --sessionfile "path\to\your\Instaloader Scripts\cookies.txt"
```
# Donations Accepted:

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/ispique)
