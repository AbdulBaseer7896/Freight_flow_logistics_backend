from rest_framework import serializers
from freight_app.models import CarrierData

class CarrierDataSerializer(serializers.ModelSerializer):
    _id = serializers.IntegerField(source='id', read_only=True)
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    
    # Explicitly enforce required fields
    MC = serializers.CharField(required=True, error_messages={'required': 'MC number is required.'})
    Legal_Name = serializers.CharField(required=True, error_messages={'required': 'Legal Name is required.'})
    Email = serializers.EmailField(required=True, error_messages={'required': 'Email is required.'})
    Phone = serializers.CharField(required=True, error_messages={'required': 'Phone number is required.'})
    USDOT_Number = serializers.CharField(required=True)
    Physical_Address = serializers.CharField(required=True)
    
    # Optional files and fields
    MCAuthFile = serializers.FileField(required=False, allow_null=True)
    COLFile = serializers.FileField(required=False, allow_null=True)
    W9File = serializers.FileField(required=False, allow_null=True)
    NOVFile = serializers.FileField(required=False, allow_null=True)
    
    class Meta:
        model = CarrierData
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'isActive']

