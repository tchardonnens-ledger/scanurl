from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .services.utils import *
from databases import Database
from sqlalchemy import create_engine, MetaData, Table, Column, String
import sqlalchemy
import json

DATABASE_URL = "sqlite:///./test.db"
database = Database(DATABASE_URL)
metadata = MetaData()

json_table = Table(
    "json_data",
    metadata,
    Column("id", sqlalchemy.Integer, primary_key=True),
    Column("content", String(2000)),
)

engine = create_engine(DATABASE_URL)
metadata.create_all(engine)

async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(lifespan=lifespan)

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

class JSONData(BaseModel):
    data: dict

@app.post("/log")
async def log_json(data: JSONData):
    json_str = json.dumps(data)
    query = json_table.insert().values(content=json_str)
    await database.execute(query)
    return {"message": "JSON logged successfully"}

@app.get("/json")
async def get_json():
    query = json_table.select()
    records = await database.fetch_all(query)
    return [{"id": record["id"], "content": json.loads(record["content"])} for record in records]

@app.get("/reset")
async def reset_db():
    query = json_table.delete()
    await database.execute(query)
    return {"message": "Database reset successfully"}