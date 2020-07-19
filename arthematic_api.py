from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)

# DATABASE CONNECTION MONGODB
client = MongoClient('mongodb://localhost:27017/')
db = client.test_database
UserNum = db["username"]

UserNum.insert({
    'no_of_users': 0
})


class visit(Resource):
    def get(self):
        prev_num = UserNum.find({})[0]['no_of_users']
        new_number = prev_num + 1
        UserNum.update({}, {"$set": {'no_of_users': new_number}})
        return str("Hello user " + str(new_number))
# client.server.info()


def checkpostedData(postdData, function_name):
    if(function_name == 'Add' or function_name == 'Subtract' or function_name == "multiply"):
        if "x" not in postdData or "y" not in postdData:
            return 301
        else:
            return 200

    elif(function_name == 'Division'):
        if 'x' not in postdData or 'y' not in postdData:
            return 301
        elif postdData["y"] == 0:
            return 302
        else:
            return 200


class Add(Resource):
    def post(self):
        postres = request.get_json()

        status_code = checkpostedData(postres, "Add")
        if(status_code != 200):
            jresp = {
                'Message': "One value not supplied!",
                'Status_code': status_code
            }
            return jsonify(jresp)

        x = postres["x"]
        y = postres["y"]
        x = int(x)
        y = int(y)

        result = x+y
        resmap = {
            'message': result,
            'status': 200
        }
        return jsonify(resmap)


class Subtract(Resource):
    def post(self):

        postdata = request.get_json()
        status_code = checkpostedData(postdata, "Subtract")
        if(status_code != 200):
            jresp = {
                'Message': "One value not supplied!",
                'Status_code': status_code
            }
            return jsonify(jresp)

        x = postdata["x"]
        y = postdata["y"]

        res = x-y

        jres = {
            'Message': res,
            'Status code': 200
        }

        return jsonify(jres)


class multiply(Resource):
    def post(self):

        posteddata = request.get_json()
        status_code = checkpostedData(posteddata, "multiply")
        if(status_code != 200):
            jress = {
                'message': 'Full value is not supplied!',
                'status code': status_code
            }
            return jsonify(jress)

        x = posteddata["x"]
        y = posteddata["y"]

        result = x*y

        jres = {
            'message': result,
            'status code': 200
        }
        return jsonify(jres)


class Division(Resource):
    def post(self):
        posteddata = request.get_json()
        status_code = checkpostedData(posteddata, 'Division')
        if(status_code != 200):
            jress = {
                'message': 'An error has occured!',
                'status code': status_code
            }
            return jsonify(jress)

        x = posteddata["x"]
        y = posteddata["y"]
        x = int(x)
        y = int(y)

        result = (x*1.0)/y

        jres = {
            'message': result,
            'status code': 200
        }

        return jsonify(jres)


api.add_resource(Add, "/add")
api.add_resource(Subtract, "/subtract")
api.add_resource(multiply, "/multiply")
api.add_resource(Division, "/division")
api.add_resource(visit, "/visit")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    app.run(debug=True)
