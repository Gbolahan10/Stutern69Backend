class DatabaseService:
    def __init__(self, model):
        self.Model = model
    
    def find(self, query, optional=None):
        try:
            result = self.Model.find_one(query, optional)
            if result:
                return {"status": True, "result": result }
            else:
                return {"status": False, "result": result }
        except Exception as e:
            return {"status": False, "error": e }

    def findAll(self, query, optional=None):
        try:
            result = self.Model.find(query, optional)
            result_list = list(result.clone())

            if len(result_list) > 0:
                return {"status": True, "result": result}
            else:
                return {"status": False, "result": result}
        except Exception as e:
            return {"status": False, "error": e }

    def create(self, payload):
        try:
            result = self.Model.insert_one(payload)
            return {"status": True, "result": result }
        except Exception as e:
            return {"status": False, "error": e }

    def update(self, query, payload):
        try:
            result = self.Model.update_one(query, payload)
            return {"status": True, "result": result }
        except Exception as e:
            return {"status": False, "error": e }
        
    def delete_one(self, query):
        try:
            self.Model.delete_one(query)
            return {"status": True}
        except Exception as e:
            return {"status": False, "error": e }

    def count_documents(self, query):
        try:
            result = self.Model.count_documents(query)
            return {"status": True,  "result": result}
        except Exception as e:
            return {"status": False, "error": e }

    def update_one(self, query, payload):
        try:
            result = self.Model.update_one(query, payload)
            if result.modified_count > 0:
                return {"status": True,  "result": result}
            else:
                return {"status": False,  "result": result}
        except Exception as e:
            return {"status": False, "error": e }
