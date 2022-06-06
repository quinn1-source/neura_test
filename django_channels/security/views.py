from atexit import register
from django.shortcuts import render, redirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.contrib import messages
from customer.models import Customer
from django.core.mail import send_mail
from django.contrib.auth.decorators import user_passes_test
from security.forms import UserCreationForm


def loginPage(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')
		
		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			my_user = User.objects.get(username=user)
			print(my_user.id)
			customer = Customer.objects.get(user=my_user)

			if customer.name_1:

				if user.groups.filter(name='admin').exists():
					print('admin_dash')
					return redirect("dashboard")
				elif user.groups.filter(name='customer').exists():
					print('customer')
					# return render(request, '../templates/msiapp_templates/dashboard.html')
					return redirect("dashboard")
				else:
					return redirect("dashboard")
			else:
				# print('request.user.user_groups', request.user.user_groups)
				print('request.user', request.user)
				#if request.user.groups == 'customer':
				if user.groups.filter(name='admin').exists():
					return redirect('admin_user_profile')
				elif user.groups.filter(name='customer').exists():
					return redirect('user_profile')
		else:
			messages.info(request, 'Username OR password is incorrect')

	context = {}
	print('why the error???')
	return redirect('terms')


@login_required(login_url="register")
def logoutUser(request):
	logout(request)
	print('logout')
	context = {}
	return redirect('home')


######################################
# This is actually add customer html #
######################################
def is_admin(user):
    try:
        return user.is_authenticated and user.groups.filter(name='admin').exists()
    except User.DoesNotExist:
        return False


#@user_passes_test(is_admin, login_url="login")
#@login_required(login_url="login")
def registerPage(request):
	print('okay in registration')
	form = UserCreationForm()
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')
			my_admin_flag = request.POST.get('is_admin')
			if my_admin_flag == 'customer':
				group = Group.objects.get(name='customer')
				user.groups.add(group)
			elif my_admin_flag == 'admin':
				group = Group.objects.get(name='admin')
				user.groups.add(group)
			else:
				pass

			my_email = []
			messages.success(request, 'User was created for ' + username)
			my_username = request.POST.get('username')
			my_email = str(request.POST.get('email'))
			my_password = request.POST.get('password1')
			print(my_email)
			# Send Email via code
			send_mail(
				'Neura Email Verification',
				'Please click link and login to complete Registration process. http://127.0.0.1:8000/account/login',
				'sparDjango"gmail.com',
				[my_email],
				fail_silently=False,
			)
			if request.user.groups == 'customer':
				return redirect('list_customer')
			else:
				return redirect('admin_list_customer')
		else:
			my_username = request.POST.get('username')
			my_email = request.POST.get('email')
			context = {
				'form': form,
				'my_username': my_username,
				'my_email': my_email,
				}
			messages.error(request, "Username Already Exists")
			return render(request, "msiapp_templates/admin_folder/admin_customer_add.html", context)
	else:

		context = {
					'form': form,
					}
		return redirect('admin_list_customer')


