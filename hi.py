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
    code="03bdba3978f93773b236c2892ae65f76a9aff43c"
)

print(token_response)