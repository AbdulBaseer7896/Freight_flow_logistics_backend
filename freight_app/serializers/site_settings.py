from rest_framework import serializers
from freight_app.models import SiteSettings

class SiteSettingsSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    address = serializers.CharField(required=True)
    
    class Meta:
        model = SiteSettings
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

