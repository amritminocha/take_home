## Doctor Appointment Scheduler

# Overview

This Flask application is designed to manage doctor appointments. It enables updating doctors' schedules, creating new appointments, and retrieving existing appointments. The application utilizes a SQLite database for storing data.

# Setup

Change directory into the cloned repository:
1. After cloning this repository, cd into it.
2. Set up virtual environment via ```python3 -m venv env``` 
3. Activate the virtual environment via ```source env/bin/activate```
4. If it's properly set up, ```which python``` should point to a python under api-skeleton/env.
5. Install dependencies via ```pip install -r requirements.txt```

## Starting local flask server
Under take_home/src, run ```flask run --host=0.0.0.0 -p 8000```

By default, Flask runs with port 5000, but some MacOS services now listen on that port.

## Default Data
By default, the application initializes the database with two doctors: Strange and Who. These are added to the Doctor table on each application start.

# Adding More Doctors
To add more doctors to the database, you can use the following Python code snippet and add it in app.py:
```
if not Doctor.query.filter_by(name="New Doctor Name").first():
            new_doctor = Doctor(name="New Doctor Name")
            db.session.add(new_doctor)
```

## API Endpoints

# Update Doctor Schedule

Endpoint: /update_doctor_schedule

Method: POST

Description: Updates the availability schedule for a specific doctor.

Payload Example:
```
{
  "doctor": "Strange",
  "schedules": [
    {
      "day": "Monday",
      "start_time": "09:00:00",
      "end_time": "17:00:00"
    },
    {
      "day": "Tuesday",
      "start_time": "09:00:00",
      "end_time": "17:00:00"
    }
  ]
}
```


Curl Request:
```
curl --location 'http://localhost:8000/update_doctor_schedule' \
--header 'Content-Type: application/json' \
--data '{
    "doctor": "Strange",
    "schedules": [
        {
            "day": "Monday",
            "start_time": "09:00:00",
            "end_time": "17:00:00"
        },
        {
            "day": "Tuesday",
            "start_time": "09:00:00",
            "end_time": "17:00:00"
        }
    ]
}
'
```


If we want to set (9 AM to 5 PM, M-F for Strange, 8 AM to 4 PM M-F for Who),
run these two curls:

Curl1 for doctor Strange:
```
curl --location 'http://localhost:8000/update_doctor_schedule' \
--header 'Content-Type: application/json' \
--data '{
    "doctor": "Strange",
    "schedules": [
        {
            "day": "Monday",
            "start_time": "09:00:00",
            "end_time": "17:00:00"
        },
        {
            "day": "Tuesday",
            "start_time": "09:00:00",
            "end_time": "17:00:00"
        },
        {
            "day": "Wednesday",
            "start_time": "09:00:00",
            "end_time": "17:00:00"
        },
        {
            "day": "Thursday",
            "start_time": "09:00:00",
            "end_time": "17:00:00"
        },
        {
            "day": "Friday",
            "start_time": "09:00:00",
            "end_time": "17:00:00"
        }
    ]
}
'
```

Curl2 for doctor Who:
```
curl --location 'http://localhost:8000/update_doctor_schedule' \
--header 'Content-Type: application/json' \
--data '{
    "doctor": "Who",
    "schedules": [
        {
            "day": "Monday",
            "start_time": "08:00:00",
            "end_time": "16:00:00"
        },
        {
            "day": "Tuesday",
            "start_time": "08:00:00",
            "end_time": "16:00:00"
        },
        {
            "day": "Wednesday",
            "start_time": "08:00:00",
            "end_time": "16:00:00"
        },
        {
            "day": "Thursday",
            "start_time": "08:00:00",
            "end_time": "16:00:00"
        },
        {
            "day": "Friday",
            "start_time": "08:00:00",
            "end_time": "16:00:00"
        }
    ]
}
'
```

# Create Appointment

Endpoint: /create_appointment

Method: POST

Description: Books an appointment with a specific doctor, checking for any overlapping appointments.

Payload Example:
```
{
  "doctor": "Who",
  "start_time": "2024-01-15T10:00:00",
  "end_time": "2024-01-15T11:00:00"
}
```

Curl Request:
```
curl --location 'http://localhost:8000/create_appointment' \
--header 'Content-Type: application/json' \
--data '{"doctor": "Strange", "start_time": "2024-01-15T12:00:00", "end_time": "2024-01-15T12:40:00"}'
```

# Get Appointments
Endpoint: /get_appointments

Method: GET

Description: Retrieves a list of appointments for a specified doctor within a given time range.

Query Parameters: doctor, start_time, end_time

Curl Request:
```
curl --location 'http://localhost:8000/get_appointments?doctor=Who&start_time=2024-01-10T00%3A00%3A00&end_time=2024-01-17T23%3A59%3A59'
```

# Get Next Available Appointment

Endpoint: /get_next_available_appointment

Method: GET

Description: Finds the next available appointment slot for a specified doctor.

Query Parameters: doctor, start_time, required_duration

Curl Request:
```
curl --location 'http://localhost:8000/get_next_available_appointment?doctor=Who&start_time=2024-01-15T10%3A00%3A00&required_duration=40' \
--header 'Content-Type: application/json'
```

## Models
Doctor: Manages doctors and their relationships with appointments and availability.

DoctorAvailability: Handles the availability of each doctor.

Appointment: Represents scheduled appointments with doctors.

## Database
This application uses SQLite. On each application start, it initializes the database and populates it with some initial doctor data.

For better DB assistance, I used the software Beekeeper Studio
Downloading link: https://github.com/beekeeper-studio/beekeeper-studio/releases/tag/v4.0.3
