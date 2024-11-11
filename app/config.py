import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:123456@localhost:5437/food-db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CORS_ORIGINS = ["http://localhost:3000"]
    SWAGGER_URL = '/swagger'
    API_URL = '/api-docs'
    # Configurations for image analysis
    API_KEY = "4VQKUVUF.lEnStEKIxQVQLLYZEhc24kpiNaQTI3SA"
    TMP_DIR = "/tmp"