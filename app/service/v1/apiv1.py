import fastapi
from fastapi import Request, JSONResponse
from typing import List, Dict


def get_client_api():
    return fastapi.FastAPI()

def get_client_api_router_v1():
    return fastapi.APIRouter(prefix='/v1')

api = get_client_api()
router_v1 = get_client_api_router_v1()

@router_v1.get("/")
def root():
    return {"message": "Hello World!"}

@router_v1.get("/health")
def health():
    return {"message": "OK"}

@router_v1.get("query")
def query(query: str, history: List[Dict[str, str]]):
    try:
        # model call on query and history
        return 
    except Exception as e:
        return {"response": "Error", "error": "Not valid response"}
    
@router_v1.middleware('http')
def token_validation(request: Request, call_next):
    #TODO: change it to False
    valid = True
    # check session
    if valid:
        call_next(request)
    else:
        return JSONResponse(status_code=401, content={"response": "Unauthorized"})
