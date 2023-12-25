from fastapi import FastAPI
import uvicorn
from api import api

app = FastAPI(
    title="Report Engine"
)
app.include_router(api.api_router)

def serve():
    """Serve the web application."""
    uvicorn.run(app, port=8001, host='0.0.0.0')

if __name__ == "__main__":
    serve()