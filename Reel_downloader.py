import getpass
import instaloader

# Create instaloader instance
L = instaloader.Instaloader()

# OPTIONAL: Login (needed to download private profile you follow)
# Ask for username first so we can try loading browser session
username = input("Enter Instagram username: ")

try:
    L.load_session_from_browser(username)
    print("Loaded login session from your browser!")
except Exception as e:
    print("Failed to load browser session:", e)
    # Fallback: manual login
    password = getpass.getpass("Enter Instagram password: ")
    try:
        L.login(username, password)
        print("Login successful!")
    except Exception as e2:
        print("Login failed:", e2)
        exit()

profile_name = "example_profile"  # Replace with the target profile name

# Load profile
profile = instaloader.Profile.from_username(L.context, profile_name)

print(f"Downloading Reels from @{profile_name}...")

for post in profile.get_posts():
    if post.is_video and post.typename == "GraphVideo":
        if post.caption and ("#reels" in post.caption.lower() or "reel" in post.caption.lower()):
            L.download_post(post, target=f"{profile_name}_reels")

    # Or simpler: if post is reel format
    if post.typename == "GraphVideo" and post.is_video and post.video_url:
        L.download_post(post, target=f"{profile_name}_reels")

print("Download completed.")

# Note: Ensure you have instaloader installed: pip install instaloader