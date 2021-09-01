from flask_restful import Resource, reqparse
from models.unit_kompetensi import UnitKompetensiModel


class UnitKompetensi(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("kode_unit", type=str, required=True,
                        help="This field can't be blank.")
    parser.add_argument("judul_unit", type=str, required=True,
                        help="This field can't be blank.")

    def get(self, id_unit):
        uk = UnitKompetensiModel.find_by_id_unit(id_unit)
        if uk:
            return uk.json(), 200
        return {"message": "Unit Kompetensi not found"}

    def post(self, kode_unit, judul_unit):
        if UnitKompetensiModel.find_by_kode_unit(kode_unit):
            return {"message": "Unit Kompetensi {} already exists".format(kode_unit)}, 400

        data = UnitKompetensi.parser.parse_args()
        uk = UnitKompetensiModel(**data)
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
