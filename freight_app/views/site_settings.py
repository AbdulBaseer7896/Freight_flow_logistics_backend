from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from freight_app.serializers import SiteSettingsSerializer
from freight_app.models import SiteSettings

class SiteSettingsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        settings = SiteSettings.objects.first()
        if not settings:
            settings = SiteSettings.objects.create()
        return Response(SiteSettingsSerializer(settings).data)

    def _save(self, request):
        settings = SiteSettings.objects.first()
        if not settings:
            settings = SiteSettings.objects.create()
        serializer = SiteSettingsSerializer(settings, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Site settings updated successfully', 'settings': serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        return self._save(request)

    def put(self, request):
        return self._save(request)

    def patch(self, request):
        return self._save(request)
