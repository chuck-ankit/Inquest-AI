from fastapi import FastAPI, Form, Request, Response, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.middleware.sessions import SessionMiddleware
import uvicorn
import os
import aiofiles
import json
import csv
from src.helper import llm_pipeline
from pathlib import Path
from typing import Optional
import shutil

app = FastAPI(title="InquestAI")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add session middleware
app.add_middleware(
    SessionMiddleware,
    secret_key="your-secret-key",
    max_age=3600  # 1 hour
)

# Static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Security
security = HTTPBasic()

# Ensure required directories exist
UPLOAD_DIR = Path("static/docs")
OUTPUT_DIR = Path("static/output")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/features")
async def features(request: Request):
    return templates.TemplateResponse("features.html", {"request": request})

@app.get("/about")
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

@app.get("/contact")
async def contact(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})

@app.get("/faq")
async def faq(request: Request):
    return templates.TemplateResponse("faq.html", {"request": request})

@app.get("/blog")
async def blog(request: Request):
    return templates.TemplateResponse("blog.html", {"request": request})

@app.get("/dashboard")
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.post("/upload")
async def upload_file(
    request: Request, 
    pdf_file: bytes = File(...), 
    filename: str = Form(...)
):
    try:
        # Validate file size and type
        if len(pdf_file) > 10 * 1024 * 1024:  # 10MB limit
            raise HTTPException(status_code=400, detail="File too large")
        
        if not filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Invalid file type")

        pdf_path = UPLOAD_DIR / filename
        
        async with aiofiles.open(pdf_path, 'wb') as f:
            await f.write(pdf_file)

        return Response(
            jsonable_encoder(json.dumps({
                "msg": "success",
                "pdf_filename": str(pdf_path)
            }))
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/analyze")
async def analyze_file(
    request: Request,
    pdf_filename: str = Form(...)
):
    try:
        output_file = get_csv(pdf_filename)
        return Response(
            jsonable_encoder(json.dumps({
                "output_file": output_file
            }))
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def get_csv(file_path: str) -> str:
    try:
        answer_generation_chain, ques_list = llm_pipeline(file_path)
        output_file = OUTPUT_DIR / "QA.csv"

        with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(["Question", "Answer"])

            for question in ques_list:
                answer = answer_generation_chain.run(question)
                csv_writer.writerow([question, answer])

        return str(output_file)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@app.post("/contact/submit")
async def submit_contact(request: Request):
    try:
        form_data = await request.form()
        # Process contact form submission
        # Add email sending logic here
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/history")
async def get_history(request: Request):
    # Implement user history retrieval
    return {"history": []}

if __name__ == "__main__":
    uvicorn.run("app:app", host='0.0.0.0', port=8080, reload=True)