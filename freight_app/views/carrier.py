import json
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from freight_app.serializers import CarrierDataSerializer
from freight_app.models import CarrierData

class CarrierDataView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        try:
            carrier_data_str = request.data.get('carrierData')
            if carrier_data_str:
                data = json.loads(carrier_data_str)
            else:
                data = request.data.copy()
            
            serializer = CarrierDataSerializer(data=data)
            if serializer.is_valid():
                carrier = serializer.save()
                if 'MCAuthFile' in request.FILES:
                    carrier.MCAuthFile = request.FILES['MCAuthFile']
                if 'COLFile' in request.FILES:
                    carrier.COLFile = request.FILES['COLFile']
                if 'W9File' in request.FILES:
                    carrier.W9File = request.FILES['W9File']
                if 'NOVFile' in request.FILES:
                    carrier.NOVFile = request.FILES['NOVFile']
                carrier.save()
                return Response({'message': 'Carrier data saved successfully!'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': 'Error saving carrier data', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CarriersDataListView(APIView):
    def get(self, request):
        carriers = CarrierData.objects.all().order_by('-id')
        serializer = CarrierDataSerializer(carriers, many=True)
        return Response(serializer.data)

class ToggleStatusView(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, pk):
        carrier = get_object_or_404(CarrierData, pk=pk)
        carrier.isActive = 'inActive' if carrier.isActive == 'active' else 'active'
        carrier.save()
        return Response({'message': 'Status updated successfully', 'carrier': CarrierDataSerializer(carrier).data})

class DeleteCarrierView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, pk):
        carrier = get_object_or_404(CarrierData, pk=pk)
        carrier.delete()
        return Response({'message': 'Carrier deleted successfully'})
