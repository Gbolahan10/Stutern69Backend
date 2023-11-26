from authService import AuthService
from databaseService import DatabaseService
from status import Error
from flask import request
from functools import wraps
import jwt
from flask import request, jsonify
from config import TOKEN_SECRET_KEY
from datetime import datetime
from helpers import users

def validate_required_fields(required_fields):
    def decorator(func):
        def wrapper(*args, **kwargs):
            missing_fields = []
            data = request.get_json()
            for field in required_fields:
                if field not in data or not data[field]:
                    missing_fields.append(field)
            if missing_fields:
                return Error(f"Missing required field: {', '.join(missing_fields)}").result(), 400 
            return func(*args, **kwargs, request_data=data)
        return wrapper
    return decorator

def validate_approved_fields(approved_fields):
    def decorator(func):
        def wrapper(*args, **kwargs):
            unapproved_fields = []
            data = request.get_json()
            for field in data:
                if field not in approved_fields:
                    unapproved_fields.append(field)
            if unapproved_fields:
                return Error(f"Request body contains unapproved field: {', '.join(unapproved_fields)}").result(), 400 
            return func(*args, **kwargs)
        return wrapper
    return decorator


def verify_authentication(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split("Bearer ")[1]
        if not token:
            return Error("Authentication token missing").result(), 401
        try:
            response = jwt.decode(token, TOKEN_SECRET_KEY, algorithms=['HS256'])
            
            current_user = users.find_one({"user_id": response['user_id']}, {'_id': False, 'password': False})
            
            if current_user == None:
                return Error("Invalid Authentication token!").result(), 401

            exp_time = datetime.fromtimestamp(response['exp'])
            if datetime.now() > exp_time:
                return jsonify({"message":'Authorization Token is expired'}),401

            if current_user["verified_email"]== False:
                return Error("User hasn't verified email, therefore restricted.").result(), 401
        except Exception as e:
            return Error(f"Invalid Authentication token! - {e}").result(), 500

        return f(current_user, *args, **kwargs)

    return decorated