from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
import os
import openai
import langchain_community
from langchain import OpenAI


# Initialize the FastAPI app
app = FastAPI()

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse(os.path.join("static", "favicon.ico"))

# Initialize Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Input model: Accept a menu or dish name from the user
class RecipeRequest(BaseModel):
    dish_name: str

# Endpoint to serve the UI
@app.get("/", response_class=HTMLResponse)
async def serve_ui(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Endpoint for generating a recipe
@app.post("/api/generate-recipe")
async def generate_recipe(request: RecipeRequest):
    if not request.dish_name:
        raise HTTPException(status_code=400, detail="Invalid input. 'dish_name' field is required.")
    
    try:
        # Set your OpenAI API key
        openai_model = OpenAI(openai_api_key="sk-svcacct-7LVrFGzApU6rvptUzDCo3wdCnypBo13kQtGrnLTvP3iMnn2yad9zrUrIol8RgXFsUT3BlbkFJchV1csvM-Sc5hJhba0pilrKmQ2MMAMLV4B1ittUWqe3A_b5lwNNoX8PEgdP5Pu2AA")
        
        # Prompt for generating a recipe based on the dish name
        prompt = f"Please provide a recipe for the dish: {request.dish_name}"
        
        # Get the response from OpenAI
        response = openai_model(prompt)
        
        return {"recipe": response}
    
    except openai.error.OpenAIError as e:
        raise HTTPException(status_code=502, detail="Failed to connect to OpenAI API. Please try again later.")
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")
