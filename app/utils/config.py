from os import environ

SECRET_KEY = environ.get('SECRET_KEY')
TOKEN_SECRET_KEY = "JWT_SECRET_*_+"
REFRESH_SECRET_KEY = "JWT_REFRESH_SECRET_*_+"
FLASK_ENV = 'development'
DEBUG = True
TESTING = True
DATABASE_URI = 'mongodb+srv://gbolahan2454:IWGDW7gvIcteCvOk@cluster0.mcqnmyz.mongodb.net/stutern69?retryWrites=true&w=majority'
