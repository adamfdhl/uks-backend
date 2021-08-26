from flask_restful import Resource
from flask import request

from models.unit_kompetensi import UnitKompetensiModel
from models.elemen_kompetensi import ElemenKompetensiModel


class Prediction(Resource):

    def __init__(self):
        self.sentence_1 = None
        self.sentence_2 = None
        self.score = 0

    def post(self):
        sentence_1 = request.form['sentence_1']
        sentence_2 = request.form['sentence_2']
        if sentence_1:
            self.sentence_1 = sentence_1
        if sentence_2:
            self.sentence_2 = sentence_2
        self.validate()
        uk = self.get_all_uk()
        ek = self.get_all_ek()
        return {
            "sentence_1": self.sentence_1,
            "sentence_2": self.sentence_2,
            "score": self.score,
        }, 200

    def validate(self):
        self.score = 0.5
    
    def get_all_uk(self):
        return {"unit": [unit.json() for unit in UnitKompetensiModel.query.all()]}
    
    def get_all_ek(self):
        return {"elemen": [elemen.json() for elemen in ElemenKompetensiModel.query.all()]}