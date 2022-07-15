import mysql.connector
from prettytable import PrettyTable, SINGLE_BORDER
import datetime
from time import sleep


def title(msg):
    """
    def to create the titles in the same format
    :param msg: message that goes in the title
    :return: title formatted
    """
    print('=' * 40)
    print(f'\033[0;32m{msg.center(40)}\033[m')
    print('=' * 40)


def menu(field1, field2, options):
    """
    def to create a menu
    :param field1: 1st column field
    :param field2: 2nd column field
    :param options: options in the menu
    :return: a formatted menu with 2 fields and unlimited options
    """
    menu = PrettyTable()
    menu.align = 'c'
    menu.add_column(f'     {field1}     ', [options.index(i) + 1 for i in options])
    menu.add_column(f'      {field2}      ', options)
    menu.set_style(SINGLE_BORDER)
    print(menu)


def new_client(date, name, make, color, l_plate, time_in, time_out):
    """
    signin a new/returning client
    :param date: date of the signin
    :param name: client's name
    :param make: car's make/model
    :param color: car's color
    :param l_plate: licence plate
    :param time_in: time the car signs in
    :param time_out: the car sings out
    :return: the details of a new client
    """
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='carpark',
                                             user='root',
                                             password='')
        cursor = connection.cursor()
        mySql_insert_query = """INSERT INTO clients (date, name, CarMake, color, license_plate, timeIn, timeOut) 
                                VALUES (%s, %s, %s, %s, %s, %s, %s) """

        record = (date, name, make, color, l_plate, time_in, time_out)
        cursor.execute(mySql_insert_query, record)
        connection.commit()
        print("Record inserted successfully!")

    except mysql.connector.Error as error:
        print(f"Failed to insert into MySQL table {error}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def summary(datefrom, dateto):
    """
    getter client's information based on a date range
    :param datefrom:date from where to start the search
    :param dateto:date that finishes the period of the search
    :return: information based on the date range
    """
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='carpark',
                                             user='root',
                                             password='')
        cursor = connection.cursor()
        mySql_get_data = """SELECT * FROM clients WHERE date BETWEEN %s AND %s"""
        cursor.execute(mySql_get_data, (datefrom, dateto,))
        record = cursor.fetchall()

        for field in record:
            print('Date: ', field[0])
            print('Name: ', field[1])
            print('Car Make: ', field[2])
            print('Color: ', field[3])
            print('License Plate: ', field[4])
            print('Time In: ', field[5])
            if field[5] == field[6]:
                print('Status: In\n')
            else:
                print('Time Out: ', field[6])
                print('Stayed Period: ', field[8])
                print('Amount to pay R$ ', field[9], '\n')

    except mysql.connector.Error as error:
        print(f"Failed to get record from table {error}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def summary_money_amount(datefrom, dateto):
    """
    Sums the amount of money made
    :param datefrom:datefrom:date from where to start the search
    :param dateto:date that finishes the period of the search
    :return: The sum of the amount of money made in a range period
    """
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='carpark',
                                             user='root',
                                             password='')
        cursor = connection.cursor()
        mySql_money_data = """SELECT SUM(amount) FROM clients WHERE date BETWEEN %s AND %s"""
        cursor.execute(mySql_money_data, (datefrom, dateto,))
        result = cursor.fetchone()[0]
        if result is None:
            print("Keep working. No money registered so far.")
        else:
            print(f'The amount in this date range is R$ {result}')

    except mysql.connector.Error as error:
        print(f"Failed to get record from table {error}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def summary_client_in():
    """
    Shows the clients that are still in the parkinglot
    :return: details from clients that are in the car park.
    """
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='carpark',
                                             user='root',
                                             password='')
        cursor = connection.cursor()
        mySql_money_data = """SELECT * FROM clients WHERE timeIn = timeOut"""
        cursor.execute(mySql_money_data)
        result = cursor.fetchall()
        for row in result:
            print('Date: ', row[0])
            print('Name: ', row[1])
            print('Car Make: ', row[2])
            print('Color: ', row[3])
            print('License Plate: ', row[4])
            print('Time In: ', row[5])
            if row[5] == row[6]:
                print('Status: In\n')
            else:
                print('Time Out: ', row[6])
                print('Time Period: ', row[8])
                print('Amount to pay R$ ', row[9], '\n')

    except mysql.connector.Error as error:
        print(f"Failed to get record from table {error}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def timeout(date, l_plate):
    """
    Sign out function that updates the client's status and calculates the amount to be paid
    :param date: date that the client is leaving the car park
    :param l_plate: Licence Plate details
    :return: time that the client left, status and amount to be paid
    """
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='carpark',
                                             user='root',
                                             password='')

        cursor = connection.cursor()

        # Update timeOut column
        sql_update_query = """UPDATE clients SET timeOut = %s WHERE license_plate = %s"""
        cursor.execute(sql_update_query, (date, l_plate,))
        connection.commit()

        # Set the time period stayed
        sql_time_diff_query = """UPDATE clients SET time_period = TIMEDIFF(timeOut, timeIn) WHERE license_plate = %s"""
        cursor.execute(sql_time_diff_query, (l_plate,))
        connection.commit()

        # Calculate the amount to be paid
        sql_amount_query = """UPDATE clients SET amount = TIMESTAMPDIFF(MINUTE, timeIn, timeOut) * (10 / 60) 
        WHERE license_plate = %s"""
        cursor.execute(sql_amount_query, (l_plate,))
        connection.commit()

        # Updating status on the in_out column
        sql_amount_query = """UPDATE clients SET _out = 'yes' WHERE license_plate = %s"""
        cursor.execute(sql_amount_query, (l_plate,))
        connection.commit()

        # Print time Period and amount to be paid
        cursor = connection.cursor()
        mySql_get_data = """SELECT * FROM clients WHERE license_plate = %s"""
        cursor.execute(mySql_get_data, (l_plate,))
        record = cursor.fetchall()

        for row in record:
            print('Time Period: ', row[8])
            print('Amount to pay R$', row[9], '\n')
        print('Good bye!')

    except mysql.connector.Error as error:
        print("Failed to update table record: {}".format(error))
    finally:
        if connection.is_connected():
            connection.close()


