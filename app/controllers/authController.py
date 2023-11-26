import bcrypt
from config import TOKEN_SECRET_KEY, REFRESH_SECRET_KEY
from flask import jsonify
from authService import AuthService
from databaseService import DatabaseService
from helpers import users
from status import Error
from datetime import datetime
import uuid, random
from authMiddleware import validate_required_fields


class AuthController:
    def __init__(self):
        self.authService = AuthService()
        self.userService = DatabaseService(users)

    def generate_username(self, first_name, numOfDigits):
        print("gen username")
        while True:
            random_number = f'{random.randrange(1, 10**numOfDigits):0{numOfDigits}}'
            username = f"{first_name}{random_number}"
            if self.userService.find({"username": username})['status'] == False:
                return username

    @validate_required_fields(['parentFirstName', 'parentLastName', 'parentEmail', 'consentGiven', 'childFirstName', 'childLastName', 'childAge', 'gender', 'password'])
    def register_user(self, request_data):
        try:
            data_dict = {}
            
            if self.authService.validate_email(request_data['parentEmail']) == False:
                return Error(f"parent's ${request_data['email']} is not a valid email address").result(), 400

            parental_consent = request_data['consentGiven']

            if parental_consent == False:
                return Error(f"No Consent given. Can't proceed with sign-up").result(), 400
            parental_consent = True
            print("1 generated")
            
            uid = str(uuid.uuid4())
            pwd = request_data['password']
            hashed_password = self.authService.hashPassword(pwd)
            print("2 generated")
            childFirstName = request_data['childFirstName']
            username = self.generate_username(childFirstName, 4)

            print("username generated")
            
            data = {
                'parentFirstName': request_data['parentFirstName'],
                'parentLastName': request_data['parentLastName'],
                'parentEmail': request_data['parentEmail'],
                'consentGiven': parental_consent,
                'childFirstName': request_data['childFirstName'],
                'childLastName': request_data['childLastName'],
                'password': hashed_password,
                'username': username,
                'createdAt': datetime.utcnow(),
                'lastUpdated': datetime.utcnow(),
            }
            
            try:
                self.userService.create(data)
            except:
                return Error("Database Error: 201").result(), 500

            data_dict['user'] = self.userService.find({"username": username}, {'_id': False, 'password': False})['result']

            successresponse = {}
            successresponse["success"] = True
            successresponse["error"] = None
            successresponse["message"] = "Sign-up Successful"
            successresponse["data"] = data_dict

            return jsonify(successresponse), 201
        except:
            return jsonify(Error('Internal Server Error').result()), 500

    
    @validate_required_fields(['username', 'password'])
    def login(self, request_data):
        data_dict = {}

        user = self.userService.find({"username": request_data['username']})
        
        if not user['status']:
            return Error('User not found. Please sign up.').result(), 404

        user_data = user['result']
        
        psswd = request_data['password']
        hash = psswd.encode('utf-8')
        if( bcrypt.checkpw(hash, user_data['password']) == False):
            return jsonify( Error('Wrong username/password combination').result()), 400

        print(user_data)
        data_dict['token'] = self.authService.createToken(str(user_data['_id']), TOKEN_SECRET_KEY, 365)
        data_dict['refresh_token'] =  self.authService.createToken(str(user_data['_id']), REFRESH_SECRET_KEY, 366)
        user_data.pop("password")
        user_data.pop("_id")
        data_dict['user'] = user_data
        
        
        successresponse = {}
        successresponse["success"] = True
        successresponse["error"] = None
        successresponse["message"] = "Login Successful"
        successresponse["data"] = data_dict

        return jsonify(successresponse), 201