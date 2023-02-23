from flask import Flask
app = Flask(__name__)
app.secret_key = "secret"
DB = "bid_my_ride_schema"