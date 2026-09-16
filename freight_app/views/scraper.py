import json
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from freight_app.pythonCode import get_data_as_json

class MCNumberView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, mc):
        if not mc.isdigit():
            return Response({'error': 'Invalid input. Please enter a valid number.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            result_json = get_data_as_json(mc)
            return Response(json.loads(result_json))
        except Exception as e:
            return Response({'error': 'Server Error', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MCLookupView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, mcNumber):
        if not mcNumber.isdigit():
            return Response({'error': 'Invalid MC number format'}, status=status.HTTP_400_BAD_REQUEST)
        
        api_url = f"https://highway.com/monitor/api/v1/carriers/by_identifier?is_type=MC&value={mcNumber}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/html, application/xhtml+xml, application/xml',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'no-cache',
            'Referer': 'https://highway.com/',
            'Priority': 'u=0, i',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Upgrade-Insecure-Requests': '1'
        }
        
        # Forward cookies if the frontend provided any
        client_cookie = request.headers.get('Cookie')
        if client_cookie:
            headers['Cookie'] = client_cookie
        
        try:
            response = requests.get(api_url, headers=headers)
            response.raise_for_status()
            carrier_data = response.json()
            
            physical = carrier_data.get('physical_address', {})
            address_parts = [physical.get('street1'), physical.get('city'), physical.get('state'), physical.get('postal_code')]
            address = ", ".join(filter(bool, address_parts))
            
            mc_val = next((id.get('value') for id in carrier_data.get('identifiers', []) if id.get('is_type') == 'MC'), 'N/A')
            dot_val = next((id.get('value') for id in carrier_data.get('identifiers', []) if id.get('is_type') == 'DOT'), 'N/A')
            
            phones = carrier_data.get('phones') or []
            phone = phones[0].get('value', 'N/A') if len(phones) > 0 else 'N/A'
            
            emails = carrier_data.get('email_addresses') or []
            email = emails[0].get('value', 'N/A') if len(emails) > 0 else 'N/A'

            formatted_data = {
                'Legal_Name': carrier_data.get('legal_name', 'N/A'),
                'Physical_Address': address,
                'MC': mc_val,
                'Phone': phone,
                'USDOT_Number': dot_val,
                'Email': email
            }
            return Response(formatted_data)
        except requests.exceptions.RequestException as e:
            status_code = e.response.status_code if e.response is not None else status.HTTP_500_INTERNAL_SERVER_ERROR
            error_details = str(e)
            if e.response is not None:
                try:
                    error_details = e.response.json().get('error', str(e))
                except ValueError:
                    error_details = e.response.text or str(e)
            
            return Response({
                'error': 'Failed to fetch carrier data',
                'details': error_details
            }, status=status_code)
        except Exception as e:
            return Response({'error': 'Failed to fetch carrier data', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
