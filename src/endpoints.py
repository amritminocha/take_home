from flask import Blueprint, jsonify, request
from src.extensions import db
from src.models import Doctor, DoctorAvailability, Appointment
from datetime import datetime, timedelta

home = Blueprint('/', __name__)

@home.route('/')
def index():
    return {'data': 'OK'}

@home.route('/update_doctor_schedule', methods=['POST'])
def update_doctor_schedule():
    data = request.get_json()
    doctor_name = data['doctor']
    schedules = data['schedules'] 

    doctor = Doctor.query.filter_by(name=doctor_name).first()
    if not doctor:
        return jsonify({'error': f'Doctor {doctor_name} not found'}), 404

    for schedule in schedules:
        day = schedule['day']
        start_time = datetime.strptime(schedule['start_time'], "%H:%M:%S").time()
        end_time = datetime.strptime(schedule['end_time'], "%H:%M:%S").time()

        if day not in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
            continue  # Skip invalid days

        availability = DoctorAvailability.query.filter_by(doctor_id=doctor.id, day=day).first()
        if availability:
            availability.start_time = start_time
            availability.end_time = end_time
        else:
            new_availability = DoctorAvailability(doctor_id=doctor.id, day=day, start_time=start_time, end_time=end_time)
            db.session.add(new_availability)

    db.session.commit()
    return jsonify({'message': 'Doctor schedule updated successfully'}), 200

@home.route('/create_appointment', methods=['POST'])
def create_appointment():
    data = request.get_json()
    doctor_name = data['doctor']
    start_time = datetime.strptime(data['start_time'], "%Y-%m-%dT%H:%M:%S")
    end_time = datetime.strptime(data['end_time'], "%Y-%m-%dT%H:%M:%S")

    doctor = Doctor.query.filter_by(name=doctor_name).first()
    if not doctor:
        print(f'Doctor {doctor_name} not found')
        return jsonify({'error': f'Doctor {doctor_name} not found'}), 404

    day = start_time.strftime('%A')
    day_availability = DoctorAvailability.query.filter_by(doctor_id=doctor.id, day=day).first()
    if not day_availability or not day_availability.is_available(start_time.time(), end_time.time()):
        print('Appointment conflict')
        return jsonify({'error': 'Appointment conflict'}), 400

    # Check for overlapping appointments
    overlapping_appointments = Appointment.query.filter_by(doctor_id=doctor.id).filter(
        (Appointment.start_time <= start_time) & (Appointment.end_time > start_time) |
        (Appointment.start_time < end_time) & (Appointment.end_time >= end_time)
    ).all()

    if overlapping_appointments:
        print('Overlapping appointments')
        return jsonify({'error': 'Overlapping appointments'}), 400

    appointment = Appointment(start_time=start_time, end_time=end_time, doctor=doctor)
    db.session.add(appointment)
    db.session.commit()

    print('Appointment created successfully')
    return jsonify({'message': 'Appointment created successfully'}), 201


@home.route('/get_appointments', methods=['GET'])
def get_appointments():
    doctor_name = request.args.get('doctor')
    start_time = datetime.strptime(request.args.get('start_time'), "%Y-%m-%dT%H:%M:%S")
    end_time = datetime.strptime(request.args.get('end_time'), "%Y-%m-%dT%H:%M:%S")

    doctor = Doctor.query.filter_by(name=doctor_name).first()
    if not doctor:
        print(f'Doctor {doctor_name} not found')
        return jsonify({'error': f'Doctor {doctor_name} not found'}), 404

    appointments = [{'start_time': appointment.start_time, 'end_time': appointment.end_time}
                    for appointment in doctor.appointments
                    if start_time <= appointment.start_time <= end_time]

    print('Appointments:', appointments)
    return jsonify({'appointments': appointments})


@home.route('/get_next_available_appointment', methods=['GET'])
def get_next_available_appointment():
    doctor_name = request.args.get('doctor')
    start_time = datetime.strptime(request.args.get('start_time'), "%Y-%m-%dT%H:%M:%S")
    required_duration = timedelta(minutes=int(request.args.get('required_duration')))

    doctor = Doctor.query.filter_by(name=doctor_name).first()
    if not doctor:
        return jsonify({'error': f'Doctor {doctor_name} not found'}), 404

    current_time = start_time
    search_limit = datetime.now() + timedelta(weeks=4)  # Example limit: 4 weeks from now

    while current_time <= search_limit:
        end_time = current_time + required_duration
        day = current_time.strftime('%A')
        day_availability = DoctorAvailability.query.filter_by(doctor_id=doctor.id, day=day).first()

        if day_availability and day_availability.is_available(current_time.time(), end_time.time()) and doctor.is_available(current_time, end_time):
            return jsonify({'next_appointment': {'start_time': current_time, 'end_time': end_time}})

        if day_availability and current_time.time() >= day_availability.end_time:
            current_time = (current_time + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        else:
            overlapping_appointments = Appointment.query.filter(
                Appointment.doctor_id == doctor.id,
                Appointment.end_time > current_time,
                Appointment.start_time < end_time
            ).order_by(Appointment.end_time.asc()).first()

            if overlapping_appointments:
                current_time = overlapping_appointments.end_time
            else:
                current_time = end_time

    return jsonify({'error': 'No available appointment found within the specified time range'}), 404
