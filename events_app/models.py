from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
from datetime import date
from datetime import timezone

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your models here.

# =============================
# USER MANAGER
# =============================


class UserManager(models.Manager):
    def reg_validator(self, postData):
        # ---- Declare empty dictionary that will store your error messages.
        errors = {}
#---- NAME ----#
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name must be at least 2 characters long"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must be at least 2 characters long"


# ------- Email -------
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Please input a valid email address!"
        else:
            # searches for email in DB to see if it already exists
            for user in User.objects.all():
                if postData['email'] == user.email:
                    errors['email'] = "Email already exists in our system. Please login in if you're a returning member"

# ------- Password -------
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters long!"
        elif postData['password'] != postData['password2']:
            errors['password2'] = "Passwords do not match!"

        return errors

    def log_validator(self, postData):
        # instantiate empty errors obj
        errors = {}

        # query for users info based on email input provided by user
        user_info = User.objects.filter(email=postData['email_input'])

        if not user_info:
            errors['email_input'] = "Email does not exist. Please register before logging in."

        else:
            # our user exists
            user = User.objects.get(email=postData['email_input'])
            if not bcrypt.checkpw(postData['password_input'].encode(), user.password.encode()):
                errors['password_input'] = "Password or email is not correct"

        return errors

    def not_logged_validator(self):
        # instatiate empty error obj
        errors = {}
        errors['no'] = "Please log in first."
        return errors

# =============================
# EVENT MANAGER
# =============================


class EventManager(models.Model):
    def event_validator(self, postData):
        # instantiate an empty object
        errors = {}

    # ------  Event name   ------#
        if len(postData['event']) < 3:
            errors['event'] = "Please enter a valid event name"
    # ------   Description ------#
        if len(postData['desc']) < 12:
            errors['desc'] = "Description should be 20 characters or longer "
        return errors

# classes are singular.


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

# classes are singular.


class Event(models.Model):
    event_name = models.CharField(max_length=255)
    desc = models.TextField(max_length=500)
    date = models.DateField()
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    location = models.CharField(max_length=255)
    creator_of_event = models.ForeignKey(
        User, related_name="created_events", on_delete=models.CASCADE)
    users_who_like = models.ForeignKey(
        User, related_name="liked_events", on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = EventManager()
