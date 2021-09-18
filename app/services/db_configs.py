import os 
from dotenv import load_dotenv

load_dotenv()


configs = {
    'user': os.getenv('USER'),
    'password': os.getenv('PASSWORD'),
    'host': os.getenv('HOST'),
    'database': os.getenv('DB_NAME')
}