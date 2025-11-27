from rest_framework import viewsets, status
from rest_framework.response import Response
from config.db import db
from bson import ObjectId
import datetime

class EquipoViewSet(viewsets.ViewSet):
    def list(self, request):
        try:
            equipos = []
            for doc in db.equipos.find():
                doc['id'] = str(doc['_id'])
                del doc['_id']
                equipos.append(doc)
            return Response(equipos)
        except Exception as e:
            print(f"Error connecting to DB: {e}")
            return Response({'error': 'Database Connection Error', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request):
        data = request.data
        data['created_at'] = datetime.datetime.utcnow()
        result = db.equipos.insert_one(data)
        data['id'] = str(result.inserted_id)
        del data['_id']
        return Response(data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        try:
            doc = db.equipos.find_one({'_id': ObjectId(pk)})
            if doc:
                doc['id'] = str(doc['_id'])
                del doc['_id']
                return Response(doc)
            return Response(status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        try:
            db.equipos.update_one({'_id': ObjectId(pk)}, {'$set': request.data})
            return Response(request.data)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            db.equipos.delete_one({'_id': ObjectId(pk)})
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
