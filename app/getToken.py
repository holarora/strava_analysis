import webbrowser
from flask import Flask, request, redirect
from stravalib.client import Client

client_id, client_secret = open("client_secrets.txt").read().strip().split(",")
request_scope = ["read_all", "profile:read_all", "activity:read_all"]

# Create a client object
client = Client()

token_response = client.exchange_code_for_token(
    client_id="139704",
    client_secret="00af07ae180e7e0e43df54c3043b4cf2efc0b2c9",
    code="4d3450b3c88711c61a756cf088bc2544a07ed073" // paste token here
)

print(token_response)