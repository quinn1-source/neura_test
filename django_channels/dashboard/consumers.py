from multiprocessing.spawn import import_main_path
import string
from tkinter import E
from unicodedata import decimal
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
import json

from numpy import true_divide
#from chat.exceptions import ClientError
#from chat.constants import *
from dashboard.models import ContactUsFile, ContactUsNotificationFile
#from account.models import Account
from dashboard.utils import LazyDashboardEncoder
# from notification.models import Notification
import pickle
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
# from django.db.models import Q
from dashboard.serializer import ContactUsNotificationFileEncoder
from django.core.serializers import serialize
# from django.contrib.postgres.search import SearchVector
from dashboard.filters import ContactUsNotificationFileFilter
from customer.models import Customer
import sqlalchemy
from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt
from .utils import get_plot, get_usage_plot
from datetime import datetime
import pickle
from dashboard.store_procedures import get_enquiry_info, get_list_nodes, customer_energy_usage_report, finding_last_reading, db_get_list_selected, quservalueselectricityimportfromutilityday
import simplejson as json
from decimal import Decimal
from django.contrib.auth.models import User
from django.db.models.query_utils import Q
import datetime
from datetime import datetime


PER_PAGE = 10
UPDATE_PER_PAGE = 3

class IndexDashboardConsumer(AsyncJsonWebsocketConsumer):

    async def disconnect(self, code):
        pass


    async def connect(self):
        """
        Called when the websocket is handshaking as part of initial connection.
        """
        print("Dash Consumer: connect: " + str(self.scope["user"]))

        # let everyone connect. But limit read/write to authenticated users
        await self.accept()

        # the room_id will define what it means to be "connected". If it is not None, then the user is connected.
        self.userName = None
 

    async def receive_json(self, content):
        my_dump = json.dumps(content)
        my_message_content = json.loads(my_dump)
        command = my_message_content['command']
        print(my_message_content)
        print('user_name==========  >  ', str(content['user_name']))

        if str(content['user_name']) == str(self.scope["user"].username):
            if command == "field_populate":
                if len(content["menu_item"].lstrip()) == 0:
                    raise ClientError('Error',"Retry Selection Please.")
                else:
                    await self.send_field_update(content["command"], content["menu_item"], content["userName"])
            
            elif command == "send":
                user_name = my_message_content['user_name']
                message = my_message_content['message']
                command = my_message_content['command']
                sent_to = my_message_content['sent_to']
                related_message_id = my_message_content['related_message_id']
                message = content.get('message')
                if self.scope["user"].is_authenticated:
                    if content.get('message') != '':
                        user_name = int(self.scope["user"].id)
                        await self.send(command, message, user_name, sent_to, related_message_id)
                        user_name = await get_account_object(user_name)
                        last_three_notifications = ''
                        unread_message_count = 0
                        page_number = 1
                        user_name = int(self.scope["user"].id)
                        user_name = await get_account_object(user_name)
                        account_object = user_name 
                        contact_us_from_user = ''
                        payload = {}
                        # my_list = await start_get_contact_us_message(account_object, page_number, contact_us_from_user, last_three_notifications, unread_message_count)
                        my_list = await start_get_contact_us_message(account_object)

                
                        await self.send_json({
                            "messages_payload": "start_get_contact_us_message",
                            'target': my_list['contact_us_target'],
                            'contact_us_from_user': my_list['contact_us_from_user'],
                            'contact_us_verb': my_list['contact_us_verb'],
                            'unread_message_count': my_list['unread_message_count'],
                        })
                        
                    else:
                        print('pass is success')
                else:
                    print('Redirect to login')
            elif command == 'start_get_contact_us_message':
                user_name = my_message_content['user_name']
                message = my_message_content['message']
                command = my_message_content['command']

                my_user_name = int(self.scope["user"].id)
                user_name = await get_account_object(my_user_name)
                
                account_object = user_name 
                contact_us_from_user = ''
                payload = {}
                # my_list = await start_get_contact_us_message(account_object, page_number, contact_us_from_user, last_three_notifications, unread_message_count)
                
                my_list = await start_get_contact_us_message(account_object)
                if my_list:
                    await self.send_json({
                        "messages_payload": "start_get_contact_us_message",
                        'target': my_list['contact_us_target'],
                        'contact_us_from_user': my_list['contact_us_from_user'],
                        'contact_us_verb': my_list['contact_us_verb'],
                        'unread_message_count': my_list['unread_message_count'],
                    })
                else:
                    await self.send_json({
                        "messages_payload": "start_get_contact_us_message",
                        'target': 'contact_us_target',
                        'contact_us_from_user': 'contact_us_from_user',
                        'contact_us_verb': 'contact_us_verb',
                        'unread_message_count': 0,
                    })
            elif command == 'start_get_node_list':
                user_name = my_message_content['user_name']
                my_concession = ''
                my_location = ''
                my_gateway = ''
                my_node = ''
                my_node_name = ''
                my_node_type = ''
                update_return = await db_get_list_nodes(user_name)
                concession = ''
                location = ''
                gateway = ''
                node = ''
                node_name = ''
                node_type = ''

                set_concession = ''
                set_location = ''
                set_gateway = ''
                set_node = ''
                set_node_name = ''
                set_node_type = ''
                if update_return:
                    
                    set_concession = update_return[0]
                    set_location = update_return[1]
                    set_gateway = update_return[2]
                    set_node = update_return[3]
                    set_node_name = update_return[4]
                    set_node_type = update_return[5]
                    my_concession = update_return[6]
                    my_location = update_return[7]
                    my_gateway = update_return[8]
                    my_node = update_return[9]
                    my_node_name = update_return[10]
                    my_node_type = update_return[11]
                    
                    #if my_concession != '':
                    concession = json.dumps(list(my_concession))
                    location = json.dumps(list(my_location))
                    gateway = json.dumps(list(my_gateway))
                    node = json.dumps(list(my_node))
                    node_name = json.dumps(list(my_node_name))
                    node_type = json.dumps(list(my_node_type))

                    set_concession = json.dumps(list(set_concession))
                    set_location = json.dumps(list(set_location))
                    set_gateway = json.dumps(list(set_gateway))
                    set_node = json.dumps(list(set_node))
                    set_node_name = json.dumps(list(set_node_name))
                    set_node_type = json.dumps(list(set_node_type))

                await self.send_json({
                        "messages_payload": "start_get_node_list_returned",
                        'concession': concession,
                        'location': location,
                        'gateway': gateway,
                        'node': node,
                        'node_name': node_name,
                        'node_type': node_type,
                        'set_concession': set_concession,
                        'set_location': set_location,
                        'set_gateway': set_gateway,
                        'set_node': set_node,
                        'set_node_name': set_node_name,
                        'set_node_type': set_node_type,
                    })

            elif command == 'get_selected_data':
                user_name = my_message_content['user_name']
                node = my_message_content['node']
                gateway = my_message_content['gateway']
                location = my_message_content['location']
                concession = my_message_content['concession']
                to_date = my_message_content['toDate']
                from_date = my_message_content['fromDate']
                update_return = []
                await db_get_list_selected(user_name, gateway, location, update_return, to_date, from_date)

                #my_concession = update_return[0]
                #my_location = update_return[1]
                #my_gateway = update_return[2]
                #my_node = update_return[3]
                #if my_concession != '':

                concession = json.dumps(list(my_concession))
                location = json.dumps(list(my_location))
                gateway = json.dumps(list(my_gateway))
                node = json.dumps(list(my_node))
                await self.send_json({
                        "messages_payload": "start_get_node_list_returned",
                        'concession': concession,
                        'location': location,
                        'gateway': gateway,
                        'node': node,
                    })


                #customer_energy_usage_report(node_name)
            elif command == 'customer_monitoring_data':
                user_name = my_message_content['user_name']
                message = my_message_content['toDate']
                command = my_message_content['command']
                from_date = my_message_content['fromDate']
                to_date = my_message_content['toDate']

                node = my_message_content['node']

                customer_monitoring_data_returned = customer_energy_usage_report(node, from_date, to_date)

                date_count = len(customer_monitoring_data_returned[0])
                value_count = len(customer_monitoring_data_returned[1])
                sum_currency_value = json.dumps(customer_monitoring_data_returned[2])
                sum_elect_value = json.dumps(customer_monitoring_data_returned[3])
                returned_date_list = json.dumps(list(customer_monitoring_data_returned[0]))
                returned_value_list = json.dumps(list(customer_monitoring_data_returned[1]), use_decimal=True)

                await self.send_json({
                    "messages_payload": "customer_monitoring_data",
                    'node': node,
                    'from_date': from_date,
                    'to_date': to_date,
                    'returned_date_list': returned_date_list,
                    'returned_value_list': returned_value_list,
                    'sum_currency_value': sum_currency_value,
                    'sum_elect_value': sum_elect_value,
                })
            
            
            elif command == 'currency_data_get':
                user_name = my_message_content['user_name']
                meter_type = my_message_content['meterType']
                frequency = my_message_content['frequency']
                command = my_message_content['command']
                from_date = my_message_content['fromDate']
                to_date = my_message_content['toDate']
                await currency_data_get(meter_type, user_name, frequency, to_date, from_date)
            
            elif command == 'get_user_profile_data':
                user_name = my_message_content['user_name']
                my_user_profile_date = await user_profile_data_get(user_name)

                my_user_profile_date = json.dumps(my_user_profile_date)
                await self.send_json({
                    "messages_payload": "returned_user_profile_data",
                    "payload": my_user_profile_date
                })
            elif command == 'get_inbox_data':
                user_name = my_message_content['user_name']
                my_inbox_data = await inbox_data_get(user_name)
                #receiver_user = my_inbox_data[0]
                #send_user = my_inbox_data[1]
                #message = my_inbox_data[2]
                #date = my_inbox_data[3]
                #read = my_inbox_data[4]
                #message_id = my_inbox_data[5]
                #date = str(date)
                my_inbox_data = json.dumps(my_inbox_data, indent=4, sort_keys=True, default=str)

                await self.send_json({
                    "messages_payload": "returned_inbox_data",
                    "payload": my_inbox_data,
                })


            elif command == 'get_inbox_read_data':
                user_name = my_message_content['user_name']
                message_id = my_message_content['message_id']
                my_inbox_data = await get_inbox_read_data(user_name, message_id)
                my_inbox_data = json.dumps(my_inbox_data, indent=4, sort_keys=True, default=str)
                receiver_user = my_inbox_data[0]
                send_user = my_inbox_data[1]
                message = my_inbox_data[2]
                date = my_inbox_data[3]
                read = my_inbox_data[4]
                message_id = my_inbox_data[5]
                await self.send_json({
                    "messages_payload": "returned_inbox_data_read",
                    "payload": my_inbox_data,
                    "receiver_user": receiver_user,
                    "send_user": send_user,
                    "message": message,
                    "date": date,
                    "message_id": message_id,
                })
            elif command == 'getEnquiryInfo':
                user_name = my_message_content['user_name']
                currency_kwh = my_message_content['currency_kwh']
                from_date = my_message_content['from_date']
                meter_value = my_message_content['meter_value']
                to_date = my_message_content['to_date']
                node_array = my_message_content['node_array']
                frequency = my_message_content['frequency']

                returned_get_enquiry_info = await db_get_enquiry_info(user_name, node_array, currency_kwh, meter_value, from_date, to_date, frequency)
                sum_currency_value = json.dumps(returned_get_enquiry_info[2])
                sum_elect_value = json.dumps(returned_get_enquiry_info[3])
                returned_date_list = json.dumps(list(returned_get_enquiry_info[1]))
                returned_value_list = json.dumps(list(returned_get_enquiry_info[0]), use_decimal=True)
                await self.send_json({
                    "messages_payload": "returned_enquiry_info",
                    #'node': node,
                    'from_date': from_date,
                    'to_date': to_date,
                    'returned_date_list': returned_date_list,
                    'returned_value_list': returned_value_list,
                    'sum_currency_value': sum_currency_value,
                    'sum_elect_value': sum_elect_value,
                })

            else:
                print('error in command get data')
            
        else:
            print('slice')

    async def send(self, command, message, user_name, sent_to, related_message_id):
        sent_to = sent_to
        related_message_id = related_message_id
        if int(user_name) == int(self.scope["user"].id):
            if command == 'send':
                my_message = message
               # await update_contact_us_message(command, message, self.scope["user"].id,  sent_to, related_message_id)
                await contact_us_notification_file_update(message, self.scope["user"].id, sent_to, related_message_id)

                
