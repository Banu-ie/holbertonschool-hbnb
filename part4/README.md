# HBnB - Simple Web Client (Part 4)

## Pages
- index.html — List of places with price filter
- login.html — Login with JWT auth
- place.html — Place details + reviews
- add_review.html — Add review (auth only)

## Setup
1. Update API_URL in scripts.js to your API address
2. Add CORS to part3: pip install flask-cors, then add CORS(app) in app/__init__.py
3. Run API: cd ../part3 && python run.py
4. Open index.html in browser or: python3 -m http.server 8000
