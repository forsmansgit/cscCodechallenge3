import uvicorn
import psycopg
import os
from psycopg.rows import dict_row
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import date
# ports: 8150 - 8159
PORT=8151

# Load environment variables from .env file
load_dotenv()
DB_URL = os.getenv("DB_URL")
conn = psycopg.connect(DB_URL, autocommit=True, row_factory=dict_row)

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

#datamodell som ska valideras
class booking(BaseModel):
    guest_id: int
    room_id: int
    datefrom: date
    dateto: date

@app.get("/if/{user_input}")
def if_(user_input: str):
    message = None # same as Null
    if user_input == "hello":
        message = "Hello, world!"
    elif user_input == "goodbye":
        message = "Goodbye, world!"
    else:
        message = f"Unknown input: {user_input}"
        
    return {"msg": message}

@app.get("/hotel_rooms")
def hotel_rooms():
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM hotel_rooms")
        hotel_rooms = cur.fetchall()
        return hotel_rooms

#@app.get("/temp")
#def temp():
#    with conn.cursor() as cur:
#        cur.execute("SELECT * FROM hotel_rooms ORDER BY room_number")
#        rooms = cur.fetchall()
#        return rooms

# Get all rooms
@app.get("/rooms/{id}")
def get_one_room(id: int):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM hotel_rooms WHERE id = %s", [id])
        #cur.execute("SELECT * FROM hotel_rooms WHERE %s", (id,))
        #cur.execute("SELECT * FROM hotel_rooms WHERE iid = %(id)s", {"id": id})
        rooms = cur.fetchall()
        return rooms
    
# bookings
@app.post("/bookings")
def create_booking(booking: booking):
    with conn.cursor() as cur:
        cur.execute("""INSERT INTO hotel_bookings (guest_id, room_id, datefrom, dateto) 
        VALUES (%s,%s, %s, %s) 
        RETURNING id""", 
        (booking.guest_id, booking.room_id, booking.datefrom, booking.dateto))
        booking_id = cur.fetchone()['id']
    return {"msg": "Booking Created", "booking_id": booking_id}


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=PORT,
        ssl_keyfile="/etc/letsencrypt/privkey.pem",
        ssl_certfile="/etc/letsencrypt/fullchain.pem",
    )
