import sqlite3
import psycopg2
from flask_restful import Resource
from models.elemen_kompetensi import ElemenKompetensiModel


class ElemenKompetensi(Resource):
    def get(self, id_unit):
        el_kompetensi = ElemenKompetensiModel.find_by_id_unit(id_unit)
        if len(el_kompetensi) > 0:
            return el_kompetensi.json(), 200
        return {"message": "Elemen kompetensi for {} not found".format(id_unit)}, 404

    def post(self, id_unit, elemen_kompetensi):
        if ElemenKompetensiModel.find_by_elemen(elemen_kompetensi):
            return {"message": "Elemen kompetensi {} already exists".format(elemen_kompetensi)}, 400

        el_kompetensi = ElemenKompetensiModel(id_unit, elemen_kompetensi)
        try:
            el_kompetensi.save_to_db()
        except:
            return {"message": "An error occurred while creating elemen kompetensi"}, 500

        return el_kompetensi.json()

    def delete(self, elemen_kompetensi):
        el_kompetensi = ElemenKompetensiModel.find_by_elemen(elemen_kompetensi)
        if el_kompetensi:
            el_kompetensi.delete_from_db()
        return {"message": "Elemen kompetensi deleted"}


class ListElemenKompetensi(Resource):
    def get(self):
        return {"elemen": [elemen.json() for elemen in ElemenKompetensiModel.query.all()]}
