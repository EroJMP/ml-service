import os
from dotenv import load_dotenv
from pathlib import Path

# Load .env file if it exists
env_path = Path(__file__).parent.parent / '.env'
if env_path.exists():
    load_dotenv(env_path)

# API Configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")

# Handle PORT from various platforms (Render, Railway, etc. use PORT)
# Also handle case where PORT might be set to literal '$PORT' string
port_value = os.getenv("PORT") or os.getenv("API_PORT", "8000")
# If port_value is the literal '$PORT' string, use default
if port_value == "$PORT":
    port_value = "8000"
try:
    API_PORT = int(port_value)
except (ValueError, TypeError):
    API_PORT = 8000

DEBUG = os.getenv("DEBUG", "True").lower() in ('true', '1', 't')

# CORS Settings - Allow our Next.js app
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000,http://localhost:3001").split(',')

# Security
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")

# Paths
BASE_DIR = Path(__file__).parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"
DB_DIR = BASE_DIR / "database"

# Model Settings
MODEL_PATH = os.getenv("MODEL_PATH", str(BASE_DIR / "cnn_sign_model.h5"))
CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", "0.75"))

# Supabase Configuration (for temporary signature storage)
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY", "")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY", "")

# Create directories if they don't exist
UPLOAD_DIR.mkdir(exist_ok=True)
DB_DIR.mkdir(exist_ok=True) 