from rest_framework import serializers
from freight_app.models import Contact, ContactForm

class ContactSerializer(serializers.ModelSerializer):
    _id = serializers.IntegerField(source='id', read_only=True)
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    
    fullName = serializers.CharField(required=True, error_messages={'required': 'Full name is required'})
    phoneNumber = serializers.CharField(required=True, error_messages={'required': 'Phone number is required'})
    email = serializers.EmailField(required=True, error_messages={'required': 'Email is required'})
    
    class Meta:
        model = Contact
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class ContactFormSerializer(serializers.ModelSerializer):
    _id = serializers.IntegerField(source='id', read_only=True)
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    
    fullName = serializers.CharField(required=True)
    phoneNumber = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    register = serializers.ChoiceField(choices=ContactForm.REGISTER_CHOICES, required=True)
    
    class Meta:
        model = ContactForm
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
