from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import Customer
from .forms import CreateUserForm, CustomerForm, DeviceForm
from django.contrib.auth.decorators import login_required
import os
from django_channels import settings
from django.contrib import messages
from datetime import date
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import user_passes_test
from security.views import is_admin
from customer.filters import DeviceFilter, customerFilter 
import mysql.connector
from mysql.connector import Error

# Create your views here.


def terms(request):
	if request.method == 'POST':
		terms_accepted = request.POST.get('terms')
		if terms_accepted == 'Y':
			print('request.user.is_authenticated', request.user.is_authenticated)
			if request.user.is_authenticated:
				try:
					customer = Customer.objects.get(user=request.user)
					print('customer = try : ', customer)
				except:
					customer = Customer.objects.get()
					print('customer = except : ', customer)
				
				customer.terms = 'Y'
				customer.terms_accepted_at = date.today()
				customer.save()
				return redirect("user_profile")
			else:
				messages.warning(request, "Please login")
				return redirect("account_signup")
		else:
			logout(request)
			return redirect('account_signup')
	else:
		try:
			customer = Customer.objects.get(user=request.user)
			my_terms = customer.terms
		except:
			my_terms = 'N'
		
		if my_terms == 'N' or my_terms == '':
			return render(request, "../templates/snippets/terms.html")
		else:
			print('going to user profile')
			return redirect("user_profile")


#@login_required(login_url="login")
def user_profile(request):
	print('okay here I am')
	customer = Customer.objects.get(user=request.user)
	if request.method == 'POST':
		customer = CustomerForm(request.POST, request.FILES, instance=customer)
		if customer.is_valid():
			customer = customer.save(commit=False)
			customer.user = request.user
			if request.POST.get('address_line_1'):
				customer.address_line_1 = request.POST.get('address_line_1')
			if request.POST.get('address_line_2'):
				customer.address_line_2 = request.POST.get('address_line_2')
			if request.POST.get('city'):
				customer.city = request.POST.get('city')
			if request.POST.get('province'):
				customer.province = request.POST.get('province')
			if request.POST.get('postal_code'):
				customer.postal_code = request.POST.get('postal_code')
			if request.POST.get('country'):
				customer.country = request.POST.get('country')
			if request.POST.get('gender'):
				customer.gender = request.POST.get('gender')
			if request.POST.get('name_1'):
				customer.name_1 = request.POST.get('name_1')
			if request.POST.get('name_2'):
				customer.name_2 = request.POST.get('name_2')
			# New input Fields for Customer
			if request.user.email != '':
				customer.email = request.user.email
				my_email = request.user.email
			else:
				if request.POST.get('email'):
					customer.email = request.POST.get('email')
					my_email = request.POST.get('email')
				else:
					my_email = customer.email
			
			if request.POST.get('organisation'):
				customer.organisation = request.POST.get('organisation')
			if request.POST.get('prefered_correspondence'):
				customer.prefered_correspondence = request.POST.get('prefered_correspondence')
			
			if request.POST.get('contact_number'):
				customer.contact_number = request.POST.get('contact_number')
			if request.POST.get('profile_pic'):
				customer.profile_pic = request.POST.get('profile_pic')
			try:
				customer.profile_pic

				if request.FILES.get('profile_pic'):
					if customer.profile_pic != request.FILES.get('profile_pic') or customer.profile_pic != 'None':
						delete_flag = 1
						delete_path = customer.profile_pic
						customer.profile_pic = request.FILES.get('profile_pic')
					elif customer.profile_pic != request.FILES.get('profile_pic'):
						customer.profile_pic = request.FILES.get('profile_pic')

			except:
				if request.FILES.get('profile_pic'):
					customer.profile_pic = request.FILES.get('profile_pic')
			my_postal_address = f"{request.POST.get('address_line_1')} {request.POST.get('address_line_2')} {request.POST.get('city')} {request.POST.get('province')} {request.POST.get('country')} {request.POST.get('postal_code')}"
			my_postal_address = ''
			print('my_postal_address', my_postal_address)
			print('Going to save 2')
			if not my_postal_address:
				print('postal Adress Set None')
				my_postal_address = None

			my_output = ''
			
			update_second_db_customer(
				request.POST.get('name_1'), 
				request.POST.get('name_2'),
				my_email,
				request.POST.get('contact_number'), # cell 
				request.POST.get('contact_number'), # landline
				my_postal_address,
				request.user.id,
				request.POST.get('organisation'),
				request.POST.get('prefered_correspondence'),
				request.user.username,
				my_output,
			)

			customer.save()

			if request.FILES.get('profile_pic'):
				# Delete profile pic
				if delete_flag == 1:
					os.remove(settings.MEDIA_ROOT.replace("\media", "\\media\\") + str(delete_path).replace("/", "\\"))

			messages.success(request, "Profile Saved")
			
			return redirect("dashboard")
			#render(request, "../templates/dashboard/dashboard.html")

		else:
			messages.error(request, "Invalid Form")

	else:
		customer = Customer.objects.get(user=request.user)
		if customer.name_1 == '':
			context = {
				'form': customer
			}
			delete_flag = 0
			return render(request, "../templates/customer/user_profile.html", context)
			
		else:
			return redirect("dashboard")
			
	context = {
		'form': customer
	}
	delete_flag = 0
	return render(request, "../templates/customer/user_profile.html", context)


