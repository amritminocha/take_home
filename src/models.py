from src.extensions import db
from flask import jsonify


class DummyModel(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.String, nullable=False)

    def json(self) -> str:
        """
        :return: Serializes this object to JSON
        """
        return jsonify({'id': self.id, 'value': self.value})
    
class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    appointments = db.relationship('Appointment', backref='doctor', lazy=True)
    availability = db.relationship('DoctorAvailability', backref='doctor', lazy=True)

    def is_available(self, start_time, end_time):
        for appointment in self.appointments:
            if not (end_time <= appointment.start_time or start_time >= appointment.end_time):
                return False
        return True

class DoctorAvailability(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    day = db.Column(db.String(10), nullable=False) 
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)

    def is_available(self, start_time, end_time):
        return start_time >= self.start_time and end_time <= self.end_time

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)

