from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

import models
from database import Database

print("Hello")

image_path = "./image/"

# import firebase_admin
# from firebase_admin import credentials, firestore
#
# cred = credentials.Certificate("service.json")
# firebase_admin.initialize_app(cred)
# db = firestore.client()
# doc_ref = db.collection("users").document("alovelace")
# doc_ref.set({"first": "Ada", "last": "Lovelace", "born": 1815})


#               CONNECTION TO DATABASE
# def database_connection(
#     server: str = "localhost",
#     database: str = "Caucheez",
#     username: str = "sa",
#     password: str = "12345@bcdE",
# ):
#     """
#     call this function to connect to database
#     this function return pyodbc.connect
#     """
#     return pyodbc.connect(
#         "DRIVER={ODBC Driver 17 for SQL Server};\
#                             SERVER="
#         + server
#         + ";\
#                             DATABASE="
#         + database
#         + ";\
#                             UID="
#         + username
#         + ";PWD="
#         + password
#         + ";"
#     )


# def database_connection2(server:str='TRONGNHAN', database:str='Plooker'):
#     '''
#     call this function to connect to database
#     this function return pyodbc.connect
#     '''
#     return pyodbc.connect('DRIVER={SQL Server};\
#                             SERVER='+server+';\
#                             DATABASE='+database+';\
#                             UID='+username+';PWD='+password+';')


# def database_connection2(server: str = "localhost", database: str = "Caucheez"):
#     """
#     call this function to connect to database
#     this function return pyodbc.connect
#     """
#     return pyodbc.connect(
#         "DRIVER={SQL Server};\
#                             SERVER="
#         + server
#         + ";\
#                             DATABASE="
#         + database
#         + ";\
#                             Trusted_Connection=yes;"
#     )


# #               DATABASE COMMAND
# class Database:
#     def __init__(self):
#         self.conn = database_connection2()
#         self.cursor = self.conn.cursor()
#         pass
#
#     # get Mentor Info by Rating - display mentor info, sort in descending order of rating
#     def getMentorInfoByRating(self, data: MentorInfo) -> list:
#         command = "EXEC sp_getMentorInfoByRating"
#         try:
#             self.cursor.execute(command)
#         except:
#             return "SOME ERROR OCCUR"
#         result = []
#         for i in self.cursor:
#             result.append([x for x in i])
#         return result
#
#     # get Field - display field name and number of mentor in each field, sort in descending order
#     def getFeild(self, data: Field) -> list:
#         command = "EXEC sp_getFeild "
#         try:
#             self.cursor.execute(command)
#         except:
#             return "SOME ERROR OCCUR"
#         result = []
#         for i in self.cursor:
#             result.append([x for x in i])
#         return result
#
#     # get Mentor by Field - display all the mentor in that field
#     def getMentorByFeild(self, data: Field) -> list:
#         command = "EXEC sp_getMentorByFeild '%s'" % (data.fieldName)
#         try:
#             self.cursor.execute(command)
#         except:
#             return "SOME ERROR OCCUR"
#         result = []
#         for i in self.cursor:
#             result.append([x for x in i])
#         return result
#
#     # get search - input: keyword, output: mentor profile containing that keyword
#     def getSearchResult(self, data) -> list:
#         command = "EXEC sp_search '%s'" % (data)
#         try:
#             self.cursor.execute(command)
#         except:
#             return "SOME ERROR OCCUR"
#         result = []
#         for i in self.cursor:
#             result.append([x for x in i])
#         return result
#
#     # check Login Information
#     def checkLogin(self, username: str, password: str) -> str:
#         command = "EXEC sp_checkLogin '" + username + "', '" + password + "'"
#         try:
#             result = ""
#             self.cursor.execute(command)
#             print("hello")
#             for i in self.cursor:
#                 result += i[0]
#             return result
#         except:
#             return "SOME ERRORS OCCUR"
#
#     # sign up
#     def signup(self, account: AccountInfo, user: UserInfo) -> str:
#         command_addaccount = "EXEC sp_AddAccount '%s', '%s', '%s'" % (
#             account.username,
#             account.password,
#         )
#         command_adduser = "EXEC sp_AddUser '%s', '%s', '%s', '%s', '%s', '%s', '%b'" % (
#             user.fname,
#             user.lname,
#             user.email,
#             user.phone,
#             user.dob,
#             user.country,
#             user.gender,
#             "Mentee",
#         )
#         try:
#             self.cursor.execute(command_addaccount)
#             id = []
#             for i in self.cursor:
#                 id.append([e for e in i])
#             self.cursor.execute(command_adduser)
#             self.conn.commit()
#         except:
#             return "FAIL TO SIGN UP"
#         return "SUCCESS"


