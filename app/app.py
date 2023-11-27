from flask import Flask, render_template, request
from flask_cors import CORS
from flask_application import FlaskApplication
from authController import AuthController

app = Flask(__name__, template_folder = 'templates')
CORS(app)

auth = AuthController()

CONFIG_FILE = 'config.py'

FlaskApp = FlaskApplication(app, CONFIG_FILE)

#Static routes
FlaskApp.add_endpoint('/', lambda : "Server ok")
FlaskApp.add_endpoint('/auth/signin', auth.login, methods=["POST"])
FlaskApp.add_endpoint('/auth/signup', auth.register_user, methods=['POST'])


FlaskApp.run('0.0.0.0')

