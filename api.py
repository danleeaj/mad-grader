from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

class Debate(Resource):
    def get(self, name):
        return {"data": f"Get world, {name}"}
    def post(self, name):
        return {"data": f"{name}, post world"}

api.add_resource(Debate, "/debate/<string:name>")

if __name__ == "__main__":
    app.run(debug=True)