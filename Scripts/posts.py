import instaloader
import os

instance = instaloader.Instaloader()

# Personal account is not recommended. To use it, simply create a new account.
username = "YOUR INSTAGRAM USERNAME HERE"
password = "YOUR INSTAGRAM PASSWORD HERE"

instance.compress_json = False

# Check if you have a session file to load, if not, login using credentials
try:
    instance.load_session_from_file(username, "cookies.txt")

except FileNotFoundError:
    try:
        instance.login(username, password)

    except:
        # If login fails, load the session using sessionid and csrftoken (not recommended if you use VPN)
        instance.load_session(username, {"sessionid": "YOUR SESSION ID HERE", "csrftoken": "YOUR CSRFTOKEN HERE"})

# Save the session to a file for future use
instance.save_session_to_file("cookies.txt")

if instance.context.is_logged_in:
    print(f"Logged as {username}")

else:
    print("An error occurred while logging into the account.")

while True:
    username = input("Enter any username you want: ")
    print("The account you are looking for is being searched in Instagram's database..")

    try:
        try:
            profile = instaloader.Profile.from_username(instance.context, username)
            if profile and profile.mediacount > 0:
                print("Account found. Downloading posts.. ")
                instance.download_profile(username)
                print("The download process has been completed.")

                # Delete unwanted files
                for root, dirs, files in os.walk(username):
                    for file in files:
                        if file.endswith((".xz", ".txt", ".json")):
                            os.remove(os.path.join(root, file))
                            print(f"Deleting: {file}")

            elif profile and profile.mediacount == 0:
                print("There are no posts in the account you are looking for.")

        except instaloader.exceptions.PrivateProfileNotFollowedException:
            print("This is a private account. You need to follow it to access its posts.")

    except instaloader.exceptions.ProfileNotExistsException:
        print("The account you are looking for is not exists on instagram. Try another username")