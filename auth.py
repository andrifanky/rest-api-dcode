
from flask import Flask, request, make_response, jsonify
from flask_restful import Resource, Api
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'inirahasianegara'

#decorator untuk kunci endpoint/authenticator
def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        #token akan diparsing meallaui parameter endpoint
        token = request.args.get('token')
        if not token:
            return make_response(jsonify({"msg": "NotFound Token"}), 404)

        #decode token yang diterima
        try:
            output = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except:
            return make_response(jsonify({"msg": "Token not true"}))
        return f(*args, **kwargs)
    return decorator


#1 membuat endpoint untuk login
class LoginUser(Resource):
    def post(self):
        username = request.form.get('username')
        password = request.form.get('password')

        if username and password == 'superadmin':
            #hasilkan nomor token
            token = jwt.encode({"username":username, "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=10)}, app.config['SECRET_KEY'], algorithm="HS256")
            return jsonify({"token":token, "msg":"Succesfull Login!"})
        return jsonify({"msg": "Please Login!"})



#2 Halaman yang di protec 
class Dashboard(Resource):
    @token_required
    def get(self):
        return jsonify({"msg": "Succesfull Login"})


#3 Halaman non protec
class HomePage(Resource):
    def get(self):
        return jsonify({"msg": "Ini adalah halaman public"})

api.add_resource(LoginUser, "/api/login", methods=["POST"])
api.add_resource(Dashboard, "/api/dashboard", methods=["GET"])
api.add_resource(HomePage, "/api", methods=["GET"])

if __name__ == '__main__':
    app.run(debug=True)
