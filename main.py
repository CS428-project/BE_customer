from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

import pyodbc
import models
# from database import Database

image_path = "./image/"


#               CONNECTION TO DATABASE
def database_connection():
#     """
#     call this function to connect to database
#     this function return pyodbc.connect
#     """
    return pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=mssql-138433-0.cloudclusters.net,18705;"
            "PORT=18705;"
            "DATABASE=eCommerce;"
            "UID=Admin;"
            "PWD=Admin123"
    )


#               DATABASE COMMAND
class Database:
    def __init__(self):
        self.conn = database_connection()
        self.cursor = self.conn.cursor()
        pass
 
    # get Mentor Info by Rating - display mentor info, sort in descending order of rating
    def getMentorInfoByRating(self, data: models.MentorInfo) -> list:
        command = "EXEC sp_getMentorInfoByRating"
        try:
            self.cursor.execute(command)
        except:
            return "SOME ERROR OCCUR"
        result = []
        for i in self.cursor:
            result.append([x for x in i])
        return result

    # get Field - display field name and number of mentor in each field, sort in descending order
    def getField(self) -> list:
        command = "EXEC sp_getFeild "
        try:
            self.cursor.execute(command)
        except:
            return "SOME ERROR OCCUR"
        result = []
        for i in self.cursor:
            result.append([x for x in i])
        return result

    # get Mentor by Field - display all the mentor in that field
    def getMentorByField(self, data: models.Field) -> list:
        command = "EXEC sp_getMentorByFeild '%s'" % (data.fieldName)
        try:
            self.cursor.execute(command)
        except:
            return "SOME ERROR OCCUR"
        result = []
        for i in self.cursor:
            result.append([x for x in i])
        return result

    # get search - input: keyword, output: mentor profile containing that keyword
    def getSearchResult(self, keyword: str) -> list:
        command = "EXEC sp_Search '%s'" % (keyword)
        try:
            self.cursor.execute(command)
        except:
            return "SOME ERROR OCCUR"
        result = []
        for i in self.cursor:
            result.append([x for x in i])
        return result

    # check Login Information
    def checkLogin(self, username: str, password: str) -> str:
        command = "EXEC sp_checkLogin '" + username + "', '" + password + "'"
        try:
            result = ""
            self.cursor.execute(command)
            print("hello")
            for i in self.cursor:
                result += i[0]
            return result
        except:
            return "SOME ERRORS OCCUR"

    # sign up
    def signup(self, account: models.AccountInfo, user: models.UserInfo) -> str:
        command_addaccount = "EXEC sp_AddAccount '%s', '%s', '%s'" % (
            account.username,
            account.password,
        )
        command_adduser = "EXEC sp_AddUser '%s', '%s', '%s', '%s', '%s', '%s', '%b'" % (
            user.fname,
            user.lname,
            user.email,
            user.phone,
            user.dob,
            user.country,
            user.gender,
            "Mentee",
        )
        try:
            self.cursor.execute(command_addaccount)
            id = []
            for i in self.cursor:
                id.append([e for e in i])
            self.cursor.execute(command_adduser)
            self.conn.commit()
        except:
            return "FAIL TO SIGN UP"
        return "SUCCESS"

    #booking
    def postBooking(self, info: models.Booking) -> str:
        command = "EXEC sp_postBooking '%s', '%s', '%s', '%s', '%s', '%s'" % (info.ID, info.mentorID, info.menteeID, info.book_at, info.time, info.status)
        try:
            result = ""
            self.cursor.execute(command)
            for i in self.cursor:
                result += i[0]
            self.conn.commit()
        except:
            return "SOME ERRORS OCCUR"
        return "SUCCESS"
    
    
    
    # get mentee booking
    def getListBookingMentee(self, menteeid: str) -> list:
        command = "EXEC sp_getListBookingMentee '%s'" % (menteeid)
        try:
            self.cursor.execute(command)
        except:
            return "SOME ERROR OCCUR"
        result = []
        for i in self.cursor:
            result.append([x for x in i])
        return result
    
        # get mentor booking
    def getListBookingMentor(self, mentorid: str) -> list:
        command = "EXEC sp_getListBookingMentor '%s'" % (mentorid)
        try:
            self.cursor.execute(command)
        except:
            return "SOME ERROR OCCUR"
        result = []
        for i in self.cursor:
            result.append([x for x in i])
        return result
    
    # put mentor booking (update sessions can be booked)
    def putBooking(self, booking:models.Booking) -> list:
        command = "EXEC sp_putBooking '%s', '%s', '%s', '%s'" % (booking.mentorID, booking.menteeID, booking.book_at, booking.time)
        try:
            self.cursor.execute(command)
            self.conn.commit()
            return "BOOKING SUCCESSFULLY"
        except:
            return "SOME ERROR OCCUR"

    


###################################################################################################################
#           MAIN PART
###################################################################################################################
app = FastAPI()
database = Database()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# sign up
@app.get("/")
async def check():
    return ["this note tell you that you successfully connect to the api"]

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
