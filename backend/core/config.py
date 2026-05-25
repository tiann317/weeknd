from dotenv import load_dotenv
import os

load_dotenv()

DB_CLIENT_ID = os.getenv("DB_CLIENT_ID")
DB_API_KEY = os.getenv("DB_API_KEY")
AUGS_LAT = os.getenv("AUGS_LAT")
AUGS_LON = os.getenv("AUGS_LON")
OBER_LAT = os.getenv("OBER_LAT")
OBER_LON = os.getenv("OBER_LON")
