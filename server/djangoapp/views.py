from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
from . import restapis
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

def profile(request):
    data = {
        'name': 'Vitor',
        'location': 'Finland',
        'is_active': True,
        'count': 28
    }
    return JsonResponse(data)

def about(request):
    context = {}
    return render(request, 'djangoapp/about.html', context)

def contact(request):
    context = {}
    return render(request, 'djangoapp/contact.html', context)

def is_authenticated_post_api_request(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            return True
        else:
            return False
    else:
        return False

def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/index.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)

def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)


# Create an `about` view to render a static about page
# def about(request):
# ...


# Create a `contact` view to return a static contact page
#def contact(request):

# Create a `login_request` view to handle sign in request
# def login_request(request):
# ...

# Create a `logout_request` view to handle sign out request
# def logout_request(request):
# ...

# Create a `registration_request` view to handle sign up request
# def registration_request(request):
# ...

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        url = "https://ca3ab0e1.us-south.apigw.appdomain.cloud/api/dealership"
        # Get dealers from the URL
        dealerships = restapis.get_dealers_from_cf(url)
        # Concat all dealer's short name
        # Return a list of dealer short name
        context = {}
        context["dealerships"] = dealerships

        return render(request, "djangoapp/index.html", context)

def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        str_id = str(dealer_id)
        url = f'https://ca3ab0e1.us-south.apigw.appdomain.cloud/api/review?dealerId={str_id}'

        reviews = restapis.get_dealer_reviews_from_cf(url)
        context = {}
        context["reviews"] = reviews

        for review in reviews:
            print("-----")
            print(review)
            print("-----")


        return render(request, 'djangoapp/dealer_details.html', context)

def add_review(request, dealer_id):
    if request.user.is_authenticated:
        review = {}
        json_payload = {}

        review["car_make"] = "Audi"
        review["car_model"] = "A6"
        review["car_year"] = 2010
        review["dealership"] = dealer_id
        review["name"] = "Adam Roberts"
        review["purchase"] = True
        review["purchase_date"] = datetime.utcnow().isoformat()
        review["review"] = "Great car, though a little expensive."

        json_payload["review"] = review
        result = restapis.post_request('https://ca3ab0e1.us-south.apigw.appdomain.cloud/api/review', json_payload)
        return JsonResponse(result, safe=False)
    else:
        return JsonResponse({ "error": "Invalid credentials" })


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

