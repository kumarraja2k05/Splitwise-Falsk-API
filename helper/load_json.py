import json

class JsonLoader:
    def load_owner_json(self):
        with open('schemas\owner_schema.json') as file:
            data = json.load(file)
            return data
        
    def load_group_json(self):
        with open('schemas\group_schema.json') as file:
            data = json.load(file)
            return data
        
    def load_expense_json(self):
        with open('schemas\expense_schema.json') as file:
            data = json.load(file)
            return data