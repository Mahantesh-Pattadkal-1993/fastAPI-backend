
# Import necessary modules
from fastapi import FastAPI  # Import the FastAPI class
from routers.get_router import router as GETrouter  # Import the router from routers.get_router
import uvicorn  # Import uvicorn for running the server

# Create a FastAPI app instance
app = FastAPI()  # Create a FastAPI instance

# Include the router in your app
app.include_router(router=GETrouter)  # Include the router in the app

# Run the Uvicorn server
if __name__ == "__main__":  # Check if the script is being run directly
    uvicorn.run("app:app", host="0.0.0.0", port=8080, reload=True)  # Run Uvicorn with the app instance on port 8080

# Runs on this link: http://127.0.0.1:8080/