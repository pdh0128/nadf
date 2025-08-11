
from fastapi import FastAPI, Request, Form, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
import requests
from bs4 import BeautifulSoup
import pdfkit
import os
import tempfile
from datetime import datetime
from service import namuwiki_service
from decorator.exception_handler_decorator import exception_handler

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@exception_handler
@app.post("/convert", response_class=HTMLResponse)
async def convert_wiki(background_tasks: BackgroundTasks, url: str = Form(...)):
    pdf_path = await namuwiki_service.namuwiki_to_pdf(url)

    background_tasks.add_task(lambda p: os.path.exists(p) and os.remove(p), pdf_path)

    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename=os.path.basename(pdf_path),
        background=background_tasks,
    )