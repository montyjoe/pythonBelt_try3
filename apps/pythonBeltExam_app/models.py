from __future__ import unicode_literals
from django.db import models
import re, datetime, bcrypt
from datetime import date, timedelta

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
    def register(self, data):
        # data == views -> register -> context
        errors = []
        if len(data['fnom']) < 2:
            errors.append("First name must be at least two characters long.")
        if not data['fnom'].isalpha():
            errors.append("First name may only be letters.")
        if len(data['lnom']) < 2:
            errors.append("Last name must be at least two characters long.")
        if not data['lnom'].isalpha():
            errors.append("Last name may only be letters.")
        if not EMAIL_REGEX.match(data['e_address']):
            errors.append("Please enter a valid email address")
        try:
            User.objects.get(email_address=data['e_address'])
            errors.append("This email is already registered.")
        except:
            pass
        if len(data['pass_word']) < 8:
            errors.append("Password name must be at least eight characters long.")
        if data['pass_word'] != data['confirm_pass_word']:
            errors.append("Passwords do not match.")
        if data['dob'] == '':
            errors.append("Birthday is required.")
        elif datetime.datetime.strptime(data['dob'], '%Y-%m-%d') >= datetime.datetime.now():
            errors.append("Birthday may not be in the future.")
        print datetime.datetime.now()
        if len(errors) == 0:
            print('no errors')
            data['pass_word'] = bcrypt.hashpw(data['pass_word'].encode('utf-8'), bcrypt.gensalt())
            new_user = User.objects.create(f_name=data['fnom'], l_name=data['lnom'], email_address=data['e_address'], pw=data['pass_word'], birthday=data['dob'])
            return {
                'new': new_user,
                'error_list': None
            }
        else:
            print(errors)
            return {
                'new': None,
                'error_list': errors
            }
    def login(self, log_data):
        # log_data == views -> login -> context
        errors = []
        # check if user's account exists
        try:
            found_user = User.objects.get(email_address=log_data['e_mail'])
            if bcrypt.hashpw(log_data['p_word'].encode('utf-8'), found_user.pw.encode('utf-8')) != found_user.pw.encode('utf-8'):
                errors.append("Incorrect password.")
        except:
            # email does not exist
            errors.append("Email address not found.")
        if len(errors) == 0:
            return {
                'logged_user': found_user,
                'list_errors': None
            }
        else:
            return {
                'logged_user': None,
                'list_errors': errors
            }

class AppointmentManager(models.Manager):
    def add_appointment(self, data):
        # data == views -> register -> context
        errors = []
        if data['a_date'] == '':
            errors.append("Date is required.")
        elif datetime.datetime.strptime(data['a_date'], '%Y-%m-%d') < datetime.datetime.now() - timedelta(days=1):
            errors.append("Please enter a current or future date.")
        if data['a_time'] == '':
            errors.append("Time is required.")
        if data['a_task'] == "":
            errors.append("Please enter a task.")
        if len(errors) == 0:
            print('no errors')
            new_appointment = appointment.objects.create(task=data['a_task'], status='Pending', date=data['a_date'], time=data['a_time'])
            return {
                'new_appt': new_appointment,
                'error_list': None
            }
        else:
            print(errors)
            return {
                'new_appt': None,
                'error_list': errors
            }
    def update_appt(self, data):
        errors = []
        print data['up_date']
        if data['up_date'] == '':
            errors.append("Date is required.")
        # elif datetime.datetime.strptime(data['a_date'], '%Y-%m-%d') < datetime.datetime.now():
        #     errors.append("Please enter a current or future date.")
        if data['up_time'] == '':
            errors.append("Time is required.")
        if data['up_task'] == "":
            errors.append("Please enter a task.")
        if len(errors) == 0:
            print('no errors')
            updated_appointment = appointment.objects.get(id=data['appt_id'])
            print updated_appointment
            # .update(task=data['up_task'], status= data['up_status'], date= data['up_date'], time= data['up_time'])
            return {
                'updated_appt': updated_appointment,
                'error_list': None
            }
        else:
            print(errors)
            return {
                'updated_appt': None,
                'error_list': errors
            }

class User(models.Model):
    f_name = models.CharField(max_length=255)
    l_name = models.CharField(max_length=255)
    email_address = models.CharField(max_length=255)
    pw = models.CharField(max_length=255)
    birthday = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now =True)
    objects = UserManager()

class appointment(models.Model):
    task = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    date = models.DateField()
    time = models.TimeField()
    objects = AppointmentManager()
