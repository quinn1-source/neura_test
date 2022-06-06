from multiprocessing import context
from django.shortcuts import render, redirect
from customer.utils import get_plot, get_usage_plot
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from customer.models import Customer, Device, DeviceAuthored
from customer.forms import CreateUserForm, CustomerForm, DeviceForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
import os
from django_channels import settings
from customer.filters import DeviceFilter, customerFilter 
from .insert_test import day_django
from datetime import date, timedelta, datetime
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import user_passes_test
from customer.views import admin_list_customer
from security.views import is_admin
import mysql.connector
from mysql.connector import Error


@login_required(login_url="login")
def device(request):
	device = ''
	if request.method == 'POST':

		device = DeviceForm(request.POST, request.FILES)
		customer = Customer.objects.get(user=request.user)
		my_output = ''
		if device.is_valid():
			update_second_db_device(device, customer, my_output)
			print('my_output', my_output)
			if my_output == 0:
				Device.objects.create(
					name = request.POST.get('name'),
					address = 'Neura',
					added_by_user = 'System Generated',
					cus_id = request.POST.get('customer_id'),

				)
				# Goes to signals.py after saving Device.
				messages.success(request, "Device Saved")
			elif my_output == 1:
				messages.error(request, "Incorrect Device Type")
				return redirect("customer_add_device")
			elif my_output == 2:
				messages.error(request, "Device Not Registered. Please Check Correct Device Id")
				return redirect("customer_add_device")
			elif my_output == 3:
				messages.error(request, "Gateway Device Incorrect")
				return redirect("customer_add_device")
			elif my_output == 4:
				messages.error(request, "Location Not Found")
				return redirect("customer_add_device")
			elif my_output == 5:
				messages.error(request, "Concession Area Not Found")
				return redirect("customer_add_device")
			else:
				messages.error(request, "Technical Error Please Contact Helpdesk")
				return redirect("customer_add_device")

			# Goes to signals.py after saving Device.
			return redirect("dashboard")

		else:
			messages.error(request, "Invalid Form, Device Add Failed")

	context = {
		'form': device
	}
	delete_flag = 0
	return render(request, '../templates/msiapp_templates/customer_device_add.html')


@login_required(login_url="login")
def customer_add_device(request):
	device = ''
	if request.method == 'POST':
		user = request.user
		try:
			user = User.objects.get(username=user)
		except:
			messages.warning(request, 'User does not exist. Please check username')
			return redirect('customer_add_device')
		
		device = DeviceForm(request.POST, request.FILES)
		customer = Customer.objects.get(user=request.user)

		my_output = ''
		if device.is_valid():
			my_returned_value = update_second_db_device(request.POST.get('name'), str(request.user), my_output)
			my_output = my_returned_value[2]

			if my_output == 0:
				Device.objects.create(
					name = request.POST.get('name'),
					address = request.POST.get('address'),
					added_by_user = 'System Generated',
					cus_id = request.POST.get('customer_id'),

				)
				# Goes to signals.py after saving Device.
				messages.success(request, "Device Saved")
			elif my_output == 1:
				print('In error 1')
				messages.error(request, "Incorrect Device Type")
				return redirect("dashboard")
			elif my_output == 2:
				messages.error(request, "Device Not Registered. Please Check Correct Device Id")
				return redirect("dashboard")
			elif my_output == 3:
				messages.error(request, "Gateway Device Incorrect")
				return redirect("dashboard")
			elif my_output == 4:
				messages.error(request, "Location Not Found")
				return redirect("dashboard")
			elif my_output == 5:
				messages.error(request, "Concession Area Not Found")
				return redirect("dashboard")
			else:
				print('In error else')
				messages.error(request, "Technical Error Please Contact Helpdesk")
				return redirect("customer_add_device")

			return redirect("dashboard")

		else:
			messages.error(request, "Invalid Form, Device Add Failed")

	context = {
		'form': device
	}
	delete_flag = 0
	return render(request, '../templates/msiapp_templates/customer_device_add.html')


