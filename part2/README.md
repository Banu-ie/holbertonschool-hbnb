# HBnB Project - Part 2

## Overview
This project is a RESTful API built using Flask. It allows managing Users, Places, Amenities, and Reviews. The API supports basic CRUD operations and follows a simple layered architecture.

## Setup
Install dependencies and run the server:
pip install flask flask-restx
python3 app.py

Server runs on:
http://127.0.0.1:5000

## Architecture
The project is organized into three layers:
- Presentation Layer (Flask API)
- Business Logic Layer (Models)
- Persistence Layer (In-memory storage)

## API Endpoints

Users:
POST /users
GET /users
GET /users/<id>
PUT /users/<id>

Amenities:
POST /amenities
GET /amenities
GET /amenities/<id>
PUT /amenities/<id>

Places:
POST /places
GET /places
GET /places/<id>
PUT /places/<id>

Reviews:
POST /reviews
GET /reviews
GET /reviews/<id>
PUT /reviews/<id>
DELETE /reviews/<id>

## Testing
The API was tested using curl commands.
Example:
curl http://127.0.0.1:5000/users

## Notes
- Data is stored in memory (no database yet)
- UUID is used for unique IDs
- Data resets when server restarts
- Authentication will be added in Part 3

## Status
Users implemented
Amenities implemented
Places implemented
Reviews implemented

Project ready for submission
