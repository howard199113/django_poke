from __future__ import unicode_literals
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
import bcrypt
from datetime import date, datetime
from dateutil.parser import parse as parse_date

# Create your models here.
class UserManager(models.Manager):
    def validate_reg(self, request):
        errors = self.validate_inputs(request)
        if errors:
            return (False, errors)

        pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())

        user = self.create(name=request.POST['name'], alias=request.POST['alias'], email=request.POST['email'], password=pw_hash, birth=request.POST['birth'])

        return (True, user)

    def validate_login(self, request):

        try:
            user = User.objects.get(email=request.POST['email'])
            password = request.POST['password'].encode()
            if bcrypt.checkpw(password, user.password.encode()):
                return (True, user)

        except ObjectDoesNotExist:
            pass

        return (False, ["Invalid login."])


    def validate_inputs(self, request):
        errors = []
        birth_date = request.POST['birth'] 

        if not request.POST['name']:
            errors.append('Name cannot be blank.')
        elif len(request.POST['name']) < 3:
            errors.append('Name must be more than 3 characters.')
        if not request.POST['alias']:
            errors.append('Please enter a alias.')
        if len(request.POST['password']) < 8:
            errors.append('Password must be at least 8 characters.')
        if request.POST['password'] != request.POST['confirm']:
            errors.append('Password and password confirm must match.')
        if birth_date:
            birth_date = parse_date(birth_date).date()
            if birth_date > date.today():
                errors.append('Birth date must be today or in the past.')
        else:
            errors.append('Please add a birth date.')        

        return errors



class User(models.Model):
    name = models.CharField(max_length = 50)
    alias = models.CharField(max_length = 50)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    birth = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

class Poke(models.Model):
	poker = models.ForeignKey(User, related_name='poker')
	pokee = models.ForeignKey(User, related_name='pokee')
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
