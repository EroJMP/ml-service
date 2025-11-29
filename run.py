import uvicorn
import os
from app.config import API_HOST, DEBUG

if __name__ == "__main__":
    # Railway sets PORT environment variable, use it if available
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting server on port {port}")
    uvicorn.run("app.main:app", host=API_HOST, port=port, reload=DEBUG) 