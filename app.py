# import library
from crypt import methods
from urllib import response
from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS

# inisiasi object flask
app = Flask(__name__)

# inisiasi object flask_resful
api = Api(app)

# inisiasi object flask_cors
CORS(app)

# inisiasi variabel kosong bertipe dictionary
identitas = {} # variable global, dictionary = json

# membuat class Resource
class ContohResource(Resource):
    # metode get dan post
    def get(self):
        # response = {"msg": "Hallo dunia, ini app restful pertama kami"}
        return identitas
    
    def post(self):
        nama = request.form["nama"]
        umur = request.form["umur"]
        identitas["nama"] = nama
        identitas["umur"] = umur
        response = {"msg": "Data berhasil dimasukkan"}
        return response

# setup resourcenya
api.add_resource(ContohResource, "/api", methods=["GET","POST"])

if __name__ == '__main__':
    app.run(debug=True, port=5005)