def car_out_avoid_dub(l_plate):
    """
    Function to avoid that the same car could be sign out more than once
    using the status (_out column) from the database
    :param l_plate: Car's licence plate
    :return: the status of the selected licence plate
    """
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='carpark',
                                             user='root',
                                             password='')
        cursor = connection.cursor()
        mySql_car_out_data = """SELECT _out FROM clients WHERE license_plate = %s"""
        cursor.execute(mySql_car_out_data, (l_plate,))
        result = cursor.fetchone()[0]
        return result

    except mysql.connector.Error as error:
        print(f"Failed to get record from table {error}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def l_plate_not_found(l_plate):
    """
    To check if this licence plate is in the system
    :param l_plate: car's licence plate details
    :return: if the licence plate is in the system
    """
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='carpark',
                                             user='root',
                                             password='')
        cursor = connection.cursor()
        mySql_car_out_data = """SELECT license_plate FROM clients WHERE license_plate = %s"""
        cursor.execute(mySql_car_out_data, (l_plate,))
        result = cursor.fetchone()
        return result

    except mysql.connector.Error as error:
        print(f"Failed to get record from table {error}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def readint(msg):
    """
    To ensure the user only type a number
    :param msg: user input frase
    :return: Error messages to ensure the user uses the system properly
    """
    while True:
        try:
            n = int(input(msg))
        except (ValueError, TypeError):
            print('\033[31mERROR! Please type a valid number, thanks.\033[m')
            sleep(1)
            continue
        except KeyboardInterrupt:
            print('\033[31mUser chose not to type a number.\033[m')
            sleep(1)
            return 0
        else:
            return n


def format_check(date, fmt):
    """
    Check for the date format input
    :param date: date from where to start the search
    :param fmt: date from where to stop the search
    :return: the right date format accepted in the database.
    """
    try:
        datetime.datetime.strptime(date, fmt)
    except:
        return False
    else:
        return True
