import requests
import json
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
# import related models here
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibmcloudant.cloudant_v1 import AllDocsQuery, CloudantV1
from ibm_cloud_sdk_core import ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from dotenv import dotenv_values
from django.conf import settings
from urllib.parse import urlparse, parse_qs
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
import requests
import json
from .models import CarDealer
from requests.auth import HTTPBasicAuth

def analyze_review_sentiments(dealer_review):
    """
    results = get_request(text=dealer_review,
                url="https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/f2965ae5-49b3-4a48-96fd-4c83a2f0992c",
                api_key="TwRA5GvEKIaYyM3WxvsmHOkQGgm5qKJBMdL1xlG-T2U9",
                version="2022-04-07")
    """
    authenticator = IAMAuthenticator('TwRA5GvEKIaYyM3WxvsmHOkQGgm5qKJBMdL1xlG-T2U9')
    nlu = NaturalLanguageUnderstandingV1(
        version='2022-04-07',
        authenticator=authenticator
    )

    nlu.set_service_url('https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/f2965ae5-49b3-4a48-96fd-4c83a2f0992c')
    
    results = nlu.analyze(text=dealer_review,
                          features=Features(entities=EntitiesOptions(emotion=True, sentiment=True, limit=2))).get_result()
    #print(results)

    return results["entities"]

def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))

        # Call get method of requests library with URL and parameters
    params = dict()
    params["text"] = kwargs["text"] if "text" in kwargs else ""
    params["version"] = kwargs["version"] if "version" in kwargs else ""
    params["features"] = kwargs["features"] if "features" in kwargs else ""
    params["return_analyzed_text"] = kwargs["return_analyzed_text"] if "return_analyzed_text" in kwargs else ""
    response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                        auth=HTTPBasicAuth('apikey', kwargs["api_key"] if "api_key" in kwargs else ""))

    #status_code = response.status_code
    #print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

def post_request(url, json_payload, **kwargs):
    requests.post(url, params=kwargs, json=json_payload)

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

def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        reviews = json_result["reviews"]
        # For each dealer object
        for review in reviews:
            # Get its content in `doc` object
            # Create a CarDealer object with values in `doc` object
            sentiment = analyze_review_sentiments(review["review"])
            review_obj = DealerReview(id=review["id"], dealership=review["dealership"], name=review["name"], 
                                      purchase=review["purchase"], review=review["review"], purchase_date=review["purchase_date"],
                                      car_make=review["car_make"], car_model=review["car_model"], car_year=review["car_year"], 
                                      sentiment=sentiment)
            results.append(review_obj)

    print("---reviews---")
    print(review_obj)
    print("---reviews---")

    return results




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



