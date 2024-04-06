from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from sqlalchemy.sql import func
from datetime import datetime, timedelta
from sqlalchemy import desc
from flask_cors import CORS
from datetime import datetime

datetime_format = "%Y-%m-%dT%H:%M"

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = environ.get('dbURL')
# app.config["SQLALCHEMY_DATABASE_URI"] = environ.get('dbURL') or "mysql+mysqlconnector://root@localhost:3306/session"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'isolation_level': 'READ COMMITTED'
}



db = SQLAlchemy(app)


class Session(db.Model):
    __tablename__ = 'session'

    sessionID = db.Column(db.Integer, primary_key=True)
    starttime = db.Column(db.DateTime, nullable=False)
    endtime = db.Column(db.DateTime, nullable=False)
    ppCode = db.Column(db.String(5))
    # foreign key to carpark locator?
    notifAllowed = db.Column(db.Boolean, nullable=False)
    userID = db.Column(db.Integer, nullable=False)
    latitude = db.Column(db.Float, nullable=True)  
    longitude = db.Column(db.Float, nullable=True) 
    
    

    def __init__(self, starttime, endtime, ppCode, userID, notifAllowed, latitude, longitude):
        # self.sessionID = sessionID
        self.starttime = starttime
        self.endtime = endtime
        self.ppCode = ppCode
        self.userID = userID
        self.notifAllowed = notifAllowed
        self.latitude = latitude
        self.longitude = longitude


    def json(self):
        return {
            "sessionID": self.sessionID, 
            "starttime": self.starttime, 
            "endtime": self.endtime, 
            "ppCode": self.ppCode, 
            "userID": self.userID, 
            "notifAllowed": self.notifAllowed, 
            "latitude": self.latitude, 
            "longitude": self.longitude
            }

# get all
@app.route("/session")
def get_all():
    sessionrecord = db.session.scalars(db.select(Session)).all()
    print('heloooo')
    if len(sessionrecord):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "sessions": [session.json() for session in sessionrecord]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no session records."
        }
    ), 404

# find specific session
@app.route("/session/<string:userID>")
def find_by_sessionID(userID):
    session = db.session.scalars(
    	db.select(Session).filter_by(userID=userID).order_by(desc('sessionID')).
    	limit(1)
).first()


    if session:
        data = {
            "userID": session.userID,
            "sessionID": session.sessionID
        }
        return jsonify(
            {
                "code": 200,
                "data": data
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Session record not found."
        }
    ), 404

@app.route("/session/location/<string:userID>") #scenario 2: input userid, return location
def return_carpark_location(userID):
    session = db.session.scalars(
        db.select(Session).filter_by(userID=userID).order_by(desc('sessionID')).limit(1)
    ).first()

    if session:
        data = {
            "userID": session.userID,
            "latitude": session.latitude,
            "longitude": session.longitude
        }
        return jsonify({"code": 200, "data": data})
    else:
        return jsonify({"code": 404, "message": "Session record not found."}), 404


    

@app.route("/session/trigger")
def find_by_current_datetime():
    now = datetime.now() + timedelta(hours=8)  # Use datetime.now() if your application uses local time instead of UTC

    # Calculate 15 minutes from now
    fifteen_minutes_from_now = now + timedelta(minutes=15)
   
    # Query for sessions ending in the next 15 minutes
    sessions_ending_soon = db.session.scalars(
    db.select(Session)
    .filter(
        Session.endtime >= now,  # Ensure 'endtime' is in the future
        Session.endtime <= fifteen_minutes_from_now
    )
    ).all()
    # sessions_ending_soon = db.session.scalars(db.select(Session)).all()

    print(sessions_ending_soon)
    if sessions_ending_soon:
        return jsonify(
            {
                "code": 200,
                "data": [endingsession.json() for endingsession in sessions_ending_soon]
            }
        )
    # return jsonify({"code": 200, "data": []}), 200
    return jsonify({"code":404,"current time":now,"data":sessions_ending_soon}),404

# update session endtime
@app.route("/session/<string:sessionID>", methods=['PUT'])
def update_session(sessionID):
    try:
        session = db.session.scalars(
        db.select(Session).filter_by(sessionID=sessionID).order_by(desc('sessionID')).
        limit(1)).first()
        if not session:
            return jsonify(
                {
                    "code": 404,
                    "data": {
                        "sessionID": sessionID
                    },
                    "message": "session not found."
                }
            ), 404
        sessionendtime = session.endtime
       
        # update status
        data = request.get_json()
        if datetime.strptime(data['endtime'], datetime_format)>sessionendtime:
            if data['endtime']:
                session.endtime = data['endtime']
                session.notifAllowed = data['notifAllowed']
                db.session.commit()
                return jsonify(
                    {
                        "code": 200,
                        "data": session.json()
                    }
                ), 200
        else:
            return jsonify(
            {
                "code": 500,
                "data": {
                    "session_id": sessionID
                },
                "message": "Inputted end time is before the previously set end time."
            }
        ), 500

    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "session_id": sessionID
                },
                "message": "An error occurred while updating the session. " + str(e)
            }
        ), 500


# create new session record
@app.route("/session", methods=['POST'])
def create_session():
    # userID = request.json.get('userID')

    try:
        data = request.get_json()
    

        if data:
            if datetime.strptime(data['endtime'], datetime_format)> datetime.strptime(data['starttime'], datetime_format):
                session = Session(userID=data['userID'],starttime=data['starttime'],endtime=data['endtime'],ppCode=data['ppCode'],notifAllowed=data['notifAllowed'], latitude=data['latitude'], longitude=data['longitude'])
 
                db.session.add(session)
                db.session.commit()
            else:
                return jsonify({
                    "code":404,
                    "data": "Start time is after End time. Please check your timings." 
                }),404

        return jsonify(
            {
                "code": 200,
                "data": session.json()
            }
            ), 200
        
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while creating the session. " + str(e)
            }
        ), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5006, debug=True)
