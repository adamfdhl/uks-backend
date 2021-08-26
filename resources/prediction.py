from flask_restful import Resource
from flask import request

from models.unit_kompetensi import UnitKompetensiModel
from models.elemen_kompetensi import ElemenKompetensiModel

from utils.helpers import integration_module

import json


class Prediction(Resource):

    def __init__(self):
        self.query = None
        self.result = []

    def post(self):
        query = request.form['query']
        if query:
            self.query = query
        uk = self.get_all_uk()
        ek = self.get_all_ek()
        for unit in uk["unit"]:
            score_judul = self.get_similarity_score(query, unit["judul unit"])
            score_deskripsi = self.get_similarity_score(query, unit["deskripsi unit"])

            score = max(score_judul, score_deskripsi)

            self.result.append({
                "kode_unit": unit["kode unit"],
                "judul_unit": unit["judul unit"],
                "deskripsi_unit": unit["deskripsi unit"],
                "score": float(score)
            })
        top_result = sorted(self.result, key=lambda x: x["score"], reverse=True)[:5]
        return {
            "query": self.query,
            "result": top_result,
        }, 200

    def get_similarity_score(self, sentence_1, sentence_2):
        proportion_semantic = 0.5
        shared_parameter = 1 - proportion_semantic
        score = integration_module(sentence_1, sentence_2, proportion_semantic, shared_parameter)
        return score
    
    def get_all_uk(self):
        return {"unit": [unit.json() for unit in UnitKompetensiModel.query.all()]}
    
    def get_all_ek(self):
        return {"elemen": [elemen.json() for elemen in ElemenKompetensiModel.query.all()]}