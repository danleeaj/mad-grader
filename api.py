from flask import Flask, jsonify
from flask_restful import Api, Resource

from main import debate

app = Flask(__name__)
api = Api(app)

class Debate(Resource):
    def get(self, rubric_component, student_response, context=None):
        return jsonify(debate(rubric_component, student_response, context, jsonify=True))

api.add_resource(Debate, "/debate/<string:rubric_component>/<string:student_response>", "/debate/<string:rubric_component>/<string:student_response>/<string:context>")

if __name__ == "__main__":
    app.run(debug=True)