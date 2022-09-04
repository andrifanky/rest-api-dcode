# import library

from sqlite3 import DatabaseError
from urllib import response
from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os

# inisiasi object flask
app = Flask(__name__)

# inisiasi object flask_resful
api = Api(app)

# inisiasi object flask_cors
CORS(app)

# inisialisasi flask sqlalchemy
db = SQLAlchemy(app)

# mengkonfigurasi database sqlite
basedir = os.path.dirname(os.path.abspath(__file__))
database = "sqlite:///" + os.path.join(basedir, "db.sqlite")
app.config["SQLALCHEMY_DATABASE_URI"] = database

# membuat database model
class DatabaseModel(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nama = db.Column(db.String(100))
    umur = db.Column(db.Integer)
    alamat = db.Column(db.TEXT) # db Tambahan

    # membuat method save db
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False

# mencreate database
db.create_all()

# inisiasi variabel kosong bertipe dictionary
identitas = {} # variable global, dictionary = json

# membuat class Resource
class ContohResource(Resource):
    # metode get dan post
    def get(self):
        # menampilkan database
        query = DatabaseModel.query.all()

        # melakukan iterasi pada DAtabaseModel
        output = [{"nama" : data.nama, "umur" : data.umur, "alamat" : data.alamat}for data in query]
        response = {"code" : 200, "Query" : "Query Sukses", "data" : output}
        return output, 200
    
    def post(self):
        dataNama = request.form["nama"]
        dataUmur = request.form["umur"]
        dataAlamat = request.form["alamat"]
        
        model = DatabaseModel(nama = dataNama, umur = dataUmur, alamat = dataAlamat)
        model.save()
        response = {"msg": "Data berhasil dimasukkan", "code" : 200}
        return response, 200

# setup resourcenya
api.add_resource(ContohResource, "/api", methods=["GET","POST"])

if __name__ == '__main__':
    app.run(debug=True, port=5005)

    #coba push 2