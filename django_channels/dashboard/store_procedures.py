import mysql.connector
from mysql.connector import Error
import json
import sqlalchemy
from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt
from .utils import get_plot, get_usage_plot
import datetime

host = "neura.dyndns.org"
user = "Quinn"
password = "Holland$1"
database = "NeuraData"


def finding_last_reading(node_id, reading_type):
    node_id = int(node_id)
    reading_type = int(reading_type)
    my_node_id = json.loads(node_id)
    my_reading_type = json.loads(reading_type)
    my_host = json.loads(host)
    my_user = json.loads(user)
    my_password = json.loads(password)
    my_database = json.loads(database)


    try:
        connection = mysql.connector.connect(host=my_host, user=my_user, password=my_password, database=my_database)
        cursor = connection.cursor()
        cursor.callproc("FindLastReading", [node_id, reading_type,])
        for result in cursor.stored_results():
            rlist = result.fetchall()
            print(rlist)
    except  Error as e:
        print('why')
        print("Error occured ", e)

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("connection is closed")
    df1 = pd.DataFrame(rlist)


def customer_energy_usage_report(node_id, from_date, to_date):
    start_date = ''
    end_date = ''
    #my_node_id = int(node_id)
    if from_date:
        try:
            start_date = datetime.datetime.strptime(from_date, "%d/%m/%Y").strftime("%Y-%m-%d")
        except:
            start_date = from_date

    if to_date:
        try:
            end_date = datetime.datetime.strptime(to_date, "%d/%m/%Y").strftime("%Y-%m-%d")
        except:
            end_date = to_date

    # reading_type = int(reading_type)
    #my_node_id = json.loads(node_id)
    #my_reading_type = json.loads(reading_type)
    #my_host = "localhost"
    #my_user = "root"
    #my_password = "password"
    #my_database = "NeuraData"
    my_host = "neura.dyndns.org"
    my_user = "Quinn"
    my_password = "QuinnLondon#1"
    my_database = "neuraData"
    my_port = 2505
    #my_host = json.(host)
    #my_user = json.user)
    #my_password = json.(password)
    #my_database = json........(database)
    #reading_type = 1
    #my_node_id = 11
    
    try:
        connection = mysql.connector.connect(host=my_host, user=my_user, password=my_password, database=my_database, port=my_port)
        _userRef = '12345Neilson'
        cur = connection.cursor()
        # cur.callproc("FindLastReading", [my_node_id, reading_type,])
        #cur.callproc("squservalueselectricityimportfromutilityday", [_userRef,])
        cur.callproc("squservaluesimportfromutilityday", [_userRef, start_date, end_date])
        
        for result in cur.stored_results():
            
            rlist = result.fetchall()
        
    except  Error as e:
        print('why')
        print("Error occured ", e)

    finally:
        if (connection.is_connected()):
            cur.close()
            connection.close()
            print("connection is closed")
    
    df1 = pd.DataFrame(rlist)
    node_period = df1
    if start_date == '' and end_date != '':

        # Change date for MySQL
        if end_date:
            end_date = end_date.replace('-','/')
        new_period = node_period[(node_period[5] <= end_date)]
        
    elif start_date != '' and end_date != '':
        # Change date for MySQL
        if start_date:
            start_date = start_date.replace('-','/')
        # Change date for MySQL
        if end_date:
            end_date = end_date.replace('-','/')
        new_period = node_period[(node_period[5] >= start_date) & (node_period[5] <= end_date)]
    elif end_date == '' and start_date != '':
        # Change date for MySQL
        start_date = start_date.replace('-','/')
        new_period = node_period[(node_period[5] >= start_date)]
    else:
        
        new_period = node_period
    # To display dataframe
    table_content = new_period.to_html()
    df = pd.DataFrame(new_period, columns=[5,8,7])
    currency_value = df[7]
    elect_value = df[8]

    sum_currency_value = currency_value.sum()
    sum_elect_value = elect_value.sum()

    # data['total'] = data['age'].sum()
    x = []
    y = []

    for column in df:
        columnSeriesObj = df[column]
        if column == 5:
            x = columnSeriesObj.values
        elif column == 7:
            y = columnSeriesObj.values
    return x, y, sum_currency_value, sum_elect_value


def get_list_nodes(user_name):
        #my_host = "localhost"
    #my_user = "root"
    #my_password = "password"
    #my_database = "NeuraData"
    my_host = "neura.dyndns.org"
    my_user = "Quinn"
    my_password = "QuinnLondon#1"
    my_database = "neuraCore"
    my_port = 2505
    try:
        connection = mysql.connector.connect(host=my_host, user=my_user, password=my_password, database=my_database, port=my_port)

        _userRef = user_name
        cur = connection.cursor()
        # cur.callproc("FindLastReading", [my_node_id, reading_type,])
        #cur.callproc("squservalueselectricityimportfromutilityday", [_userRef,])
        cur.callproc("squserselectnodes", [_userRef,])
        try:
            for result in cur.stored_results():
                print('result', result)
                rlist = result.fetchall()
                print(rlist)
        except:
            rlist = []
    except  Error as e:
        print('why')
        print("Error occured ", e)

    finally:
        if (connection.is_connected()):
            connection.close()
            print("connection is closed")

    df = pd.DataFrame(rlist)
    concession = df[0]
    location = df[1]
    gateway = df[2]
    nodes = df[3] 
    node_name = df[4]
    node_type = df[5]

    set_concession = set(concession)
    set_location = set(location)
    set_gateway = set(gateway)
    set_nodes = set(nodes)
    set_node_name = set(node_name) 
    set_node_type = set(node_type)
    return set_concession, set_location, set_gateway, set_nodes, set_node_name, set_node_type, concession, location, gateway, nodes, node_name, node_type
    


