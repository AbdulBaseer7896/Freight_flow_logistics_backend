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

import os

def _format_proxy_url(proxy_str):
    """Converts various proxy formats (host:port:user:pass, user:pass@host:port, etc.) to a standard URL."""
    if not proxy_str or not str(proxy_str).strip():
        return None
    raw = str(proxy_str).strip()
    if '://' in raw:
        return raw
    if '@' in raw:
        return f'http://{raw}'
    parts = raw.split(':')
    if len(parts) == 4:
        host, port, user, pwd = parts
        return f'http://{user}:{pwd}@{host}:{port}'
    elif len(parts) == 2:
        host, port = parts
        return f'http://{host}:{port}'
    return f'http://{raw}'

def _fetch_carrier_from_highway(mc_number):
    """Fetches carrier data from Highway using a warm browser session to pass CloudFront WAF."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    raw_proxy = os.getenv('SCRAPER_PROXY') or os.getenv('HTTPS_PROXY') or os.getenv('HTTP_PROXY')
    proxy_url = _format_proxy_url(raw_proxy)
    proxies = {'http': proxy_url, 'https': proxy_url} if proxy_url else None

    if HAS_CURL_CFFI:
        session = cffi_requests.Session(impersonate='chrome124')
    else:
        session = requests.Session()

    session.headers.update(headers)
    if proxies:
        session.proxies = proxies
    
    # 1. Warm up session by visiting the home page (establishes CloudFront cookies)
    try:
        session.get('https://highway.com', timeout=15)
    except Exception:
        pass

    # 2. Query the carrier endpoint with appropriate referer and headers
    api_url = f"https://highway.com/monitor/api/v1/carriers/by_identifier?is_type=MC&value={mc_number}"
    api_headers = {
        'Referer': 'https://highway.com/',
        'Accept': 'application/json, text/plain, */*',
    }
    
    response = session.get(api_url, headers=api_headers, timeout=20)
    response.raise_for_status()
    return response.json()

class MCLookupView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, mcNumber):
        if not mcNumber.isdigit():
            return Response({'error': 'Invalid MC number format'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            carrier_data = _fetch_carrier_from_highway(mcNumber)
            
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
            error_details = "Carrier lookup service is temporarily blocked or unavailable for this IP. Please enter details manually."
            status_code = status.HTTP_404_NOT_FOUND
            return Response({
                'error': 'Failed to fetch carrier data',
                'details': error_details
            }, status=status_code)
