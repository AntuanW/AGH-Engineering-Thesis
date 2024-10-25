import os
from dotenv import load_dotenv

load_dotenv()

DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')

MONGODB_URI = f"mongodb+srv://{DB_USERNAME}:{DB_PASSWORD}@agh-engineering-thesis.yguzi.mongodb.net/?retryWrites=true&w=majority&appName=AGH-Engineering-Thesis"