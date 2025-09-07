import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Model Configuration
MODEL_NAME = os.getenv("MODEL_NAME", "facebook/opt-125m")
MAX_LENGTH = int(os.getenv("MAX_LENGTH", "512"))
MIN_LENGTH = int(os.getenv("MIN_LENGTH", "50"))

# Server Configuration
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))

# Logging Configuration
LOG_FILE = os.getenv("LOG_FILE", "request_logs.xlsx")
