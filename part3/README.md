# HBnB Project — Part 2: REST API

## 📌 Overview
This project is a RESTful API built with Flask.  
It allows managing **Users, Places, Amenities, and Reviews**.

The API supports full CRUD operations and follows a simple layered architecture.

---

## ⚙️ Setup

### 1. Install dependencies
```bash
pip install flask
```

### 2. Run the server
```bash
python3 app.py
```

### 3. Server URL
```
http://127.0.0.1:5000
```

---

## 🏗️ Architecture

The project follows a 3-layer architecture:

- **Presentation Layer** → Flask API (routes)
- **Business Logic Layer** → Models & validation
- **Persistence Layer** → In-memory storage (lists)

---

## 📡 API Endpoints

### 👤 Users
- `POST /users`
- `GET /users`
- `GET /users/<id>`
- `PUT /users/<id>`
- `DELETE /users/<id>`

### 🏠 Places
- `POST /places`
- `GET /places`
- `GET /places/<id>`
- `PUT /places/<id>`
- `DELETE /places/<id>`

### 🛠️ Amenities
- `POST /amenities`
- `GET /amenities`
- `GET /amenities/<id>`
- `PUT /amenities/<id>`
- `DELETE /amenities/<id>`

### ⭐ Reviews
- `POST /reviews`
- `GET /reviews`
- `GET /reviews/<id>`
- `PUT /reviews/<id>`
- `DELETE /reviews/<id>`

---

## 🧪 Testing

The API was tested using `curl`.

### Example:
```bash
curl http://127.0.0.1:5000/users
```

Create user:
```bash
curl -X POST http://127.0.0.1:5000/users \
-H "Content-Type: application/json" \
-d '{"name": "Aylin"}'
```

---

## 📝 Notes

- Data is stored in memory (no database yet)
- UUID is used for unique IDs
- Data resets when the server restarts
- Basic validation is implemented
- Authentication will be added in Part 3

---

## ✅ Status

- Users ✅
- Amenities ✅
- Places ✅
- Reviews ✅

✔️ All CRUD operations implemented  
✔️ API fully working  
✔️ Ready for submission
