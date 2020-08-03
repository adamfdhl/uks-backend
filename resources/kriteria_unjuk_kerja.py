import sqlite3
import psycopg2
from flask_restful import Resource, reqparse
from models.kriteria_unjuk_kerja import KriteriaUnjukKerjaModel


class KriteriaUnjukKerja(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("elemen_id", type=int, required=True,
                        help="Field elemen_id tidak boleh kosong")
    parser.add_argument("kriteria", type=str, required=True,
                        help="Field kriteria tidak boleh kosong")

    def get(self, elemen_id):
        list_kriteria = KriteriaUnjukKerjaModel.find_by_elemen_id(elemen_id)
        if len(list_kriteria) > 0:
            return {
                "elemen id": elemen_id,
                "kriteria": list_kriteria
            }, 200
        return {"messsage": "Tidak ada kriteria"}, 404

    def post(self, elemen_id, kriteria):
        list_kriteria = KriteriaUnjukKerjaModel.find_by_elemen_id(elemen_id)
        if len(list_kriteria) > 0:
            return {"message": "Kriteria {} pada elemen_id {} sudah ada".format(kriteria, elemen_id)}, 400

        data = KriteriaUnjukKerja.parser.parse_args()
        kriteria_uk = KriteriaUnjukKerjaModel(elemen_id, kriteria)

        try:
            kriteria_uk.save_to_db()
        except:
            return {"message": "An error occurred inserting kriteria"}, 500

        return kriteria_uk.json(), 200

    def delete(self, kriteria):
        kriteria_uk = KriteriaUnjukKerjaModel.find_by_kriteria(kriteria)
        if kriteria_uk:
            kriteria_uk.delete_from_db()
        return {"message": "kriteria deleted"}

    # def put(self, elemen_id, kriteria):
    #     data = KriteriaUnjukKerja.parser.parse_args()
    #     kriteria_uk = KriteriaUnjukKerjaModel.find_by_kriteria(kriteria)

    #     if kriteria_uk is None:
    #         kriteria_uk = KriteriaUnjukKerjaModel(data["elemen_id"], kriteria)
    #     else:


class ListKriteriaUnjukKerja(Resource):
    def get(self):
        return {"kriteria": [kriteria.json() for kriteria in KriteriaUnjukKerjaModel.query.all()]}
