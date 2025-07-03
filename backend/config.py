import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    BASE_URL = os.getenv('BASE_URL', 'http://localhost:5000')
