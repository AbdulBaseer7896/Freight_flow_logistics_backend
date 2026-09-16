from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from freight_app.serializers import ContactSerializer, ContactFormSerializer
from freight_app.models import Contact, ContactForm

class GeneralContactUsView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = ContactFormSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Form submitted successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class JustContactUsView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'message': 'Contact form submitted successfully'}, status=status.HTTP_201_CREATED)
        return Response({'success': False, 'message': 'Error', 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        contacts = Contact.objects.all().order_by('-id')
        serializer = ContactSerializer(contacts, many=True)
        return Response(serializer.data)

class ContactDataListView(APIView):
    def get(self, request):
        forms = ContactForm.objects.all().order_by('-id')
        serializer = ContactFormSerializer(forms, many=True)
        return Response(serializer.data)

class DeleteContactFormView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, pk):
        form = get_object_or_404(ContactForm, pk=pk)
        form.delete()
        return Response({'message': 'Contact form deleted successfully'})

class DeleteContactView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, pk):
        contact = get_object_or_404(Contact, pk=pk)
        contact.delete()
        return Response({'message': 'Carrier deleted successfully'})
