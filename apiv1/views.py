from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.parsers import JSONParser
from mbti.models import Mbti
from . serializers import MbtiSerializer
import pickle
import json
import numpy as np
from sklearn import preprocessing
import pandas as pd
import gensim

class MbtiAPIView(generics.GenericAPIView):

    queryset = Mbti.objects.all()
    serializer_class = MbtiSerializer

    def post(self, request):

        data = request.data.copy()
        content = data["content"]
        clfnames = ['logreg_ie', 'logreg_sn', 'logreg_tf', 'logreg_pj']
        preds = []
        probas = []
        types = {
            "INTJ": "The Architect",
            "INTP": "The Logician",
            "ENTJ": "The Commander",
            "ENTP": "The Debater",
            "INFJ": "The Advocate",
            "INFP": "The Mediator",
            "ENFJ": "The Protagonist",
            "ENFP": "The Campaigner",
            "ISTJ": "The Logistician",
            "ISFJ": "The Defender",
            "ESTJ": "The Executive",
            "ESFJ": "The Consul",
            "ISTP": "The Virtuoso",
            "ISFP": "The Adventurer",
            "ESTP": "The Entrepreneur",
            "ESFP": "The Entertainer"
        }

        # word2vec 
        mdl = pickle.load(open('apiv1/clfs/model.pickle', 'rb'))
        content = gensim.utils.simple_preprocess(content)
        vec = np.array(mdl.infer_vector(content)).reshape(1, 100).tolist()

        for name in clfnames:
            clf = pickle.load(open('apiv1/clfs/{}.pickle'.format(name), 'rb'))
            pred = clf.predict(vec)
            proba = clf.predict_proba(vec)
            preds.append(pred)
            probas.append(proba)
        
        ie = "I" if preds[0] == 0 else "E"
        sn = "S" if preds[1] == 0 else "N"
        tf = "T" if preds[2] == 0 else "F"
        pj = "P" if preds[3] == 0 else "J"
        label = ie + sn + tf + pj
        
        data["label"] = label
        data["type"] = types.get(label,"None")
        data["score_ie"] = [round(i, 3) for i in probas[0][0]]
        data["score_sn"] = [round(i, 3) for i in probas[1][0]]
        data["score_tf"] = [round(i, 3) for i in probas[2][0]]
        data["score_pj"] = [round(i, 3) for i in probas[3][0]]

        serializer = MbtiSerializer(data=data)
        if serializer.is_valid():
            pass
        
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        return Response(data, status=status.HTTP_200_OK)