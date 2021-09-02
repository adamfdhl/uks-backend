import os
import psycopg2
from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from resources.kriteria_unjuk_kerja import KriteriaUnjukKerja, ListKriteriaUnjukKerja
from resources.elemen_kompetensi import ElemenKompetensi, ListElemenKompetensi
from resources.unit_kompetensi import UnitKompetensi, ListUnitKompetensi
from resources.prediction import Prediction

from db import db

app = Flask(__name__)
CORS(app)
ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://postgres:adam16@localhost/tugasakhir')
    app.secret_key = 'ganteng'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)


# Unit API
api.add_resource(UnitKompetensi, '/unit/<int:id_unit>', endpoint="uk_get")
api.add_resource(
    UnitKompetensi, '/unit/<string:kode_unit>/<string:judul_unit>', endpoint="uk_post")
api.add_resource(ListUnitKompetensi, '/units')

# Elemen API
api.add_resource(ElemenKompetensi, '/elemen/<int:id_unit>')
api.add_resource(ListElemenKompetensi, '/elemens')

# Kriteria API
api.add_resource(KriteriaUnjukKerja, '/kriteria/<int:elemen_id>')
api.add_resource(ListKriteriaUnjukKerja, '/kriterias')

# Prediction API
api.add_resource(Prediction, '/validate')


if __name__ == "__main__":
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(port=5000)