@database_sync_to_async
def db_get_list_nodes(user_name):
    try:
        get_list_nodes_return = get_list_nodes(user_name)
    except:
        get_list_nodes_return = ''
    return get_list_nodes_return


@database_sync_to_async
def db_get_list_selected(user_name, gateway, location, update_return, to_date, from_date):
    get_list_selected = db_get_list_selected(user_name, gateway, location, update_return, to_date, from_date)
    return get_list_selected

@database_sync_to_async
def contact_us_store_procedure(node_name, reading_type):
    store_procedure_return = finding_last_reading(node_name, reading_type)


@database_sync_to_async
def db_get_enquiry_info(user_name, node_array, currency_kwh, meter_value, from_date, to_date, frequency):

    return_get_enquiry_info = get_enquiry_info(user_name, node_array, currency_kwh, meter_value, from_date, to_date, frequency)
    return return_get_enquiry_info


@database_sync_to_async
def currency_data_get(meter_type, user_name, frequency, to_date, from_date):
   currency_data_get = quservalueselectricityimportfromutilityday(meter_type, user_name, frequency, to_date, from_date)


@database_sync_to_async
def get_account_object(user_name):
    return User.objects.get(id=user_name)

@database_sync_to_async
def update_contact_us_message(command, message, user_name, sent_to, related_message_id):
    user_name = User.objects.get(id=user_name)
    #if related_message_id == '' or related_message_id == 'Null' or related_message_id == 'undefined': 
    return ContactUsFile.objects.create(contact_us_message=message, user_name=user_name)
    #else:
    #   record = ContactUsFile.objects.get(id=related_message_id)
    #    record.read_time = datetime.today
    #    record.read_unread = True