def dashboard_user_profile(request):
	
	customer = Customer.objects.get(user=request.user)
	if request.method == 'POST':
		customer = CustomerForm(request.POST, request.FILES, instance=customer)
		if customer.is_valid():
			customer = customer.save(commit=False)
			customer.user = request.user
			if request.POST.get('address_line_1'):
				customer.address_line_1 = request.POST.get('address_line_1')
			if request.POST.get('address_line_2'):
				customer.address_line_2 = request.POST.get('address_line_2')
			if request.POST.get('city'):
				customer.city = request.POST.get('city')
			if request.POST.get('province'):
				customer.province = request.POST.get('province')
			if request.POST.get('postal_code'):
				customer.postal_code = request.POST.get('postal_code')
			if request.POST.get('country'):
				customer.country = request.POST.get('country')
			if request.POST.get('gender'):
				customer.gender = request.POST.get('gender')
			if request.POST.get('name_1'):
				customer.name_1 = request.POST.get('name_1')
			if request.POST.get('name_2'):
				customer.name_2 = request.POST.get('name_2')
			# New input Fields for Customer
			if request.user.email != '':
				customer.email = request.user.email
				my_email = request.user.email
			else:
				if request.POST.get('email'):
					customer.email = request.POST.get('email')
					my_email = request.POST.get('email')
			
			if request.POST.get('organisation'):
				customer.organisation = request.POST.get('organisation')
			if request.POST.get('prefered_correspondence'):
				customer.prefered_correspondence = request.POST.get('prefered_correspondence')
			
			if request.POST.get('contact_number'):
				customer.contact_number = request.POST.get('contact_number')
			if request.POST.get('profile_pic'):
				customer.profile_pic = request.POST.get('profile_pic')
			try:
				customer.profile_pic

				if request.FILES.get('profile_pic'):
					if customer.profile_pic != request.FILES.get('profile_pic') or customer.profile_pic != 'None':
						delete_flag = 1
						delete_path = customer.profile_pic
						customer.profile_pic = request.FILES.get('profile_pic')
					elif customer.profile_pic != request.FILES.get('profile_pic'):
						customer.profile_pic = request.FILES.get('profile_pic')

			except:
				if request.FILES.get('profile_pic'):
					customer.profile_pic = request.FILES.get('profile_pic')
			my_postal_address = f"{request.POST.get('address_line_1')} {request.POST.get('address_line_2')} {request.POST.get('city')} {request.POST.get('province')} {request.POST.get('country')} {request.POST.get('postal_code')}"
			my_postal_address = ''
			print('my_postal_address', my_postal_address)
			print('Going to save 2')
			if not my_postal_address:
				print('postal Adress Set None')
				my_postal_address = None

			my_output = ''
			
			update_second_db_customer(
				request.POST.get('name_1'), 
				request.POST.get('name_2'),
				my_email,
				request.POST.get('contact_number'), # cell 
				request.POST.get('contact_number'), # landline
				my_postal_address,
				request.user.id,
				request.POST.get('organisation'),
				request.POST.get('prefered_correspondence'),
				request.user.username,
				my_output,
			)

			customer.save()

			if request.FILES.get('profile_pic'):
				# Delete profile pic
				if delete_flag == 1:
					os.remove(settings.MEDIA_ROOT.replace("\media", "\\media\\") + str(delete_path).replace("/", "\\"))

			messages.success(request, "Profile Saved")
			
			return redirect("dashboard")
			#render(request, "../templates/dashboard/dashboard.html")

		else:
			messages.error(request, "Invalid Form")

	else:
		customer = Customer.objects.get(user=request.user)
		if customer.name_1 == '':
			context = {
				'form': customer
			}
			delete_flag = 0
			return render(request, "../templates/customer/dashboard_user_profile.html", context)
			
		else:
			context = {
				
				'form': customer
			}
			
			return render(request, "../templates/customer/dashboard_user_profile.html", context)
	context = {
		'form': customer
	}
	delete_flag = 0
	return render(request, "../templates/customer/dashboard_user_profile.html", context)