"""
    def root(self, data:str) -> list:
        command = 'EXEC findTable \'' + data.lower() + '\''
        self.cursor.execute(command)
        result = []
        for i in self.cursor:
            result.append([x for x in i])
        return result

    def changeUserInfo(self, user: UserInfo):
        command = "EXEC changeUserInfo '%s'" % (user.userid, user.Name, user.usename, user.userPhone, user.userMail, user.userPWD, 1 if user.gender else 0, user.dob, user.userAddress)
        try:
            self.cursor.execute(command)
            self.conn.commit()
        except:
            return 'FAIL'
        return 'SUCCESS'

    #sign up
    def signup(self, user: AccountInfo) -> str:
        id = user.userID
        command = 'EXEC sp_AddUsers \''+id+'\', \''+user.Name+'\', \''+user.usename+'\',\''+user.userPhone+'\', \''+user.userMail+'\', \''+user.userPWD+'\','+str(user.gender)+', \''+user.dob+'\', \''+user.userAddress+'\''
        try:
            self.cursor.execute(command)
            self.conn.commit()
        except:
            return 'FAIL TO SIGN UP'
        return 'SUCCESS'

    def login(self, username:str, password:str) -> str:
        #return username
        command = 'EXEC sp_checkLogIn \''+username+'\', \''+password+'\''
        try:
            result = ''
            self.cursor.execute(command)
            print("hello")
            for i in self.cursor:
                result += i[0]
        except:
            return 'SOME ERRORS OCCUR'

        if result != 'None':
            return result
        else: return 'FAIL'

    def all(self):
        command = 'EXEC SearchAll'
        try:
            self.cursor.execute(command)
            result = []
            for i in self.cursor:
                result.append([e for e in i])
            return result
        except:
            return 'FAIL'

    def getUserInfo(self, id:dict):
        id = id['id']
        command = "EXEC getUserInfo '"+id+"'"
        try:
            self.cursor.execute(command)
            result = 0
            for i in self.cursor:
                result = [e for e in i]
            return result
        except:
            return 'NO USER'
"""
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


@app.post("/sign_up", tags=["account"])
async def sign_up(account: models.SignUpSchema) -> str:
    try:
        uid = database.create_new_account(account.email, account.password, 0)
        return JSONResponse(content={"success": "true", "data": {"uid": uid}})
    except Exception as e:
        return JSONResponse(
            content={"success": "failed", "data": {"message": f"Error: {str(e)}"}}
        )

    """
    RETURN 'SUCCESS' IF SUCCESSFULLY SIGN UP USER
    IF ERROR OCCUR THEN RETURN 'FAIL TO SIGN UP'

    example input:
    {
    "userid": "string",
    "Name": "Name",
    "usename": "testUser",
    "userPhone": "0912345678",
    "userMail": "gmail@gmail.com",
    "userPWD": "123",
    "gender": 0,
    "dob": "1-1-2000",
    "userAddress": "HCMC"
    }
    """
    # return database.signup(account)
    return ""


# login
@app.post("/login", tags=["account"])
async def login(payload: models.SignUpSchema) -> str:
    try:
        user_info = database.login(payload.email, payload.password)
        return JSONResponse(
            content={"success": "true", "data": {"user_info": user_info}}
        )
    except Exception as e:
        return JSONResponse(
            content={"success": "failed", "data": {"message": f"Error: {str(e)}"}}
        )

    return ""
    # return database.login(username, password)
