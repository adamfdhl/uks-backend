from flask import Flask
from flask_restful import Api

from resources.kriteria_unjuk_kerja import KriteriaUnjukKerja, ListKriteriaUnjukKerja
from resources.elemen_kompetensi import ElemenKompetensi, ListElemenKompetensi
from resources.unit_kompetensi import UnitKompetensi, ListUnitKompetensi

from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'ganteng'
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(KriteriaUnjukKerja, '/kriteria/:elemen_id')
api.add_resource(ListKriteriaUnjukKerja, '/kriterias')
api.add_resource(ElemenKompetensi, '/elemen/:id_unit')
api.add_resource(ListElemenKompetensi, '/elemens')
api.add_resource(UnitKompetensi, '/unit/:kode_unit')
api.add_resource(ListUnitKompetensi, '/units')


if __name__ == "__main__":
    db.init_app(app)
    app.run(port=5000, debug=True)
