import requests
import json
from .models import CarDealer
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    
    api_key = kwargs.get("api_key")
    print("GET from {} ".format(url))
    try:
        if api_key:
            params = dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]
            response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', api_key))
        else:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        print("Network exception occurred")

    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, payload, **kwargs):
    print(kwargs)
    print("POST to {} ".format(url))
    print(payload)
    response = requests.post(url, params=kwargs, json=payload)
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs, requests.get(url, params=params, headers={'Content-Type': 'application/json'}, auth=HTTPBasicAuth('apikey', api_key)):
    if api_key:
   # Basic authentication GET
   request.get(url, params=params, auth=True)
 else:
   # no authentication GET
   request.get(url, params=params)
    results = []
    state = kwargs.get("state")
    # Call get_request with a URL parameter
    if state:
        json_result = get_request(url, state=state)
    else:
        json_result = get_request(url)

    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["body"]["rows"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"],
                                    full_name=dealer_doc["full_name"], id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    dealer_id = kwargs['dealer_id']
    # Call get_request with a URL parameter
    json_result = get_request(url, dealerId=dealer_id)
    if json_result:
        # Get the row list in JSON as dealers
        reviews = json_result["docs"]
        # For each dealer object
        for review in reviews:            
            # Create a DealerReview object with values in `doc` object
            if review['purchase'] == True:
                review_obj = DealerReview(car_make=review["car_make"], car_model=review["car_model"],
                                    car_year=review["car_year"], dealership=review["dealership"],
                                    name=review["name"], purchase=review["purchase"],
                                    purchase_date=review["purchase_date"], review=review["review"],
                                    sentiment = analyze_review_sentiments(review["review"]))
                results.append(review_obj)
            else:
                review_obj = DealerReview(car_make='None', car_model='No car',
                                    car_year=0, dealership=review["dealership"],
                                    name=review["name"], purchase=review["purchase"],
                                    purchase_date='', review=review["review"],
                                    sentiment = analyze_review_sentiments(review["review"]))
                results.append(review_obj)
    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(text):
    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/b3e41192-1cf4-4e60-bfa0-28d4c25800c8"
    api_key = "TxOPysJNogaETEXbR7N3UMGwLB2Xlqx0LE6LxK4B2nHc"
    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2021-08-01',authenticator=authenticator)
    natural_language_understanding.set_service_url(url)
    response = natural_language_understanding.analyze( text=text+"hello hello hello",features=Features(sentiment=SentimentOptions(targets=[text+"hello hello hello"]))).get_result()
    label=json.dumps(response, indent=2)
    label = response['sentiment']['document']['label']


