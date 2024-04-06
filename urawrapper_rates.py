
from flask import Flask,jsonify
from os import environ
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)


class CP_Record(db.Model):
    __tablename__ = 'ura_rates'
    id=db.Column(db.Integer, primary_key=True)    
    ppCode = db.Column(db.VARCHAR(255))
    weekdayMin = db.Column(db.VARCHAR(20))
    weekdayRate = db.Column(db.DECIMAL(10, 2))
    satdayMin = db.Column(db.VARCHAR(20))
    satdayRate = db.Column(db.DECIMAL(10, 2))
    sunPHMin = db.Column(db.VARCHAR(20))
    sunPHRate = db.Column(db.DECIMAL(10, 2))
    startTime = db.Column(db.TIME)
    endTime = db.Column(db.TIME)

    def __init__(self,id, ppCode, weekdayMin,weekdayRate,satdayMin,satdayRate,sunPHMin,sunPHRate,startTime,endTime):
        self.id=id
        self.ppCode = ppCode
        self.weekdayMin = weekdayMin
        self.weekdayRate = weekdayRate
        self.satdayMin = satdayMin
        self.satdayRate = satdayRate
        self.sunPHMin = sunPHMin
        self.sunPHRate = sunPHRate
        self.startTime = startTime
        self.endTime = endTime

    def json(self):
        return {"id": self.id, "ppName": self.ppCode, "weekdayMin": self.weekdayMin, "weekdayRate":self.weekdayRate,
                "satdayMin":self.satdayMin,"satdayRate":self.satdayRate,"sunPHMin":self.sunPHMin,"sunPHRate":self.sunPHRate,
                "startTime":self.startTime,"endTime":self.endTime}


@app.route("/ura_rates/<string:carpark_no>")
def find_by_cp_no(carpark_no):
    
    carpark = db.session.scalars(db.select(CP_Record).filter_by(ppCode=carpark_no).limit(1)).first()
    if carpark:
        return jsonify(
            {"weekdayrate":carpark.weekdayRate,
             "weekendrate":carpark.satdayRate
             
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "carpark not found."
        }
    ), 404
    
if __name__=='__main__':
    app.run(host='0.0.0.0', port=5003,debug=False)
