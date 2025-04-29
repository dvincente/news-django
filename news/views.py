from django.shortcuts import render

import os
import requests
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return render(request, "index.html")

@require_GET
@csrf_exempt  # Optional, depending on how you use the endpoint
def coindesk_news(request):
    try:
        api_key = os.getenv('COINDESK_API_KEY')  # Or settings.COINDESK_API_KEY
        params = {
            'lang': 'EN',
            'limit': 100,
            'api_key': api_key,
        }
        response = requests.get("https://data-api.coindesk.com/news/v1/article/list", params=params)
        response.raise_for_status()
        return JsonResponse(response.json(), safe=False)
    except requests.exceptions.RequestException as e:
        print("Error fetching data from Coindesk:", e)
        return JsonResponse({"error": "Failed to fetch data from Coindesk"}, status=500)