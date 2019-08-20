from flask import Flask, jsonify
import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources\hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
Base.prepare(engine, reflect=True)

measurement = Base.classes.measurement
station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    return (
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

    
    session = Session(engine)

    results = session.query(measurement.date, measurement.prcp).all()

    session.close

    prcp = []

    for result in results:
        prcp_dict = {}
        prcp_dict["date"] = result.date
        prcp_dict["prcp"] = result.prcp
        prcp.append(prcp_dict)

    return jsonify(prcp)

@app.route("/api/v1.0/stations")
def stations():
    
    session = Session(engine)
    
    results = session.query(station.station).all()

    session.close

    stations = list(np.ravel(results))
    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def tobs():
    
    session = Session(engine)
    
    last_date = dt.datetime(2016, 8, 22)

    prev_date = last_date - dt.timedelta(365)

    results = session.query(measurement.date, measurement.prcp).filter(measurement.date > prev_date).all()

    session.close

    tobs = list(np.ravel(results))
    return jsonify(tobs)

@app.route("/api/v1.0/<start>")
def trip_start(start):
    
    session = Session(engine)

    start_date = dt.datetime.strptime(start,"%Y-%m-%d")

    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start_date).all()
    
    session.close()

    outlook = list(np.ravel(results))

    return jsonify(outlook)



@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    
    session = Session(engine)

    start_date = dt.datetime.strptime(start,"%Y-%m-%d")

    end_date = dt.datetime.strptime(end,"%Y-%m-%d")

    results= session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start_date).filter(measurement.date <= end_date).all()

    outlook = list(np.ravel(results))

    return jsonify(outlook)

if __name__ == "__main__":
    app.run(debug=True, port=5007)