@database_sync_to_async
def contact_us_notification_file_update(message, user_name, sent_to, related_message_id):
    user_name = User.objects.get(id=user_name)
    helpdesk_user = User.objects.get(username='helpdesk')
    sent_to = User.objects.get(username=sent_to)
   ## check this out...... if user_name == user_name = User.objects.get(id=user_name)

    if user_name.username != 'helpdesk':
        ContactUsNotificationFile.objects.create(contact_us_target=helpdesk_user, contact_us_from_user=user_name, contact_us_verb=message)
    else:
        ContactUsNotificationFile.objects.create(contact_us_target=sent_to, contact_us_from_user=helpdesk_user, contact_us_verb=message)
    if related_message_id:
        record = ContactUsNotificationFile.objects.get(id=related_message_id)
        record.read_time = datetime.today()
        record.contact_us_read = True
        record.save()

    return 


@database_sync_to_async
def user_profile_data_get(user_name):
    user = User.objects.get(username=user_name)
    cus = Customer.objects.get(user=user.id)
    name_1 = cus.name_1
    name_2 = cus.name_1
    address_line_1 = cus.address_line_1
    address_line_2 = cus.address_line_2
    city = cus.city
    province = cus.province
    postal_code = cus.postal_code
    country = cus.country
    gender = cus.gender
    contact_number = cus.contact_number
    email = cus.email
    id_number = cus.id_number
    terms = cus.terms

    return name_1, name_2, contact_number, email, address_line_1, address_line_2, city, province, postal_code, country, gender, contact_number, email, id_number, terms 


