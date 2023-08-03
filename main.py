from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pyodbc
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
image_path = './image/'


#               CONNECTION TO DATABASE
def database_connection(server:str='localhost', database:str='Caucheez', username:str='sa', password:str='12345@bcdE'):
    '''
    call this function to connect to database
    this function return pyodbc.connect 
    '''
    return pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};\
                            SERVER='+server+';\
                            DATABASE='+database+';\
                            UID='+username+';PWD='+password+';')

# def database_connection2(server:str='TRONGNHAN', database:str='Plooker'):
#     '''
#     call this function to connect to database
#     this function return pyodbc.connect 
#     '''
#     return pyodbc.connect('DRIVER={SQL Server};\
#                             SERVER='+server+';\
#                             DATABASE='+database+';\
#                             UID='+username+';PWD='+password+';')

def database_connection2(server:str='localhost', database:str='Caucheez'):
    '''
    call this function to connect to database
    this function return pyodbc.connect
    '''
    return pyodbc.connect('DRIVER={SQL Server};\
                            SERVER='+server+';\
                            DATABASE='+database+';\
                            Trusted_Connection=yes;')

'''
class <classname>(BaseModel):
    <variable>: <type> = <value>
'''
#               STRUCTURE DEFINE
class AccountInfo(BaseModel):
    userID: str = '123456'
    username: str = 'ltnhan'
    password: str = 'Nhan123@'
    created_at: str = '01-01-2000'

class UserInfo(BaseModel):
    userID: str = '123456'
    fname: str = 'Le'
    lname: str = 'Nhan'
    email: str = 'ltnhan@gmail.com'
    phone: str = '0123456789'
    dob: str = '01-01-2000'
    country: str = 'Vietnam'
    gender: bool = 0 #0 male, 1 female
    role: bool = 0 #0 mentee, 1 mentor

class MentorInfo(BaseModel):
    mentorID: str = '123456'
    fieldID: str = '123456'
    language: str = 'English'
    description: str = 'Hello'
    rating: float = 1.5

class Field(BaseModel):
    fieldID: str = '123456'
    fieldName: str = 'business'

class Experience(BaseModel):
    userID: str = '123456'
    position: str = 'CEO'
    workplace: str = 'Google'
    startdate: str = '01-01-2023'
    enddate: str = '01-01-2025'

#               DATABASE COMMAND
class Database:
    def __init__(self):
        self.conn = database_connection2()
        self.cursor = self.conn.cursor()
        pass

    #get Mentor Info by Rating - display mentor info, sort in descending order of rating
    def getMentorInfoByRating(self, data: MentorInfo) -> list:
        command = "EXEC sp_getMentorInfoByRating"
        try:
            self.cursor.execute(command)
        except:
            return 'SOME ERROR OCCUR'
        result = []
        for i in self.cursor:
            result.append([x for x in i])
        return result
    
    #get Field - display field name and number of mentor in each field, sort in descending order
    def getFeild(self, data: Field) -> list:
        command = "EXEC sp_getFeild " 
        try:
            self.cursor.execute(command)
        except:
            return 'SOME ERROR OCCUR'
        result = []
        for i in self.cursor:
            result.append([x for x in i])
        return result
    
    #get Mentor by Field - display all the mentor in that field
    def getMentorByFeild(self, data: Field) -> list:
        command = "EXEC sp_getMentorByFeild '%s'" % (data.fieldName)
        try:
            self.cursor.execute(command)
        except:
            return 'SOME ERROR OCCUR'
        result = []
        for i in self.cursor:
            result.append([x for x in i])
        return result

    #get search - input: keyword, output: mentor profile containing that keyword
    def getSearchResult(self, data) -> list:
        command = "EXEC sp_search '%s'" % (data)
        try:
            self.cursor.execute(command)
        except:
            return 'SOME ERROR OCCUR'
        result = []
        for i in self.cursor:
            result.append([x for x in i])
        return result
    
    #check Login Information
    def checkLogin(self, username:str, password:str) -> str:
        command = 'EXEC sp_checkLogin \''+username+'\', \''+password+'\''
        try:
            result = ''
            self.cursor.execute(command)
            print("hello")
            for i in self.cursor:
                result += i[0]
        except:
            return 'SOME ERRORS OCCUR'
        
    #sign up
    def signup(self, account: AccountInfo, user: UserInfo) -> str:
        command_addaccount = "EXEC sp_AddAccount '%s', '%s', '%s'" % (account.username, account.password)
        command_adduser = "EXEC sp_AddUser '%s', '%s', '%s', '%s', '%s', '%s', '%b'" % (user.fname, user.lname, user.email, user.phone, user.dob, user.country, user.gender, "Mentee")
        try:
            self.cursor.execute(command_addaccount)
            id = []
            for i in self.cursor:
                id.append([e for e in i])
            self.cursor.execute(command_adduser)
            self.conn.commit()
        except:
            return 'FAIL TO SIGN UP'
        return 'SUCCESS'

###################################################################################################################
#           MAIN PART   
###################################################################################################################
app = FastAPI()
database = Database()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

#sign up
@app.get('/')
async def check():
    return ['this note tell you that you successfully connect to the api']

@app.post('/sign_up', tags=['account'])
async def sign_up(account:UserInfo) -> str:
    '''
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
    '''
    return database.signup(account)
    
#login
@app.post('/login', tags=['account'])
async def login(userinput:dict) -> str:
    username = userinput['user_name']
    password = userinput['password']
    return database.login(username,password)