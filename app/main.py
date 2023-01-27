from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from .services.utils import *

app = FastAPI()

app.mount("/static", StaticFiles(directory="./app/static"), name="static")

templates = Jinja2Templates(directory="./app/templates")


@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/", response_class=HTMLResponse)
async def start_osint(request: Request, input: str = Form()):
    redirections = "None"
    try:
        ip_address = get_ip(input)
    except:
        ip_address = ""

    try:
        reverse_dns = get_reverse_dns(ip_address)
    except:
        reverse_dns = "Only found IP: "+ ip_address

    try:
        whois = get_whois(ip_address)
    except:
        whois = ""

    try:
        redirections = analyse_redirections(input)
    except:
        redirections = ""

    return templates.TemplateResponse("response.html", {
        "request": request,
        "url": input,
        "reverse_dns": reverse_dns,
        "whois": whois,
        "analyse_redirections": redirections
    })
