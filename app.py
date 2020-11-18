import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite", echo=False)

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect = True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        # f"/api/v1.0/<start><br/>"
        # f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    """Returns the jsonified precipitation data for the last year in the database"""
    # Query all passengers
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= "2016-08-23").\
        all()
    session.close()
    # return jsonify(results)
    # Convert query results to dictionary
    last_year_precipitation = []
    for date, prcp in results:
        prcp_d = {}
        prcp_d["date"] = date
        prcp_d["prcp"] = prcp

        last_year_precipitation.append(prcp_d)
        
    return jsonify(last_year_precipitation)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Returns jsonified data of all of the stations in the database
    results = session.query(Station.name, Station.station).all()
   
    session.close()

    return jsonify(results) 

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    #Query the dates and temperature observations of the most active station for the last year of data.
    # Return jsonified data for the most active station (USC00519281) for the last year of data
    results = session.query(Measurement.date).\
        filter(Measurement.station == "USC00519281", Measurement.date >= "2016-08-23").\
        with_entities(Measurement.date, Measurement.tobs).all()
   
    session.close()

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)