import requests
import json
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
# import related models here
from .models import CarDealer
from requests.auth import HTTPBasicAuth
from ibmcloudant.cloudant_v1 import AllDocsQuery, CloudantV1
from ibm_cloud_sdk_core import ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from dotenv import dotenv_values
from django.conf import settings
from urllib.parse import urlparse, parse_qs

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
import requests
import json
from .models import CarDealer
from requests.auth import HTTPBasicAuth

def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["dealerships"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                   id=dealer["id"], lat=dealer["lat"], long=dealer["long"], short_name=dealer["short_name"],                          
                                   st=dealer["st"], zip=dealer["zip"])
            results.append(dealer_obj)

    return results

def get_reviews_from_cf(request):
    incoming_query = urlparse(request.build_absolute_uri()).query
    query_string = parse_qs(incoming_query)
    
    db_name = "reviews"

    selector = {}

    if 'dealerId' in query_string.keys():
        selector = {'dealership': int(query_string['dealerId'][0].replace('"', '')) }

    try:
        authenticator = IAMAuthenticator(settings.CAPSTONE_APIKEY)
        service = CloudantV1(authenticator=authenticator)
        service.set_service_url(settings.CAPSTONE_URL)

        response = service.post_find(
            db=db_name,
            selector=selector,
            fields=["id", "name", "dealership", "review", "purchase", "purchase_date", "car_make", "car_model", "car_year"],
        ).get_result()

        if response['docs']:
            return JsonResponse(response['docs'], safe=False)
        else: 
            return JsonResponse({"error_type": "404", "error_message": "dealerId does not exist"})

    except ApiException as ae:
        return JsonResponse({"error_type": "500", "error_message": ae})


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative



