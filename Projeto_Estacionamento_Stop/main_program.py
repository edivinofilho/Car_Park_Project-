"""
Car Park Project
It can be used to any size car park (updating the spots variable),
keeping a list of clients connected to a database(MySQL).
"""
import datetime
import emojis
from time import sleep
import project_functions

# Car Park storage capacity
spots = 10
# Date variables to insert automatically the time of the client's arrival and departure in the MySQL format
today = datetime.datetime.now()
date_time = today.strftime("%Y/%m/%d, %H:%M:%S")
today_date = today.strftime("%Y/%m/%d")
timeIn = timeOut = date = date_time
entry_date = today_date
# Welcoming Menu
project_functions.title(emojis.encode(':car: Welcome to the Car Park GoodStop :car:'))
print('Please press 0 for MAIN MENU or 9 to EXIT')
sleep(1)
while True:
    option_welcome = project_functions.readint('Your Option: ')
    sleep(1)
    if option_welcome != 0 and option_welcome != 9:
        print('\033[31mInvalid Option. Please try again\033[m')
        sleep(1)
    elif option_welcome == 0:
        while True:
            if option_welcome == 0:
                # Main Menu
                project_functions.title('MAIN MENU')
                project_functions.menu('CODE', 'OPTIONS', ['Car In', 'Summary', 'Car Out', 'EXIT'])
                # Condition used if the Car Park is full
                if spots == 0:
                    print('\033[35mNOW we have NO places left!\033[m')
                option = project_functions.readint('Type your option here: ')
                sleep(1)
                # Error handling
                if option not in [1, 2, 3, 4]:
                    print('\033[31mInvalid Option. Please try again\033[m')
                    sleep(1)
                elif spots == 0 and option == 1:
                    print('\033[31mOption Unavailable!\033[m \033[35mWe have No spots left!\033[m')
                    sleep(1)
                # Main Menu Options
                # Option 1 → Signing in a client
                elif option == 1:
                    project_functions.title('SIGNING IN')
                    cl_name = input('Name: ').title()
                    car_make = input('Car Make/Model: ').title()
                    car_color = input('Color: ').upper()
                    lic_plate = input('License Plate: ').upper().strip()
                    project_functions.new_client(today_date, cl_name, car_make, car_color,
                                                 lic_plate, timeIn, timeOut)
                    spots -= 1
                    sleep(1)
                # Option 2 → Access the summary options
                elif option == 2:
                    while True:
                        # Submenu from the summary option
                        project_functions.title('       \033[34mSUMMARY MENU\033[m')
                        project_functions.menu('CODE', 'OPTIONS', ["Client's List", '$',
                                                                   "Clients In Now", 'Available Spots'])
                        summary_option = project_functions.readint('Option [Press 0 For Main Menu]: ')
                        sleep(1)
                        # Summary menu's option with error handling
                        if summary_option not in [0, 1, 2, 3, 4]:
                            print('\033[31mInvalid Option. Please try again\033[m')
                        # Option 1 from the summary menu → Returns a client list based on a date range
                        elif summary_option == 1:
                            fromdate = input('From [YYYY-MM-DD]: ')
                            while True:
                                if not project_functions.format_check(fromdate, '%Y-%m-%d') and not \
                                        project_functions.format_check(fromdate, '%Y%m%d'):
                                    print("\033[31mSorry, wrong format, try again!\033[m")
                                    fromdate = input('From [YYYY-MM-DD]: ')
                                else:
                                    break
                            todate = input('To [YYYY-MM-DD]: ')
                            while True:
                                if not project_functions.format_check(todate, '%Y-%m-%d') and not \
                                        project_functions.format_check(todate, '%Y%m%d'):
                                    print("\033[31mSorry, wrong format, try again!\033[m")
                                    todate = input('To [YYYY-MM-DD]: ')
                                else:
                                    break
                            project_functions.title('CLIENTS LIST')
                            sleep(1)
                            project_functions.summary(fromdate, todate)
                        # Option 2 from the summary menu → Returns the amount of money based on a date range
                        elif summary_option == 2:
                            fromdate = input('From [YYYY-MM-DD]: ')
                            while True:
                                if not project_functions.format_check(fromdate, '%Y-%m-%d') and not \
                                        project_functions.format_check(fromdate, '%Y%m%d'):
                                    print("\033[31mSorry, wrong format, try again!\033[m")
                                    fromdate = input('From [YYYY-MM-DD]: ')
                                else:
                                    break
                            todate = input('To [YYYY-MM-DD]: ')
                            while True:
                                if not project_functions.format_check(todate, '%Y-%m-%d') and not \
                                        project_functions.format_check(todate, '%Y%m%d'):
                                    print("\033[31mSorry, wrong format, try again!\033[m")
                                    todate = input('To [YYYY-MM-DD]: ')
                                else:
                                    break
                            project_functions.summary_money_amount(fromdate, todate)
                        # Option 3 from the summary menu → Returns the details of clients that are in the car park now
                        elif summary_option == 3:
                            project_functions.title('CLIENTS IN THE CAR PARK NOW')
                            sleep(1)
                            project_functions.summary_client_in()
                        # Option 4 from the summary menu → Returns the number of available spots
                        elif summary_option == 4:
                            print(f'We have {spots} spot(s) available now.')
                            sleep(1)
                        elif summary_option == 0:
                            print('Exiting Summary Menu...')
                            sleep(1)
                            break
                # Option 3 → Signs the client out and calculates the amount to be paid
                elif option == 3:
                    project_functions.title('SIGNING OUT')
                    car_lc_plate = input('License Plate: ').upper()
                    if project_functions.l_plate_not_found(car_lc_plate) is None:
                        print('Sorry, License Plate not in the system. \n'
                              'Please check the client list in summary.')
                    elif project_functions.car_out_avoid_dub(car_lc_plate) == 'yes':
                        print('The car with this license plate already left!')
                    else:
                        project_functions.timeout(date, car_lc_plate)
                        spots += 1
                    sleep(1.5)
                # Option 4 → Exits the program
                elif option == 4:
                    project_functions.title('PROGRAM CLOSING...')
                    sleep(1)
                    print(emojis.encode('Hasta la vista baby :sunglasses:'))
                    break
        break
    # Exits welcoming menu
    elif option_welcome == 9:
        print('Program Closed!')
        break
