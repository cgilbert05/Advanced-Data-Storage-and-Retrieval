import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify, json

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

## precipitation
rain_query = session.query(Measurement.date, Measurement.prcp).all()

rainfall = []

for row in rain_query:
    rainfall.append(row)

rainfall_df = pd.DataFrame(rainfall)
rainfall_df.columns = ['date', 'prcp']
rainfall_df = rainfall_df.iloc[0:]
precipitation = rainfall_df.to_json(orient='records')

## station_list 
station_query = session.query(Station.station, Station.name).all()
station_list_df = pd.DataFrame(station_query, columns=['station', 'name'])
station_list = station_list_df.to_json(orient='records')

## temps

year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)

last_year = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > year_ago).all()
last_year_df = pd.DataFrame(last_year, columns=['date','prcp'])
temps = last_year_df.to_json(orient='records')

app = Flask(__name__)

@app.route("/")
def home():
    return (
        f"Available Pages for your review:<br>"
        f"http://127.0.0.1:5000/api/v1.0/precipitation<br>"
        f"http://127.0.0.1:5000/api/v1.0/stations<br>"
        f"http://127.0.0.1:5000/api/v1.0/tobs<br>"
        f"http://127.0.0.1:5000/api/v1.0/temp/start/end"      
    )

@app.route("/api/v1.0/precipitation")
def prcp_output():
    return (precipitation)

@app.route("/api/v1.0/stations")
def station_output():
    return (station_list)

@app.route("/api/v1.0/tobs")
def tobs_output():
    return (temps)

@app.route("/api/v1.0/temp/start/end")
def temp_output():
    return ("I did not figure this one out")


if __name__ == "__main__":
    app.run(debug=True)




