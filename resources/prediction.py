from flask_restful import Resource
from flask import request

from models.unit_kompetensi import UnitKompetensiModel
from models.elemen_kompetensi import ElemenKompetensiModel

from utils.helpers import integration_module
from utils.constants import map_id_unit_to_skkni

import json


class Prediction(Resource):

    def __init__(self):
        self.query = None
        self.filter = None
        self.result = []

    def post(self):
        # query = request.form['query']
        data = request.get_json()
        query = data["query"]
        selected_filter = data["filter"]

        if query:
            self.query = query
        if selected_filter:
            self.filter = selected_filter
        
        if self.filter == "unit_kompetensi":
            print("enter unit_kompetensi")
            uk = self.get_all_uk()

            for unit in uk["unit"]:
                score_judul = self.get_similarity_score(query, unit["judul_unit"])
                score_deskripsi = self.get_similarity_score(query, unit["deskripsi_unit"])

                score = max(score_judul, score_deskripsi)

                self.result.append({
                    "id_unit": unit["id_unit"],
                    "skkni" : map_id_unit_to_skkni[unit["id_unit"]],
                    "kode_unit": unit["kode_unit"],
                    "judul_unit": unit["judul_unit"],
                    "deskripsi_unit": unit["deskripsi_unit"],
                    "similarity_score": float(score)
                })
        elif self.filter == "elemen_kompetensi":
            print("enter elemen_kompetensi")
            ek = self.get_all_ek()    
            for elemen in ek["elemen"]:
                score_elemen = self.get_similarity_score(query, elemen["elemen_kompetensi"])

                self.result.append({
                    "id_unit": elemen["id_unit"],
                    "skkni": map_id_unit_to_skkni[elemen["id_unit"]],
                    "elemen_kompetensi": elemen["elemen_kompetensi"],
                    "similarity_score": float(score_elemen)
                })
        elif self.filter == None:
            # no filter
            print("enter no filter")
            uk = self.get_all_uk()
            ek = self.get_all_ek()
            for unit in uk["unit"]:
                score_judul = self.get_similarity_score(query, unit["judul_unit"])
                score_deskripsi = self.get_similarity_score(query, unit["deskripsi_unit"])

                score = max(score_judul, score_deskripsi)

                self.result.append({
                    "id_unit": unit["id_unit"],
                    "skkni": map_id_unit_to_skkni[unit["id_unit"]],
                    "kode_unit": unit["kode_unit"],
                    "judul_unit": unit["judul_unit"],
                    "deskripsi_unit": unit["deskripsi_unit"],
                    "similarity_score": float(score)
                })

            for elemen in ek["elemen"]:
                score_elemen = self.get_similarity_score(query, elemen["elemen_kompetensi"])

                self.result.append({
                    "id_unit": elemen["id_unit"],
                    "skkni": map_id_unit_to_skkni[elemen["id_unit"]],
                    "elemen_kompetensi": elemen["elemen_kompetensi"],
                    "similarity_score": float(score_elemen)
                })

        top_result = sorted(self.result, key=lambda x: x["similarity_score"], reverse=True)[:5]
        return {
            "query": self.query,
            "filter": self.filter,
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