from fastapi import APIRouter,Response
index_routes = APIRouter()

@index_routes.get("/")
def root():
    return "Fast Api"
