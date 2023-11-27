from flask import request, jsonify
from helpers import donations
from databaseService import DatabaseService
from datetime import datetime

class PaymentController:
    def __init__(self):
        self.paymentService = DatabaseService(donations)

    def process_donation(self):
        data = request.get_json()
        data['createdAt'] = datetime.now()
        self.paymentService.create(data)
        #with email service, we can send appreciation mail to donor.
        successresponse = {}
        successresponse["success"] = True
        successresponse["error"] = None
        successresponse["message"] = "Payment Successful"

        return jsonify(successresponse), 201
        

    