from django.shortcuts import render, redirect
from django.contrib import messages
from models import *


def session_check(request):
    if 'user' in request.session:
        return True
    else:
        return False

def index(request):
    if session_check(request):
        return redirect('/dashboard')
        # ^^ REDIRECT TO APP ^^
    else:
        return render(request,'poke/loginReg.html')

def login_reg(request):
    if request.POST['action'] == 'register':
        result = User.objects.validate_reg(request)

    elif request.POST['action'] == 'login':
        result = User.objects.validate_login(request)

    if result[0] == False:
        print_errors(request, result[1])
        return redirect('/')

    return log_user_in(request, result[1])

def print_errors(request, error_list):
    for error in error_list:
        messages.add_message(request, messages.INFO, error)

def log_user_in(request, user):
    request.session['user'] = {
        'user_id': user.id,
        'name': user.name
    }
    return redirect('/dashboard')

    # ^^ REDIRECT TO APP ^^

def logout(request):
    request.session.clear()
    return redirect('/')

def dashboard(request):
	if not session_check(request):
		return redirect('/')

	ps = Poke.objects.filter(pokee__id=int(request.session['user']['user_id']))
	pcount = {}
	for p in ps:
		if p.poker.id in pcount:
			pcount[p.poker.id] += 1
		else:
			pcount[p.poker.id] = 1

	psort = []
	while len(pcount) > 0:
		maxp = 0
		key = -1
		for k in pcount:
			if pcount[k] >= maxp:
				maxp = pcount[k]
				key = k
		u = User.objects.get(id=key)
		psort.append((u.alias, maxp))
		pcount.pop(key)

	us = User.objects.exclude(id=int(request.session['user']['user_id']))
	ps = Poke.objects.all()
	users = []
	for u in us:
		count = 0
		for p in ps:
			if p.pokee.id == u.id:
				count += 1
		users.append((u, count))

	u = User.objects.get(id=int(request.session['user']['user_id']))
	context = {
        'alias':u.alias, 
        'pokes':psort, 
        'users':users
    }
	return render(request, 'poke/dashboard.html', context)

    

def poke(request):
	if request.method == 'POST':
		poker = User.objects.get(id=int(request.session['user']['user_id']))
		pokee = User.objects.get(id=int(request.POST['uid']))
		Poke.objects.create(poker=poker, pokee=pokee)
	return redirect('/dashboard')