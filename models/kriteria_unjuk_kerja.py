from db import db


class KriteriaUnjukKerjaModel(db.Model):
    __tablename__ = 'kriteria_unjuk_kerja'
    id = db.Column(db.Integer, primary_key=True)
    kriteria = db.Column(db.String(500))

    elemen_id = db.Column(db.Integer, db.ForeignKey('elemen_kompetensi.id'))
    elemen_kompetensi = db.relationship(
        'ElemenKompetensiModel', lazy=True)

    def __init__(self, elemen_id, kriteria):
        self.elemen_id = elemen_id
        self.kriteria = kriteria

    def __repr__(self):
        return "<KriteriaUnjukKerja elemen_id {}: {}>".format(self.elemen_id, self.kriteria)

    def json(self):
        return {
            "elemen_id": self.elemen_id,
            "kriteria": self.kriteria
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_elemen_id(cls, elemen_id):
        return cls.query.filter_by(elemen_id=elemen_id).all()

    @classmethod
    def find_by_kriteria(cls, kriteria):
        return cls.query.filter_by(kriteria=kriteria.lower()).first()
