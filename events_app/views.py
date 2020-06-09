from django.shortcuts import render, redirect
# dont forget to import the models
from .models import *
from django.contrib import messages
import bcrypt
# Create your views here.

# ===================================
#  INDEX/ ROOT ROUTE
# ===================================


def index(request):
    return render(request, 'index.html')

# ===================================
#  REGISTER
# ===================================


def register(request):
    if request.POST:
        errors = User.objects.reg_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            # if successful, and there are no errors. we create the user
            user = User.objects.create(
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                email=request.POST['email'],
                password=bcrypt.hashpw(
                    request.POST['password'].encode(), bcrypt.gensalt()).decode()
            )

            # we need to put our user in session
            request.session['user_id'] = user.id

            return redirect('/dashboard')

# ===================================
#  LOG IN
# ===================================


def login(request):
    # if there are any errors that exist within the login validator from models.py, this should
    # throw an error
    # verify this is a post route after form submission

    if request.POST:
        # we call on the login validator from models.py
        errors = User.objects.log_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')

        else:
            # if there are no errors, query for email input
            user = User.objects.get(email=request.POST['email_input'])
            # put the user into session
            request.session['user_id'] = user.id
            return redirect('/dashboard')


def dashboard(request):
    if 'user_id' not in request.session:  # if no one is in session.

        errors = User.objects.not_logged_validator()
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)

            return redirect('/')
    else:
        # if successful log in and reg
        # pull the user from session.
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)  # this is your db query
        context = {
            'user': user
        }
        return render(request, 'dashboard.html', context)


# ===================================
#  LOG OUT
# ===================================


def logout(request):

    request.session.clear()

    return redirect('/')

# ===================================
#  CREATE EVENT
# ===================================


def create_event(request):
    return render(request, 'new.html')

# ===================================
#  POST ROUTE CREATE EVENT
# ===================================


def new_event(request):
    if request.POST:
        errors = Event.objects.event_validator(request.POST)
        # if any errors exist at all
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return (redirect, '/create_event')
    else:

        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)

        event = Event.objects.create(
            event_name=request.POST['event'],
            description=request.POST['desc'],
            date=request.POST['date'],
            location=request.POST['location'],
            creator_of_event=user
        )
        return redirect('dashboard')
