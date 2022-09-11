# from sqlite3 import DatabaseError
# from urllib import response 
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

# create database
db.create_all()

# inisiasi variabel kosong bertipe dictionary
# identitas = {} # variable global, dictionary = json

# membuat class Resource
class ContohResource(Resource):
    # metode get dan post
    def get(self):
        # menampilkan database
        query = DatabaseModel.query.all()

        # melakukan iterasi pada DatabaseModel
        output = [{"id": data.id,"nama" : data.nama, "umur" : data.umur, "alamat" : data.alamat}for data in query]
        response = {"code" : 200, "Query" : "Query Sukses", "data" : output}
        return output, 200
    
    def post(self):
        dataNama = request.form["nama"]
        dataUmur = request.form["umur"]
        dataAlamat = request.form["alamat"]
        
        model = DatabaseModel(nama = dataNama, umur = dataUmur, alamat = dataAlamat)
        model.save()
        response = {"msg": "Succesful create data", "code" : 200}
        return response, 200

    def delete(self):
        query = DatabaseModel.query.all()
        for data in query:
            db.session.delete(data)
            db.session.commit()

        response = {"msg" : "Succesful delete all data", "code" : 200}
        return response

# membuat class update
class UpdateResource(Resource):


    def put(self, id):
        query = DatabaseModel.query.get(id)

        # form edit data
        editNama = request.form["nama"]
        editUmur = request.form["umur"]
        editAlamat = request.form["alamat"]

        # replace data
        query.nama = editNama
        query.umur = editUmur
        query.alamat = editAlamat

        db.session.commit()

        response = {"msg" : "Succesful update data", "code" : 200}

        return response, 200

    #delete by id
    def delete(self, id):
        queryData = DatabaseModel.query.get(id)


        # call method delete
        db.session.delete(queryData)
        db.session.commit()

        response = { "msg" : "Succesful delete data", "code" : 200}
        return response


# setup resourcenya
api.add_resource(ContohResource, "/api", methods=["GET","POST", "DELETE"])
api.add_resource(UpdateResource, "/api/<id>", methods=["PUT", "DELETE"])


if __name__ == '__main__':
    app.run(debug=True, port=5005)