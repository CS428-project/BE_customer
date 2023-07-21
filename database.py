import firebase_admin
from firebase_admin import auth, credentials, firestore

from models import UserInfo

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

    def create_new_account(self, email: str, password: str, role: bool) -> str:
        try:
            user = auth.create_user(email=email, password=password)
            user_doc_ref = self.database.collection("users").document(user.uid)
            # TODO: SET Email as data for that user and some basic infor as default.
            user_doc_ref.set(
                {
                    "userID": user.uid,
                    "email": email,
                    "role": role,
                }
            )
            return user.uid
        except:
            raise Exception("Email already usage")

    def login(self, email: str, password: str) -> UserInfo:
        try:
            # Authenticate user using Firebase Authentication
            user = auth.get_user_by_email(email)
            auth.verify_password(password, user)

            # Fetch account data from Firejtore
            user_doc_ref = self.database.collection("users").document(user.uid)
            user_data = user_doc_ref.get().to_dict()
            return user_data
        except auth.AuthError as e:
            raise Exception(f"Authentication error: {e}")
        except Exception as e:
            raise Exception(f"Other error: {e}")

    # try:
    #     user = auth.create_user(email=email, password=password)
    #     return user.uid
    # except:
    #     raise Exception("Email already usage")

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
