from flask import Flask, jsonify
import numpy as np
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

Station = Base.classes.station
Measurement = Base.classes.measurement

session = Session(engine)
app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= "2016-08-24").all()

    session.close()
    all_prcp = []
    for date,prcp  in data:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
               
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():
    stations = session.query(Station.station).\
                 order_by(Station.station).all()

    session.close()
    list_stations = list(np.ravel(stations))

    return jsonify(list_stations)


#Same as percipitation?
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    temps = session.query(Measurement.date,  Measurement.tobs,Measurement.prcp).filter(Measurement.date >= '2016-08-23').filter(Measurement.station=='USC00519281').order_by(Measurement.date).all()
    session.close()

    list_tobs = []
    for prcp, date,tobs in temps:
        tobs_dict = {}
        tobs_dict["prcp"] = prcp
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        
        list_tobs.append(tobs_dict)

    return jsonify(list_tobs)

@app.route("/api/v1.0/<start_date>")
def start_date(start_date):

    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).all()

    session.close()

    sdate_tobs = []
    for min, avg, max in results:
        sdate_tobs_dict = {}
        sdate_tobs_dict["min_temp"] = min
        sdate_tobs_dict["avg_temp"] = avg
        sdate_tobs_dict["max_temp"] = max
        sdate_tobs.append(sdate_tobs_dict) 
    return jsonify(sdate_tobs)

#mimic startdate function
@app.route("/api/v1.0/<start_date>/<end_date>")
def start_end_date(start_date, end_date):
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    session.close()
    start_end_tobs = []
    for min, avg, max in results:
        start_end_tobs_dict = {}
        start_end_tobs_dict["min_temp"] = min
        start_end_tobs_dict["avg_temp"] = avg
        start_end_tobs_dict["max_temp"] = max
        start_end_tobs.append(start_end_tobs_dict) 
    

    return jsonify(start_end_tobs)
if __name__ == '__main__':
    app.run(debug=True)