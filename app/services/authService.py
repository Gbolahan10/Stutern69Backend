import bcrypt
from flask import jsonify
from status import Error
from datetime import datetime, timedelta
import jwt, re, random

class AuthService:
    def __init__(self):
        pass

    def validate_email(self, email):   
        pattern = "^[a-zA-Z0-9-_.]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
        if re.match(pattern, email):
            return True
        return False

    def hashPassword(self, password):
        try:
            byte_pwd = password.encode('utf-8')
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(byte_pwd, salt)
            return hashed_password
        except:
            return jsonify(Error('Error: 201 failed to hash password').result(), 500)


    def createToken(self, user_id, secret, valid_days):
        payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=valid_days)
        }
        token = jwt.encode(payload, secret, 'HS256')
        
        return token

    def verify_token(self, token, secretKey):
        try:
            try:
                verificationResponse = jwt.decode(token, secretKey, algorithms=['HS256'])
            except:
                return Error('Invalid token').result(), 400
            
            exp_time = datetime.fromtimestamp(verificationResponse['exp'])
            if datetime.now() > exp_time:
                return Error('Authorization Token is expired').result(), 401
            
            user_id = verificationResponse['user_id']
            return user_id
        
        except Exception as e:
            return Error(f'Wrong Authentication token - {e}').result(), 500

    def generateOTP(numOfDigits):
        status_code = 500
        try:
            otp = f'{random.randrange(1, 10**numOfDigits):0{numOfDigits}}'
            return otp
        except Exception as e:
            return Error(f"Error: {e}, Couldn't generate OTP").result(), status_code