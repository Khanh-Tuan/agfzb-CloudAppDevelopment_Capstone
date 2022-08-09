from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)

# Create an `about` view to render a static about page
# def about(request):
# ...


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method =="GET":
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
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

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
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
# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        url = "https://4695b995-5eb0-4c4f-abeb-1c5a3d07ac9f-bluemix.cloudant.com/api/dealerships"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        context = {}
        context['dealerships'] = dealerships
        # Return a list of dealer short name
        return render(request, 'djangoapp/index.html', context)
        


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        url = "https://4695b995-5eb0-4c4f-abeb-1c5a3d07ac9f-bluemix.cloudant.com/api/reviews"
        reviews = get_dealer_reviews_from_cf(url, dealer_id=dealer_id)
        context['reviews'] = reviews
        context['dealer_id'] = dealer_id
        return render(request, 'djangoapp/dealer_details.html', context)


# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    user = request.user
    context = {}
    if request.method == "GET":
        cars = CarModel.objects.filter(dealer_id=dealer_id)
        context['cars'] = cars
        context['dealer_id'] = dealer_id
        return render(request, 'djangoapp/add_review.html', context)
    elif request.method == "POST":
        if user.is_authenticated:
            url = 'https://4695b995-5eb0-4c4f-abeb-1c5a3d07ac9f-bluemix.cloudant.com/api/reviews'
            review = {}
            review['name'] = user.first_name + ' ' + user.last_name
            review['dealership'] = dealer_id
            review['review'] = request.POST['content']
            review['purchase'] = request.POST.get("purchasecheck") == 'on'
            if request.POST.get("purchasecheck") == 'on':
                review['purchase_date'] = request.POST["purchasedate"]
                car = CarModel.objects.get(pk=request.POST["car"])
                review['car_make'] = car.carmake.name
                review['car_model'] = car.name
                review['car_year'] = car.year.strftime("%Y")
            json_payload = {}
            json_payload['review'] = review
            print (json_payload)
            result = post_request(url, json_payload, dealerId=dealer_id)
            print ('POST result: ')
            print (result)
            context["dealer_id"] = dealer_id
            return redirect("/djangoapp/dealer/" + str(dealer_id), context)
