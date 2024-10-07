import os
from dotenv import load_dotenv


load_dotenv()


DATA_PATH = "../data"
DISTANCEMATRIX_URL = "http://distancematrix.ai/distancematrixaccurate"
DISTANCEMATRIX_API_KEY = os.getenv("DISTANCE_MATRIX_API_KEY")
