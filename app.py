import os
import psycopg2
from flask import Flask
from flask_restful import Api

from resources.kriteria_unjuk_kerja import KriteriaUnjukKerja, ListKriteriaUnjukKerja
from resources.elemen_kompetensi import ElemenKompetensi, ListElemenKompetensi
from resources.unit_kompetensi import UnitKompetensi, ListUnitKompetensi

from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://postgres:adamfdhl@localhost/tugasakhir')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'ganteng'
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


# Unit API
api.add_resource(UnitKompetensi, '/unit/<string:kode_unit>', endpoint="uk_get")
api.add_resource(
    UnitKompetensi, '/unit/<string:kode_unit>/<string:judul_unit>', endpoint="uk_post")
api.add_resource(ListUnitKompetensi, '/units')

# Elemen API
api.add_resource(ElemenKompetensi, '/elemen/<int:id_unit>')
api.add_resource(ListElemenKompetensi, '/elemens')

# Kriteria API
api.add_resource(KriteriaUnjukKerja, '/kriteria/<int:elemen_id>')
api.add_resource(ListKriteriaUnjukKerja, '/kriterias')

if __name__ == "__main__":
    db.init_app(app)
    app.run(port=5000, debug=True)
