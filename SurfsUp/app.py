# Import the dependencies.
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

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
        f"/api/v1.0/start_date/<start><br/>"
        f"/api/v1.0/date_range/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    previous = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    """Return a list of all passenger names"""
    # Query all passengers
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= previous).all()
    
    session.close()
    
    #Create a dictionary for the row data to append to a list of all_precipitation.
    all_precipitation = []
    for date, prcp in results:
            prcp_dict = {}
            prcp_dict['date'] = date
            prcp_dict['prcp'] = prcp
            all_precipitation.append(prcp_dict)
    
    return jsonify(all_precipitation)


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    stations = session.query(Station.station).all()
    session.close()

    station_list = list(np.ravel(stations))

    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
#Query the dates and temperatures of the most-active station for the previous year of data.
#Utilized the most-active station from Part 1 of homework.
def tobs():
    session = Session(engine)
    previous = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    previous_data = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == "USC00519281").\
        filter(Measurement.date >= previous).all()
    session.close()
    previous_data_list = list(np.ravel(previous_data))
    return jsonify(previous_data_list)

@app.route("/api/v1.0/start_date/<start_date>")
def from_date(start_date):
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()
    session.close()
    results_list = list(np.ravel(results))
    return jsonify(results_list)


@app.route("/api/v1.0/date_range/<start_date>/<end_date>")
def get_range(start_date, end_date):
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.date <= end_date).all()
    session.close()
    results_list = list(np.ravel(results))
    return jsonify(results_list)

if __name__ == '__main__':
    app.run(debug=True)