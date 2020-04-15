import sqlite3
from flask_restful import Resource
from models.unit_kompetensi import UnitKompetensiModel


class UnitKompetensi(Resource):
    def get(self, kode_unit):
        uk = UnitKompetensiModel.find_by_kode_unit(kode_unit)
        if uk:
            return uk.json(), 200
        return {"message": "Unit Kompetensi not found"}

    def post(self, kode_unit, judul_unit):
        if UnitKompetensiModel.find_by_kode_unit(kode_unit):
            return {"message": "Unit Kompetensi {} already exists".format(kode_unit)}, 400

        uk = UnitKompetensiModel(kode_unit, judul_unit)
        try:
            uk.save_to_db()
        except:
            return {"message": "An error occurred"}, 500

    def delete(self, kode_unit):
        uk = UnitKompetensiModel.find_by_kode_unit(kode_unit)
        if uk:
            uk.delete_from_db()
        return {"message": "Unit Kompetensi Deleted"}


class ListUnitKompetensi(Resource):
    def get(self):
        return {"unit": [unit.json() for unit in UnitKompetensiModel.query.all()]}
