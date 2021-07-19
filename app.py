import numpy as np
import datetime as dt
from dateutil.relativedelta import relativedelta

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

app = Flask(__name__)

year_ago = '2016-08-23'

# Flask Routes
@app.route("/")
def welcome():
    return (
      "<p>Welcome to the Hawaii weather API!</p>"
      "<p>Available Route :</p>"
      "/api/v1.0/precipitation<br/><br/>"
      "/api/v1.0/stations<br/><br/>"
      "/api/v1.0/tobs<br/><br/>"
      "/api/v1.0/date<br/><br/>"
      "/api/v1.0/start_date/end_date<br/><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    prcp_res = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_ago).all()  
    prcp_arr = []

    for date, prcp in prcp_res:
      prcp_dict = {}
      prcp_dict[date] = prcp
      prcp_arr.append(prcp_dict)  
    
    session.close()
    return jsonify(prcp_arr)
    

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    all_station = session.query(Station.station, Station.name).all()
    station_arr = []

    for station, name in all_station:
      station_dict = {}
      station_dict["station"] = station,
      station_dict["name"] = name,
      station_arr.append(station_dict)

    session.close()
    return jsonify(station_arr)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    tobs_res = session.query(Measurement.date, Measurement.station, Measurement.tobs).filter(Measurement.date >= year_ago).all()
    tobs_res_arr = []
    for date, station, tobs in tobs_res:
      tobs_dict = {}
      tobs_dict["date"] = date,
      tobs_dict["station"] = station,
      tobs_dict["tobs"] = tobs
      tobs_res_arr.append(tobs_dict)

    session.close()
    return jsonify(tobs_res_arr)

@app.route("/api/v1.0/<date>")
def start(date):
    session = Session(engine)
    temp_res = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= date).all()
    session.close()
    
    return jsonify(list(np.ravel(temp_res)))

@app.route("/api/v1.0/<start>/<end>")
def startEnd(start,end):
    session = Session(engine)
    start_end_res = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()

    return jsonify(list(np.ravel(start_end_res)))

if __name__ == "__main__":
    app.run(debug=True)