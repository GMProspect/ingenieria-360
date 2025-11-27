from rest_framework import viewsets, status
from rest_framework.response import Response
from config.db import db
from bson import ObjectId
import datetime
import pymongo

class HistorialCalculoViewSet(viewsets.ViewSet):
    def list(self, request):
        history = []
        # Sort by created_at descending
        cursor = db.historial_calculo.find().sort('created_at', pymongo.DESCENDING)
        for doc in cursor:
            doc['id'] = str(doc['_id'])
            del doc['_id']
            history.append(doc)
        return Response(history)

    def create(self, request):
        data = request.data
        data['created_at'] = datetime.datetime.utcnow()
        result = db.historial_calculo.insert_one(data)
        data['id'] = str(result.inserted_id)
        del data['_id']
        return Response(data, status=status.HTTP_201_CREATED)
