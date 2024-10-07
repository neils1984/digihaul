import os
from dotenv import load_dotenv


load_dotenv()

# APIS
DISTANCEMATRIX_URL = "http://distancematrix.ai/distancematrixaccurate"
DISTANCEMATRIX_API_KEY = os.getenv("DISTANCE_MATRIX_API_KEY")

# DATASET
DATA_PATH = "../data"