@database_sync_to_async
def inbox_data_get(user_name):
    user = User.objects.get(username=user_name)
    print('user===========>', user.username)
    if user_name == user.username:
        inbox_list = ContactUsNotificationFile.objects.order_by('-contact_us_timestamp').filter(Q(contact_us_from_user=user)|Q(contact_us_target=user))
        #inbox_list = ContactUsNotificationFile.objects.order_by('-contact_us_timestamp').filter(Q(contact_us_target=user))
        received_user = []
        sent_user = []
        message = []
        date = []
        read = []
        message_id = []
        for data in inbox_list:
            received_user.append(data.contact_us_target.username)
            sent_user.append(data.contact_us_from_user.username)
            message.append(data.contact_us_verb)
            date.append(data.contact_us_timestamp)
            message_id.append(data.id)
            #print(date)
            #for my_date in date:
                #my_date = str(my_date)
                #oldest_ts = datetime.datetime.strptime(my_date, "%YYYY %MM %d  %H:%M:%S.%f")
                #print(oldest_ts)
            read.append(data.contact_us_read)
    return received_user, sent_user, message, date, read, message_id


@database_sync_to_async
def get_inbox_read_data(user_name, message_id):
    user = User.objects.get(username=user_name)
    if user_name == user.username:
        data = ContactUsNotificationFile.objects.get(id=message_id)
        
        #inbox_list = ContactUsNotificationFile.objects.order_by('-contact_us_timestamp').filter(Q(contact_us_target=user))
        received_user = data.contact_us_target.username
        sent_user = data.contact_us_from_user.username
        message = data.contact_us_verb
        date = data.contact_us_timestamp
        read = data.contact_us_read
        message_id = data.id
        
        if user_name != sent_user:
            data.contact_us_read = True
            data.read_time = datetime.today()
            data.save()

    return received_user, sent_user, message, date, read, message_id