def profile(request):
	print('profile view')


@user_passes_test(is_admin, login_url="login")
@login_required(login_url="login")
def admin_list_customer(request):
	customers = Customer.objects.all()
	initial_customer_count = customers.count()

	myFilter = customerFilter(request.GET, queryset=customers)
	
	# rebuilt list
	customers = myFilter.qs

	# Paginator
	page_num = request.GET.get('page', 1)
	paginator = Paginator(customers, 6) # 6 customers per page

	try:
		customers = paginator.page(page_num)
	except PageNotAnInteger:
		# if page is not an integer, deliver the first page
		customers = paginator.page(1)
	except EmptyPage:
		# if the page is out of range, deliver the last page
		customers = paginator.page(paginator.num_pages)

	name_1 = request.GET.get('name_1')
	email = request.GET.get('email')
	address_line_1 = request.GET.get('address_line_1')
	registration_start_date = request.GET.get('registration_start_date')

	if name_1 == None:
		name_1 = ''
	if email == None:
		email = ''
	if address_line_1 == None:
		address_line_1 = ''
	if registration_start_date == None:
		registration_start_date = ''
	print('count', customers)
	context = {
		'form': customers,
		'page_obj': customers,
		'name_1': name_1,
		'email': email,
		'address_line_1': address_line_1,
		'registration_start_date': registration_start_date,
	}
	return render(request, '../templates/msiapp_templates/admin_folder/admin_customer_list.html', context)
	

def update_second_db_customer(name_1, name_2, my_email, cell_contact_number, landline_contact_number, my_postal_address, user_id, organisation, prefered_correspondence, user_name, my_output):
	print('Im in the customer update')
	my_host = "neura.dyndns.org"
	my_user = "Quinn"
	my_password = "QuinnLondon#1"
	my_database = "neuraCore"
	my_port = 2505
	print('my list+++++===>', name_1, name_2, my_email, cell_contact_number, landline_contact_number, my_postal_address, user_id, organisation, prefered_correspondence, user_name, my_output)
	try:
		connection = mysql.connector.connect(host=my_host, user=my_user, password=my_password, database=my_database, port=my_port)
		cur = connection.cursor()
		

		try:
			returned_list = cur.callproc("UserData", [name_1, name_2, my_email, cell_contact_number, landline_contact_number, my_postal_address, user_id, organisation, prefered_correspondence, user_name, my_output])
			connection.commit()
			print('returned list', returned_list)
		except Error as e:
			print("Error occured ", e)
			print('Error message from 2nd DB what the heck')
	except  Error as e:
		print('why')
		print("Error occured ", e)

	finally:
		if (connection.is_connected()):
			cur.close()
			connection.close()
			print("connection is closed")
