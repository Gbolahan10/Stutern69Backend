from waitress import serve
import os

class FlaskApplication:
    def __init__(self, app, configFile):
        self.app = app
        self.app.config.from_pyfile(configFile)

    def add_endpoint(self, endpoint, function_pointer, methods = None):
        endpoint_name = f'Route-{endpoint}'

        if(methods == None):
            methods = ["GET", "POST", "PUT", "DELETE", "PATCH"]
            
        self.app.add_url_rule(endpoint, endpoint_name, function_pointer, methods=methods)

    def run(self, hosts):
        
        port = int(os.environ.get("PORT", 5000))

        if(self.app.config['FLASK_ENV'] == "development"):
            self.app.run(host=hosts, port=port)

        if(self.app.config['FLASK_ENV'] == "production"):
            serve(self.app, host=hosts, port=port)
