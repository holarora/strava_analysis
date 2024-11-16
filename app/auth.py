import webbrowser
import json

from stravalib.client import Client

# Open the secrets file and store the client ID and client secret as objects, separated by a comma
# Read below to learn how to set up the app that provides you with the client ID
# and the client secret
client_id, client_secret = open("client_secrets.txt").read().strip().split(",")

# Create a client object
client = Client()
request_scope = ["read_all", "profile:read_all", "activity:read", "activity:read_all"]

# Create a localhost URL for authorization (for local development)
redirect_url = "http://localhost/authorize"

# Create authorization url; your app client_id required to authorize
url = client.authorization_url(
    client_id=client_id,
    redirect_uri=redirect_url,
    scope=request_scope,
)

# Open the URL in a web browser
webbrowser.open(url)

print(
    """You will see a url that looks like this. """,
    """http://127.0.0.1:5000/authorization?state=&code=12323423423423423423423550&scope=read,activity:read_all,profile:read_all,read_all")""",
    """Copy the values between code= and & in the url that you see in the
 browser. """,
)
# Using input allows you to copy the code into your Python console
# (or Jupyter Notebook)
code = input("Please enter the code that you received: ")
print(
    f"Great! Your code is {code}\n"
    "Next, I will exchange that code for a token.\n"
    "I only have to do this once."
)

# Exchange the code returned from Strava for an access token
token_response = client.exchange_code_for_token(
    client_id=client_id, client_secret=client_secret, code=code
)

token_response
# Example output of token_response
# {'access_token': 'value-here-123123123', 'refresh_token': # '123123123',
# 'expires_at': 1673665980}

# Get current athlete details
athlete = client.get_athlete()
# Print athlete name :) If this works, your connection is successful!
print(f"Hi, {athlete.firstname} Welcome to stravalib!")

# You are now successfully authenticated!