@database_sync_to_async
# def start_get_contact_us_message(account_object, page_number, contact_us_from_user, last_three_notifications, unread_message_count, **kwargs):
def start_get_contact_us_message(account_object):
    page_number = 1
    my_dict = {}
    print('account_object', account_object.id)

    #my_unread_message_count = ContactUsNotificationFile.objects.filter(contact_us_from_user=account_object, contact_us_read=False)
    # unread_message_count = len(my_unread_message_count)
    # my_unread_message_count = ContactUsNotificationFile.objects.order_by('-contact_us_timestamp').filter(Q(contact_us_from_user=account_object)|Q(contact_us_target=account_object))
    my_unread_message_count = ContactUsNotificationFile.objects.order_by('-contact_us_timestamp').filter(Q(contact_us_target=account_object))

    unread_message_count = 0
    contact_us_list = ContactUsNotificationFile.objects.filter(contact_us_from_user=account_object).order_by('-contact_us_timestamp') | ContactUsNotificationFile.objects.filter(contact_us_target=account_object).order_by('-contact_us_timestamp') 

    for item in my_unread_message_count:
        if item.contact_us_read == False:
            unread_message_count += 1

    new_page_number = int(page_number) 
    for ob in contact_us_list:
        my_dict['contact_us_target'] = str(ob.contact_us_target.username)
        my_dict['contact_us_from_user'] = str(ob.contact_us_from_user.username)
        my_dict['contact_us_verb'] = str(ob.contact_us_verb)
        my_dict['contact_us_timestamp'] = ob.contact_us_timestamp

        #my_dict['contact_us_timestamp'] = json.dumps(ob.contact_us_timestamp)
        
        my_dict['unread_message_count'] = unread_message_count

    return my_dict
      
