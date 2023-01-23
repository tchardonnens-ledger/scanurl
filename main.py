from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from services import osint

import socket
from ipwhois import IPWhois
import requests
import urllib
import tldextract
from utils import analyse_redirections

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/", response_class=HTMLResponse)
async def start_osint(request: Request, url: str = Form()):
    # Demande à l'utilisateur de saisir une URL
    url = url
    # Récupère l'adresse IP de l'URL en utilisant le module "socket"
    extracted_domain = tldextract.extract(url)

    # Concatenate the subdomain and domain parts
    # domain = extracted_domain.subdomain + '.' + extracted_domain.domain + '.' + extracted_domain.suffix
    domain = extracted_domain.domain + '.' + extracted_domain.suffix
    print(domain)
    ip_address = socket.gethostbyname(domain)

    # Réalise un reverse DNS en utilisant le module "socket"
    reverse_dns = socket.gethostbyaddr(ip_address)

    # Réalise un whois en utilisant le module "ipwhois"
    ipwhois = IPWhois(ip_address)
    whois = ipwhois.lookup_rdap()

    redirections = analyse_redirections(url)

    return templates.TemplateResponse("response.html", {
        "request": request,
        "url": url,
        "reverse_dns": reverse_dns,
        "whois": whois,
        "analyse_redirections": redirections
    })
