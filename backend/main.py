from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from response import llm_search_disabled, llm_search_enabled

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserInput(BaseModel):
    query: str

@app.post("/search_enabled/")
async def get_llm_response(request: Request, user_input: UserInput = None):
    payload = await request.json()
    print(f"Received payload: {payload}")
    if user_input:
        try:
            output = llm_search_enabled(user_input.query)
            return {"response": output}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        raise HTTPException(status_code=422, detail="Invalid input")
    
@app.post("/search_disabled/")
async def get_llm_response(user_input: UserInput):
    try:
        output = llm_search_disabled(user_input.query)
        return {"response": output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
