import pyodbc
#               CONNECTION TO DATABASE
def database_connection():
#     """
#     call this function to connect to database
#     this function return pyodbc.connect
#     """
    return pyodbc.connect('DRIVER={SQL Server};SERVER=mssql-138433-0.cloudclusters.net,18705;PORT=18705;DATABASE=eCommerce;UID=Admin;PWD=Admin123')

import models
#               DATABASE COMMAND
class Database:
    def __init__(self):
        self.conn = database_connection()
        self.cursor = self.conn.cursor()
        pass
 
    # get Mentor Info by Rating - display mentor info, sort in descending order of rating
    def getMentorInfoByRating(self) -> list:
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
        command = "EXEC sp_getField"
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
        command = "EXEC sp_search '%s'" % (keyword)
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
        command = "EXEC sp_InsertBooking '%s', '%s', '%s', '%s', '%s', '%s'" % (info.mentorID, info.menteeID, info.book_at, info.time, info.status, info.duration, info.status,info.paymentID)
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
        command = "EXEC sp_putBooking '%s', '%s', '%s', '%s', '%s'" % (booking.mentorID, booking.menteeID, booking.book_at, booking.time, booking.status)
        try:
            self.cursor.execute(command)
            self.conn.commit()
            return "BOOKING SUCCESSFULLY"
        except:
            return "SOME ERROR OCCUR"

