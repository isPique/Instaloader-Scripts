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

user = ""
profile = instaloader.Profile.from_username(instance.context, username = user)

os.makedirs(user, exist_ok = True)
os.chdir(user)

# Get the user's highlights and download them
for highlight in instance.get_highlights(user = profile):
    for item in highlight.get_items():
        instance.download_storyitem(item, '{}/{}'.format(highlight.owner_username, highlight.title))

# Delete unwanted files
def delete_files_with_specific_extensions(folder_path, extensions):
    for root_folder, _, files in os.walk(folder_path):
        for file in files:
            file_extension = file.split(".")[-1]
            if file_extension in extensions:
                file_path = os.path.join(root_folder, file)
                try:
                    os.remove(file_path)
                    print(f"{file_path} deleted.")
                except Exception as e:
                    print(f"Error occurred while deleting {file_path}: {e}")

os.chdir("..")
folder_path = user
extensions = ["xz", "txt", "json"]

delete_files_with_specific_extensions(folder_path, extensions)