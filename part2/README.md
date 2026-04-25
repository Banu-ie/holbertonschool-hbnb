# HBnB Project - Part 2

## Overview
This project is a REST API built with Flask.
It manages Users, Places, Amenities, and Reviews.

## Setup
pip install flask flask-restx
python3 app.py

## Endpoints

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

## Notes
Data is stored in memory.
