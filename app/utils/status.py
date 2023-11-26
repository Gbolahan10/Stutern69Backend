class Status():
    def __init__(self):
        self.requestStatus = False
        self.message = None
        self.response = None

    def result(self):
        response_dict = {}
        response_dict['success'] = self.requestStatus
        response_dict['message'] = self.message
        response_dict['data'] = self.response

        return response_dict


class Error(Status):
    def __init__(self, failure_message):
        self.message = failure_message
        self.requestStatus = False
        self.response = None    

class Success(Status):
    def __init__(self, response):
        self.message = "Successful"
        self.requestStatus = True
        self.response = response    
    