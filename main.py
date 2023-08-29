from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from passlib.context import CryptContext


import models
from database import Database

image_path = "./image/" 


###################################################################################################################
#           MAIN PART
###################################################################################################################
app = FastAPI()
database = Database()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

# sign up
@app.get("/")
async def check():
    return ["this note tell you that you successfully connect to the api"]

@app.post("/login")
async def check():
    return ["this note tell you that you successfully connect to the api"]
'''
@app.post("/signup")
async def signup(user: models.UserIn, response: Response):
    hashed_password = get_password_hash(user.password)
    query = users_table.insert().values(username=user.username, hashed_password=hashed_password)
    user_id = await database.execute(query)
    token = f"user-{user_id}"  # Create a token (implement more secure way)
    response.set_cookie(key="Authentication", value=token)
    return {"message": "User created successfully"}
'''
#search
@app.get('/searchresults/{id}', tags=['Search Results'])
async def searchResults(keyword:str):
    '''return list as a result of matching information'''
    return database.getSearchResult(keyword)

# API endpoint to create a booking
@app.post("/bookings/", response_model=models.Booking)
def create_booking(booking: models.Booking):
    return database.postBooking(booking)

# API endpoint to get the list of bookings for a specific customer (mentee)
@app.get("/bookings/customer/{customer_id}")
def get_bookings_by_customer(customer_id: str):
    return database.getListBookingMentee(customer_id)

# API endpoint to get the list of bookings for a specific mentor (tutor)
@app.get("/bookings/mentor/{mentor_id}")
def get_bookings_by_mentor(mentor_id: str):
    return database.getListBookingMentor(mentor_id)

# API endpoint to update the details of a specific booking by mentor
@app.put("/bookings/{booking_id}", response_model=models.Booking)
def update_booking_by_mentor(updated_booking: models.Booking):
    return database.putBooking(updated_booking)


#uvicorn main:app --host localhost --port 8000
print(database.getSearchResult('business'))