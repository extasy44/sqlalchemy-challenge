import datetime as dt
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

year_ago = '2016-08-23'

# Flask Routes
@app.route("/")
def welcome():
    return (
      "<p>Welcome to the Hawaii weather API!</p>"
      "<p>Usage:</p>"
      "/api/v1.0/precipitation<br/><br/>"
      "/api/v1.0/stations<br/><br/>"
      "/api/v1.0/tobs<br/><br/>"
      "/api/v1.0/date<br/><br/>."
      "/api/v1.0/start_date/end_date<br/><br/>."
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    prcp_res = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_ago).all()    
    return jsonify(prcp_res)

@app.route("/api/v1.0/stations")
def stations():
    all_station = session.query(Station.station, Station.name).all()
    return jsonify(all_station)

@app.route("/api/v1.0/tobs")
def tobs():
    tobs_res = session.query(Measurement.date, Measurement.station, Measurement.tobs).filter(Measurement.date >= year_ago).all()
    return jsonify(tobs_res)

@app.route("/api/v1.0/<date>")
def startDateOnly(date):
    temp_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= date).all()
    return jsonify(temp_results)

@app.route("/api/v1.0/<start>/<end>")
def startDateEndDate(start,end):
    start_end_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    return jsonify(start_end_results)

if __name__ == "__main__":
    app.run(debug=True)