def quservalueselectricityimportfromutilityday(meter_type, user_name, frequency, to_date, from_date):
    #my_host = "localhost"
    #my_user = "root"
    #my_password = "password"
    #my_database = "NeuraData"
    my_host = "neura.dyndns.org"
    my_user = "Quinn"
    my_password = "QuinnLondon#1"
    my_database = "neuraData"
    my_port = 3306
    node = (17, 51)
    print('okay step 4')
    try:
        connection = mysql.connector.connect(host=my_host, user=my_user, password=my_password, database=my_database, port=my_port)
        query = ''
        #query = f"Select * from squValuesImportFromUtilityDay WHERE userRef in ('{user_name}') and node in {node};"
       # Select * from quservalueselectricityimportfromutilityday WHERE userRef in ('5678DuToit', '1234Piper') and node in (17, 51, 71);
        print(query)
        try:
            result_dataFrame = pd.read_sql(query, connection)
            concession = result_dataFrame[0]
            print(result_dataFrame)
        except:
            print('a')
        
        
    except  Error as e:
        print('why')
        print("Error occured ", e)

    finally:
        if (connection.is_connected()):
            connection.close()
            print("connection is closed")

    return


def db_get_list_selected(user_name, gateway, location, update_return, to_date, from_date):
    print('almost___________+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')


def get_enquiry_info(user_name, node_array, currency_kwh, meter_value, from_date, to_date, frequency):
    print(from_date)
    print(to_date)
    print('currency_kwh', currency_kwh)
    my_host = "neura.dyndns.org"
    my_user = "Quinn"
    my_password = "QuinnLondon#1"
    my_database = "neuraData"
    my_port = 3306
    node_list = ''
    print('currency_kwh', currency_kwh)
    for node in node_array:
        node_list += node+','

    try:
        connection = mysql.connector.connect(host=my_host, user=my_user, password=my_password, database=my_database, port=my_port)
        cur = connection.cursor()
        if frequency == 'daily':
            cur.callproc("squValuesImportFromUtilityDay", [node_list, from_date, to_date])
        elif frequency == 'weekly':
            cur.callproc("squValuesImportFromUtilityWeek", [node_list, from_date, to_date])
        elif frequency == 'monthly':
            cur.callproc("squvaluesimportfromutilitymonth", [node_list, from_date, to_date])

        try:
            for result in cur.stored_results():
                rlist = result.fetchall()
        except:
            rlist = []
    except  Error as e:
        print('why')
        print("Error occured ", e)

    finally:
        if (connection.is_connected()):
            connection.close()
            print("connection is closed")
    if frequency == 'daily':
        dataframe = pd.DataFrame(rlist, columns = ['Cost', 'Usage','Node', 'CustomerOid', 'ContactFirstName', 'ContactLastName', 'NodeName', 'NodeType', 'DateOnly', 'MonthOnly'])
    else:
         dataframe = pd.DataFrame(rlist, columns = ['Cost', 'Usage','Node', 'CustomerOid', 'ContactFirstName', 'ContactLastName', 'NodeName', 'NodeType', 'DateOnly'])
    print(meter_value)
    if meter_value == 0:
        rslt_df = dataframe[dataframe['NodeType'] == 0]
        print('0 is electricity',len(rslt_df.index))
    elif meter_value == 1:
        rslt_df = dataframe[dataframe['NodeType'] == 1]
        print('0 is water',len(rslt_df.index))
    else:
        rslt_df = dataframe
        print('0 is all',len(rslt_df.index))
    
    currency_value = rslt_df['Cost']
    elect_value = rslt_df['Usage']


    sum_currency_value = currency_value.sum()
    sum_elect_value = elect_value.sum()
 
    if currency_kwh == 'currency':
        for column in rslt_df[['Cost','DateOnly']]:
            print(column)
            columnSeriesObj = rslt_df[column]
            if column == 'Cost':
                x = columnSeriesObj.values
            elif column == 'DateOnly':
                y = columnSeriesObj.values 
    if currency_kwh == 'output':
        for column in rslt_df[['Usage', 'DateOnly']]:
            columnSeriesObj = rslt_df[column]
            if column == 'Usage':
                x = columnSeriesObj.values
            elif column == 'DateOnly':
                y = columnSeriesObj.values

    return x, y, sum_currency_value, sum_elect_value


    