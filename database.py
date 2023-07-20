import firebase_admin
from firebase_admin import auth, credentials, firestore

# cred = credentials.Certificate("service.json")
# firebase_admin.initialize_app(cred)
# db = firestore.client()
# doc_ref = db.collection("users").document("alovelace")
# doc_ref.set({"first": "Ada", "last": "Lovelace", "born": 1815})


#               DATABASE COMMAND
class Database:
    def __init__(self):
        cred = credentials.Certificate("service.json")
        firebase_admin.initialize_app(cred)
        self.database = firestore.client()
        # self.conn = database_connection2()
        # self.cursor = self.conn.cursor()
        pass

    def create_new_account(self, email: str, password: str) -> str:
        try:
            user = auth.create_user(email=email, password=password)
            return user.uid
        except:
            raise Exception("Email already usage")

    # # get Mentor Info by Rating - display mentor info, sort in descending order of rating
    # def getMentorInfoByRating(self, data: MentorInfo) -> list:
    #     command = "EXEC sp_getMentorInfoByRating"
    #     try:
    #         self.cursor.execute(command)
    #     except:
    #         return "SOME ERROR OCCUR"
    #     result = []
    #     for i in self.cursor:
    #         result.append([x for x in i])
    #     return result
    #
    # # get Field - display field name and number of mentor in each field, sort in descending order
    # def getFeild(self, data: Field) -> list:
    #     command = "EXEC sp_getFeild "
    #     try:
    #         self.cursor.execute(command)
    #     except:
    #         return "SOME ERROR OCCUR"
    #     result = []
    #     for i in self.cursor:
    #         result.append([x for x in i])
    #     return result
    #
    # # get Mentor by Field - display all the mentor in that field
    # def getMentorByFeild(self, data: Field) -> list:
    #     command = "EXEC sp_getMentorByFeild '%s'" % (data.fieldName)
    #     try:
    #         self.cursor.execute(command)
    #     except:
    #         return "SOME ERROR OCCUR"
    #     result = []
    #     for i in self.cursor:
    #         result.append([x for x in i])
    #     return result
    #
    # # get search - input: keyword, output: mentor profile containing that keyword
    # def getSearchResult(self, data) -> list:
    #     command = "EXEC sp_search '%s'" % (data)
    #     try:
    #         self.cursor.execute(command)
    #     except:
    #         return "SOME ERROR OCCUR"
    #     result = []
    #     for i in self.cursor:
    #         result.append([x for x in i])
    #     return result
    #
    # # check Login Information
    # def checkLogin(self, username: str, password: str) -> str:
    #     command = "EXEC sp_checkLogin '" + username + "', '" + password + "'"
    #     try:
    #         result = ""
    #         self.cursor.execute(command)
    #         print("hello")
    #         for i in self.cursor:
    #             result += i[0]
    #         return result
    #     except:
    #         return "SOME ERRORS OCCUR"
    #
    # # sign up
    # def signup(self, account: AccountInfo, user: UserInfo) -> str:
    #     command_addaccount = "EXEC sp_AddAccount '%s', '%s', '%s'" % (
    #         account.username,
    #         account.password,
    #     )
    #     command_adduser = "EXEC sp_AddUser '%s', '%s', '%s', '%s', '%s', '%s', '%b'" % (
    #         user.fname,
    #         user.lname,
    #         user.email,
    #         user.phone,
    #         user.dob,
    #         user.country,
    #         user.gender,
    #         "Mentee",
    #     )
    #     try:
    #         self.cursor.execute(command_addaccount)
    #         id = []
    #         for i in self.cursor:
    #             id.append([e for e in i])
    #         self.cursor.execute(command_adduser)
    #         self.conn.commit()
    #     except:
    #         return "FAIL TO SIGN UP"
    #     return "SUCCESS"
