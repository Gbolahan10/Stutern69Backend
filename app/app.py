from paymentController import PaymentController
from flask import Flask, render_template, request
from flask_cors import CORS
from flask_application import FlaskApplication
from authController import AuthController
import os

app = Flask(__name__, template_folder = 'templates')
CORS(app)

auth = AuthController()
payment = PaymentController()

CONFIG_FILE = 'config.py'

FlaskApp = FlaskApplication(app, CONFIG_FILE)

paystack_public_key = os.environ.get('PAYSTACK_PUBLIC_KEY')

#Static routes
FlaskApp.add_endpoint('/', lambda : "Server ok")
FlaskApp.add_endpoint('/auth/signin', auth.login, methods=["POST"])
FlaskApp.add_endpoint('/auth/signup', auth.register_user, methods=['POST'])
FlaskApp.add_endpoint('/wishes/donate', lambda : render_template('donate.html', paystack_public_key=paystack_public_key))
FlaskApp.add_endpoint('/wishes/process_donation', payment.process_donation, methods=["POST"])

FlaskApp.run('0.0.0.0')

