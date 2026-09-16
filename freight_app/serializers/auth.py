from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from freight_app.models import User

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['message'] = "SignIn Successful"
        data['id'] = str(self.user.id)
        data['role'] = self.user.role
        data['token'] = data.pop('access')
        return data

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, min_length=4)
    email = serializers.EmailField(required=True)
    address = serializers.CharField(required=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'address', 'avatar', 'role']
        read_only_fields = ['id', 'role', 'avatar']

