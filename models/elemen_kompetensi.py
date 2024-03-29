from db import db
from utils.constants import map_id_unit_to_skkni


class ElemenKompetensiModel(db.Model):
    __tablename__ = 'elemen_kompetensi'
    id = db.Column(db.Integer, primary_key=True)
    elemen_kompetensi = db.Column(db.String(500))

    id_unit = db.Column(db.Integer, db.ForeignKey(
        'unit_kompetensi.id'))
    # unit_kompetensi = db.relationship("UnitKompetensiModel", lazy=True)

    kriteria_unjuk_kerja = db.relationship(
        "KriteriaUnjukKerjaModel", lazy=True, backref="elemen_kompetensi")

    def __init__(self, id_unit, elemen_kompetensi):
        self.id_unit = id_unit
        self.elemen_kompetensi = elemen_kompetensi

    def __repr__(self):
        return "<ElemenKompetensi id_unit {}: {}>".format(self.id_unit, self.elemen_kompetensi)

    def json(self):
        return {
            "id_unit": self.id_unit,
            "skkni": map_id_unit_to_skkni[self.id_unit],
            "elemen_kompetensi": self.elemen_kompetensi,
            # "kriteria": [kriteria.json() for kriteria in self.kriteria_unjuk_kerja.all()]
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id_unit(cls, id_unit):
        return cls.query.filter_by(id_unit=id_unit).all()

    @classmethod
    def find_by_elemen(cls, elemen):
        return cls.query.filter_by(elemen_kompetensi=elemen).first()
