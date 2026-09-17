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

try:
    from curl_cffi import requests as cffi_requests
    HAS_CURL_CFFI = True
except ImportError:
    import requests as cffi_requests
    HAS_CURL_CFFI = False

class MCLookupView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, mcNumber):
        if not mcNumber.isdigit():
            return Response({'error': 'Invalid MC number format'}, status=status.HTTP_400_BAD_REQUEST)
        
        api_url = f"https://highway.com/monitor/api/v1/carriers/by_identifier?is_type=MC&value={mcNumber}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://highway.com/',
        }

        try:
            req_kwargs = {'headers': headers, 'timeout': 15}
            if HAS_CURL_CFFI:
                req_kwargs['impersonate'] = 'chrome124'
            
            response = cffi_requests.get(api_url, **req_kwargs)
            response.raise_for_status()
            carrier_data = response.json()
            
            physical = carrier_data.get('physical_address', {})
            address_parts = [physical.get('street1'), physical.get('city'), physical.get('state'), physical.get('postal_code')]
            address = ", ".join(filter(bool, address_parts))
            
            mc_val = next((id.get('value') for id in carrier_data.get('identifiers', []) if id.get('is_type') == 'MC'), mcNumber)
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
        except Exception as e:
            error_details = str(e)
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            if hasattr(e, 'response') and e.response is not None:
                status_code = e.response.status_code
                try:
                    error_details = e.response.json().get('error', str(e))
                except Exception:
                    error_details = e.response.text or str(e)
            
            return Response({
                'error': 'Failed to fetch carrier data',
                'details': error_details
            }, status=status_code)
