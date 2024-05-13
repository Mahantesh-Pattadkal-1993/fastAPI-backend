# Import the APIRouter class from FastAPI
from fastapi import APIRouter
from services.first_service import Animal

# Define a router using APIRouter
router = APIRouter()
AnimalService = Animal("Simba","Lion")

# Define a route for the root endpoint "/"
@router.get("/")
async def read_root():
    # Return a simple message
    return {"message": "Hello, World!"}

@router.get("/Animal")
async def read_root():
    # Return a simple message
    return {"message": {"name": AnimalService.name, "Species":AnimalService.species}}



# Define a route that takes an item_id and an optional query parameter q
@router.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    # Return the item_id and the value of the q parameter
    return {"item_id": item_id, "q": q}