@user_passes_test(is_admin, login_url="login")
@login_required(login_url="login")
def admin_add_device(request):
	device = ''
	if request.method == 'POST':
		user = request.POST.get('customer_id')
		try:
			user = User.objects.get(username=user)
		except:
			messages.warning(request, 'User does not exist. Please check username')
			return redirect('admin_add_device')

		device = DeviceForm(request.POST, request.FILES)
		customer = Customer.objects.get(user=user)
		
		if device.is_valid():
			Device.objects.create(
				name = request.POST.get('name'),
				address = request.POST.get('address'),
				added_by_user = request.user.username,
				cus_id = customer.id,
			)
			# Goes to signals.py after saving Device.
			messages.success(request, "Device Saved")
			return redirect("admin_list_device", pk=user.id)

		else:
			messages.error(request, "Invalid Form, Device Add Failed")

	context = {
		'form': device
	}
	delete_flag = 0
	return render(request, '../templates/msiapp_templates/admin_folder/admin_device_add.html')


@user_passes_test(is_admin, login_url="login")
@login_required(login_url="login")
def admin_list_device(request, pk):
	customer = Customer.objects.get(user=request.user)
	if request.method == 'POST':
		device = Device.objects.filter(customers=customer)
		check = len(device)
		if check == 0:
			messages.error(request, "Device not found... ")
			return redirect(admin_list_customer)

		my_filter = DeviceFilter(request.GET, queryset=device)
		meetings = my_filter.qs
		context = {
			'myFilter': my_filter,
			'form': meetings,
			'customer': customer,
		}
		return render(request, '../templates/msiapp_templates/admin_folder/admin_device_list.html', context)
	else:
		devices = Device.objects.all()
		context = {
			'form': devices,
		}
	return render(request, '../templates/msiapp_templates/admin_folder/admin_device_list.html', context)


@login_required(login_url="login")
def edit_device(request, pk):
	device_name = pk
	print('device_name', device_name)
	try:
		device = Device.objects.get(id=device_name)
	except:
		# Goes to signals.py after saving Device.
		messages.error(request, "Device not found!")
		print("Device not found!")
		# Redirect to the same page
		return redirect(list_device)

	# Many to many search
	deviceAuthored = DeviceAuthored.objects.get(device=device)
	customer_device = deviceAuthored.customer.user.username
	print('deviceAuthored', deviceAuthored)
	print('customer_device', customer_device)
	if request.method == 'POST':
		if request.POST.get('name'):
			device.name = request.POST.get('name')
		if request.POST.get('address'):
			device.address = request.POST.get('address')
		#if request.POST.get('customers'):
			# device.customers = request.POST.get('customers')
			# device.customers.set(device)
		device.save()
		messages.success(request, "Device edit saved")
		return redirect(list_device)

	context = {
        'form': device,
		'customer_device': customer_device,
    }
	return render(request, '../templates/msiapp_templates/customer_device_edit.html', context)


@login_required(login_url="login")
def list_device(request):
	user = request.user
	try:
		customer = Customer.objects.get(user=user)
	# 	print(customer)
	except:
		return redirect('home')

	device = Device.objects.filter(customers=customer)
	check = len(device)
	print('check', check)
	if check == 0:
		return redirect('device')

	my_filter = DeviceFilter(request.GET, queryset=device)
	meetings = my_filter.qs
	context = {
        'myFilter': my_filter,
        'form': meetings,
    }
	return render(request, '../templates/msiapp_templates/customer_device_list.html', context)


@user_passes_test(is_admin, login_url="login")
@login_required(login_url="login")
def admin_edit_device(request, pk):
	device_name = pk
	try:
		device = Device.objects.get(id=device_name)
		#print(customer)
	except:
		# Goes to signals.py after saving Device.
		messages.error(request, "Device not found!")
		# Redirect to the same page
		return redirect(edit_device, id)
	
	# Many to many search
	deviceAuthored = DeviceAuthored.objects.get(device=device)
	customer_device = deviceAuthored.customer.user.username
	if request.method == 'POST':
		if request.POST.get('name'):
			device.name = request.POST.get('name')
		if request.POST.get('address'):
			device.address = request.POST.get('address')
		#if request.POST.get('customers'):
			# device.customers = request.POST.get('customers')
			# device.customers.set(device)
		device.save()
		messages.success(request, "Device edit saved")
		return redirect(admin_list_device, pk=deviceAuthored.customer.user.id)

	context = {
        'form': device,
		'customer_device': customer_device,
    }
	return render(request, '../templates/msiapp_templates/admin_folder/admin_device_edit.html', context)


