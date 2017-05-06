from django.shortcuts import render, redirect
from .models import User, appointment
from django.contrib import messages
from datetime import datetime, timedelta
from django.core.urlresolvers import reverse

# Create your views here.
def index(request):
    return render(request, 'pythonBeltExam_app/index.html')

def register(request):
    context = {
        'fnom': request.POST['first_name'],
        'lnom': request.POST['last_name'],
        'e_address': request.POST['email'],
        'pass_word': request.POST['password'],
        'confirm_pass_word': request.POST['confirm'],
        'dob': request.POST['birthdate']
    }
    register_results = User.objects.register(context)
    # register_results == models -> returned list with user&errors
    if register_results['new'] != None:
        # created new User
        request.session['user_id'] = register_results['new'].id
        request.session['user_fname'] = register_results['new'].f_name
        return redirect('/appointments')
    else:
        for error_str in register_results['error_list']:
            messages.add_message(request, messages.ERROR, error_str)
        return redirect('/')

def login(request):
    p_data = {
        'e_mail': request.POST['email'],
        'p_word': request.POST['password']
    }
    login_results = User.objects.login(p_data)
    if login_results['logged_user'] != None:
        # created new User
        request.session['user_id'] = login_results['logged_user'].id
        request.session['user_fname'] = login_results['logged_user'].f_name
        return redirect('/appointments')
    else:
        for error in login_results['list_errors']:
            messages.add_message(request, messages.ERROR, error)
        return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')

def appointments(request):
    request.session['today'] = datetime.now().strftime('%Y-%m-%d')
    context = {
        'today_appts': appointment.objects.filter(date=request.session['today']).order_by('date', 'time'),
        'other_appts': appointment.objects.exclude(date=request.session['today']).order_by('date', 'time'),
    }
    # if 'user_id ' not in request.session:
    #     messages.add_message(request, messages.ERROR, "You must login before accessing that page!")
    #     return redirect('/')

    return render(request, 'pythonBeltExam_app/appointments.html', context)

def add_appointment(request):
    add_appt_context = {
        'a_task': request.POST['appt_task'],
        'a_date': request.POST['appt_date'],
        'a_time': request.POST['appt_time'],
    }
    add_appt_results = appointment.objects.add_appointment(add_appt_context)
    if add_appt_results['new_appt'] != None:
        return redirect('/appointments')
    else:
        for error_str in add_appt_results['error_list']:
            messages.add_message(request, messages.ERROR, error_str)
        return redirect('/appointments')

def update_page(request, appointment_id):
    request.session['appt_id'] = appointment_id
    update_page_context = {
        'this_appt': appointment.objects.filter(id=appointment_id),
    }
    # if 'user_id ' not in request.session:
    #     messages.add_message(request, messages.ERROR, "You must login before accessing that page!")
    #     return redirect('/')

    return render(request, 'pythonBeltExam_app/update.html', update_page_context)

def update(request):
    if request.method == "POST":
        update_context = {
            'up_task': request.POST['update_task'],
            'up_date': request.POST['update_date'],
            'up_time': request.POST['update_time'],
            'up_status': request.POST['update_status'],
            'appt_id': request.session['appt_id']
        }
        update_appt_results = appointment.objects.update_appt(update_context)
        if update_appt_results['updated_appt'] != None:
            return redirect('/appointments')
        else:
            for error_str in update_appt_results['error_list']:
                messages.add_message(request, messages.ERROR, error_str)
            id_appt = request.session['appt_id']
            return redirect(reverse('update_page', kwargs={'appointment_id':id_appt}))

def delete(request, appointment_id):
    a_appointment = appointment.objects.get(id= appointment_id)
    a_appointment.delete()
    return redirect('/appointments')





# end
