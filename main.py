import uvicorn
import psycopg
import os
from psycopg.rows import dict_row
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
# ports: 8150 - 8159
PORT=8151

# Load environment variables from .env file
load_dotenv()
DB_URL = os.getenv("DB_URL")
conn = psycopg.connect(DB_URL, autocommit=True, row_factory=dict_row)

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get("/hotel_rooms")
def hotel_rooms():
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM hotel_rooms")
        hotel_rooms = cur.fetchall()
        return hotel_rooms

@app.get("/temp")
def temp():
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM messages")
        messages = cur.fetchall()
        return messages

rooms =  [

    {
        "room" : 1001,
        "class": "A",
        "price": 150
    },
    
    {
        "room" : 1002,
        "class": "B",
        "price": 90
    },
    
    { 
        "room" : 1003,
        "class": "C",
        "price": 70
    }

]

# Get all rooms
@app.get("/rooms")
def get_all_rooms():

    return rooms

# Get one room
@app.get("/rooms/{id}")
def get_one_room(id: int):
    try:
        return rooms[id]
    except:
        return {"error": "Room not found"}

# 
@app.post("/bookings")
def create_booking(request: Request):
    return { "msg": "Booking created successfully" }

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=PORT,
        ssl_keyfile="/etc/letsencrypt/privkey.pem",
        ssl_certfile="/etc/letsencrypt/fullchain.pem",
    )
