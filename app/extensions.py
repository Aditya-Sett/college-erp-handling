# CORS -> Cross-Origin Resource Sharing
"""
Frontend-Backend Separation:

Frontend: http://localhost:3000 (React/Vue)

Backend: http://localhost:5000 (Flask)

CORS allows them to communicate

Third-Party API Access:

If you want other websites to use your API

Mobile App Backend:

Mobile apps need to call your Flask API from different domains
"""

from flask_cors import CORS

def init_extensions(app):
    CORS(app)
