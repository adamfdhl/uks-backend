from db import db
from utils.constants import map_id_unit_to_skkni


class UnitKompetensiModel(db.Model):
    __tablename__ = 'unit_kompetensi'
    id = db.Column(db.Integer, primary_key=True)
    kode_unit = db.Column(db.String(500))
    judul_unit = db.Column(db.String(500))
    deskripsi_unit = db.Column(db.String(500))

    elemen_kompetensi = db.relationship(
        "ElemenKompetensiModel", lazy=True, backref="unit_kompetensi")

    def __init__(self, kode_unit, judul_unit, deskripsi_unit):
        self.kode_unit = kode_unit
        self.judul_unit = judul_unit
        self.deskripsi_unit = deskripsi_unit

    def __repr__(self):
        return "<UnitKompetensi id: {}, kode_unit: {}, judul_unit: {}, deskripsi_unit: {}>".format(self.id, self.kode_unit, self.judul_unit, self.deskripsi_unit)

    def json(self):
        return {
            "id_unit": self.id,
            "skkni": map_id_unit_to_skkni[self.id],
            "kode_unit": self.kode_unit,
            "judul_unit": self.judul_unit,
            "deskripsi_unit": self.deskripsi_unit
            # "elemen kompetensi": [el.json() for el in self.elemen_kompetensi.all()]
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit(self)

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
    
    @classmethod
    def find_by_id_unit(cls, id_unit):
        return cls.query.get(id_unit)

    @classmethod
    def find_by_kode_unit(cls, kode_unit):
        return cls.query.filter_by(kode_unit=kode_unit).first()

    @classmethod
    def find_by_judul_unit(cls, judul_unit):
        return cls.query.filter_by(judul_unit=judul_unit).first()