@login_required(login_url="login")
def delete_device(request, pk):
	print('okay in delete')
	device = Device.objects.get(id=pk)
	device_id = device.id
	device_authored = DeviceAuthored.objects.get(device=device)
	customer = device_authored.customer
	device.delete()
	messages.success(request, "Device deleted :  " + str(device_id))
	# Redirect to the same page
	return redirect(list_device)


@user_passes_test(is_admin, login_url="login")
@login_required(login_url="login")
def admin_delete_device(request, pk):
	device = Device.objects.get(id=pk)
	device_id = device.id
	device_authored = DeviceAuthored.objects.get(device=device)
	customer = device_authored.customer
	device.delete()
	messages.success(request, "Device deleted :  " + str(device_id))
	# Redirect to the same page
	return redirect(admin_list_device, pk=customer.user.id)


@login_required(login_url="login")
def customer_list_device_by_customer(request, pk):
	user = pk
	try:
		customer = Customer.objects.get(user=user)
	# 	print(customer)
	except:
		messages.error(request, 'No Device Present. Please Add New Device')
		return redirect('device')
	device = Device.objects.filter(customers=customer)
	check = len(device)

	if check == 0:
		messages.warning(request, 'No Devices Linked To Customer. Please Add Device')
		return redirect('device')

	my_filter = DeviceFilter(request.GET, queryset=device)
	meetings = my_filter.qs
	context = {
        'myFilter': my_filter,
        'form': meetings,
    }
	return render(request, '../templates/msiapp_templates/admin_folder/admin_device_list_by_customer.html', context)


@login_required(login_url="login")
def customer_list_customer_by_device(request, pk):
	customers = []
	print(pk)
	try:
		devices = Device.objects.filter(name=pk)
		print(len(devices))
	except:
		messages.warning(request, 'No Device Present. Please Create Device')
		return redirect('device')

	#my_filter = Device(request.GET, queryset=devices)
	# meetings = devices.qs

	context = {
        'myFilter': devices,
        'form': devices,
    }
	return render(request, '../templates/msiapp_templates/admin_folder/admin_list_customer_by_device.html', context)


@user_passes_test(is_admin, login_url="login")
@login_required(login_url="login")
def admin_list_device_by_customer(request, pk):
	user = pk
	try:
		customer = Customer.objects.get(user=user)
	# 	print(customer)
	except:
		messages.error(request, 'No Device Present. Please Add New Device')
		return redirect('device')
	device = Device.objects.filter(customers=customer)
	check = len(device)

	if check == 0:
		messages.warning(request, 'No Devices Linked To Customer. Please Add Device')
		return redirect('device')

	my_filter = DeviceFilter(request.GET, queryset=device)
	meetings = my_filter.qs
	context = {
        'myFilter': my_filter,
        'form': meetings,
    }
	return render(request, '../templates/msiapp_templates/admin_folder/admin_device_list_by_customer.html', context)


@user_passes_test(is_admin, login_url="login")
@login_required(login_url="login")
def admin_list_customer_by_device(request, pk):
	customers = []
	print(pk)
	try:
		devices = Device.objects.filter(name=pk)
		print(len(devices))
	except:
		messages.warning(request, 'No Device Present. Please Create Device')
		return redirect('device')

	#my_filter = Device(request.GET, queryset=devices)
	# meetings = devices.qs

	context = {
        'myFilter': devices,
        'form': devices,
    }
	return render(request, '../templates/msiapp_templates/admin_folder/admin_list_customer_by_device.html', context)


def update_second_db_device(device_id, user_name, my_output):
	print('Im in the device update')
	my_host = "neura.dyndns.org"
	my_user = "Quinn"
	my_password = "QuinnLondon#1"
	my_database = "neuraCore"
	my_port = 2505
	print('my list+++++===>', device_id, user_name, my_output)
	try:
		connection = mysql.connector.connect(host=my_host, user=my_user, password=my_password, database=my_database, port=my_port)
		cur = connection.cursor()
		

		try:
			returned_list = cur.callproc("DeviceUpdate", [device_id, user_name, my_output])
			if returned_list[2] == 0: 
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
			return returned_list

