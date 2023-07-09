import mysql.connector
import functools
import random
from datetime import date  

cnx = mysql.connector.connect(user = 'root', password = 'password',
                              host = 'localhost', database = 'testschema')
cursor = cnx.cursor(buffered=True)

#python -m tem

#Trigger to set the Pending charges to 0 after the customer has reached their destination or have cancelled the trip altogether
trigger_1 = ("""create trigger fareupdate 
            after update on bookings for each row
            begin
                update Customer set Customer.Pending_charges = 0 where customer_id = old.booking_id and new.status = "Completed";
            end$$""")

#Trigger to set the state of the driver to "Free" if the trip is completed or cancelled
trigger_2 = ("""create trigger driverAvailable
            after update on bookings for each row
            begin
                update Driver set Driver.CurrentState = 1 where Driver.driver_id = old.driver_id and new.status ="Completed" or new.status = "Canceled";
            end$$""")

#Trigger to set the state of the driver to "Occupied" if any trip is started
trigger_3 = ("""create trigger driverAvailable
            after update on bookings for each row
            begin
                update Driver set Driver.CurrentState = 0 where Driver.driver_id = old.driver_id and new.status ="Completed" or new.status = "Cancelled";
            end$$""")



# print()
# print()
# for i in range(1, 15):
#     if(i!=8):
#         print("|                                                                           |")
#     else:
#         print("|                    Welcome to the Cab Booking System                      |")
print(" ")
print(" ")
print(' ')
print("----------------------------------------xxxxxxxxxxxxxxxxxxxxxxxxxxxx----------------------------------------")
print(" ")
print("                                      Welcome to the Cab Booking System                                      ")
print(" ")


print()
print("You can currently perform three functions...")
print("1. Login")
print("2. Sign Up")
print("")
lg_Sn = int(input("Please enter the your choice here : "))
print(' ')
if(lg_Sn == 1):
    print("--------------------------xxxxxxxxxxxx-----------------------------")
    print(" ")
    print("You have selected to login into an existing account")
    print("The roles that you can login as are as follows...")
    print("1. Customer")
    print("2. Driver")
    print("3. Admin")
    print()
    Lg_Usr = int(input("Please enter your role here : "))

    if(Lg_Usr == 1):
        print(" ")
        print("--------------------------xxxxxxxxxxxx-----------------------------")
        print("You have decided to login as a Customer")
        name = str(input("Please enter your name : "))
        cus_pass = str(input("Please enter your password here : "))

        pick_cus_id = None
        query_fetch = "SELECT * FROM Customer WHERE Customer_Name = %s AND password = %s"
        cursor.execute(query_fetch, (name, cus_pass))
        row = cursor.fetchone()
        if row:
            pick_cus_id = row[0]
        if row is None:
            print(" ")
            print(' ')
            print("Username or Password incorrect!")
            print(" ")
            print("Please enter the correct credentials and try again")
            print(" ")
            print("--------------------------xxxxxxxxxxxx-----------------------------")
            print(" ")
        else:
            print(" ")
            print("Welcome customer '" + name + "' to the Cab Booking System!")
            print("--------------------------xxxxxxxxxxxx-----------------------------")
            print(" ")
            print("As a customer the various actions that you can perform are...")
            print("1. View all the locations")
            print("2. Book a cab")
            print("3. Cancel your ongoing trip")
            print(" ")
            usr_ip = int(input("Please enter what you wish to do : "))

            if(usr_ip == 1):
                print(" ")
                print("You wish to see all the locations that you can visit")
                print(" ")
                print("--------------------------xxxxxxxxxxxx-----------------------------")
                query = ("SELECT location_name FROM location_data")
                cursor.execute(query)
                for each in cursor:
                    print(each[0])
                print("--------------------------xxxxxxxxxxxx-----------------------------")
                print(" ")
            
            if(usr_ip == 2):
                print(" ")
                print("--------------------------xxxxxxxxxxxx-----------------------------")
                print("You have wished to book a cab!")
                use_yn = str(input("Do you wish to see the locations that can be booked?"))
                if(use_yn == "Y" or use_yn == "y"):
                    print(" ")
                    print("You wish to see all the locations that you can visit")
                    print(" ")
                    print("--------------------------xxxxxxxxxxxx-----------------------------")
                    query = ("SELECT location_name FROM location_data")
                    cursor.execute(query)
                    for each in cursor:
                        print(each[0])
                    print("--------------------------xxxxxxxxxxxx-----------------------------")
                    print(" ")
                else:
                    print(" ")
                    print("You have wished to not see the loactions that can be booked")
                print("Please enter the details...")
                name = str(input("Please enter your name : "))
                # query_fetch = ("""Select * from Customer where Customer.Customer_Name = '" + name + "' and Customer.password = '" + cus_pass + "';""")
                # cursor.execute(query_fetch)
                # for each in cursor:
                #     name = each[2]
                #     pick_up_id = each[0]

                dest_id = None
                destination = str(input("Please enter the destination  : "))
                q_dest = ("select location_data.location_id from location_data where location_name = '" + destination + "';")
                cursor.execute(q_dest)
                c_dest = cursor.fetchone()
                if c_dest:
                    dest_id = c_dest[0]

                payement = str(input("Please enter the payement method : "))
                date = str(input("Please enter the pickup date (yyyy-mm-dd) : "))
                # pick_book_id = pick_up_id
                fare = random.randint(20, 300)
                status = "Active"
                
                free_drv_id = None
                free_drv = ("select * from Driver where Driver.CurrentState = true order by Driver.CurrentState limit 1;")
                cursor.execute(free_drv)
                each_drv = cursor.fetchone()
                if each_drv:
                    free_drv_id = each_drv[1]

                cursor.execute("select * from bookings")
                last_entry = list(cursor)[-1]
                last_id = list(last_entry)[0]
                bkg_id = last_id + 1

                cursor.execute("INSERT INTO bookings VALUES (" + str(bkg_id) + ", '" + str(pick_cus_id) + "', '" + str(free_drv_id) + "', '" + str(pick_cus_id) + "', " + str(dest_id) + ", '" + str(date) + "', '"+ str(fare) + "', '"+ payement + "', '" + str(status) + "', NULL, '" + str(0) + "');")
                
                query_set = ("UPDATE Driver SET CurrentState = 0 WHERE driver_id = '" + str(free_drv_id) + "';")
                cursor.execute(query_set)

                query_cus = ("Update Customer SET Pending_charges = '"+ str(fare) + "' WHERE customer_id = '" + str(pick_cus_id) + "';")
                cursor.execute(query_cus)
                
                cnx.commit()

                print(" ")
                print("You have successfully booked your trip!")
                print(" ")
                print("--------------------------xxxxxxxxxxxx-----------------------------")
                print(" ")
            
            if(usr_ip == 3):
                print(" ")
                print("--------------------------xxxxxxxxxxxx-----------------------------")
                print("You have wished to to end your ongoing trip!")
                print(" ")

                td = date.today()

                dest = str(input("Have you reached you destination : "))
                if(dest == 'y' or dest == 'Y'):
                    print("You have reached your destination")
                    print(" ")
                    print("The trip will be finished!")
                    rate = int(input("Please rate the trip according to your experience : "))
                    query_comp = ("Update bookings SET status = 'Completed', rating = '" + str(rate) + "' where customer_id = '" + str(pick_cus_id) + "'; ")
                    cursor.execute(query_comp)
                    print(" ")
                    print("Thankyou for using our service!")
                    print(" ")
                    print("--------------------------xxxxxxxxxxxx-----------------------------")
                    print(" ")

                if(dest == 'n' or dest == "N"):
                    print("You are not at your destination")
                    finCan = str(input("Do you wish to cancel your trip? "))
                    if(finCan == "y" or finCan == "Y"):
                        print("You have deciced to cancel your trip!")
                        print(" ")
                        rate = int(input("Please rate the trip according to your experience : "))
                        query_comp = ("Update bookings SET status = 'Cancelled', rating = '" + str(rate) + "', cancel_time = '" + str(td) + "' where customer_id = '" + str(pick_cus_id) + "'; ")
                        print("We hope you have a better experience next time")
                        print(" ")
                        print("--------------------------xxxxxxxxxxxx-----------------------------")
                        print(" ")  
                    if(finCan == 'n' or finCan == "N"):
                        print("You have decided to not cancel your trip!")
                        print("--------------------------xxxxxxxxxxxx-----------------------------")
                        print(" ")


    if(Lg_Usr == 2):
        print(" ")
        print("--------------------------xxxxxxxxxxxx-----------------------------")
        print("You have decided to login as a Driver")
        name = str(input("Please enter your name : "))
        drv_pass = str(input("Please enter your password here : "))

        query_fetch = ("Select * from Driver where Driver_Name = %s and Password = %s;")
        cursor.execute(query_fetch, (name, drv_pass))
        row = cursor.fetchone()

        if row is None:
            print(" ")
            print(' ')
            print("Username or Password incorrect!")
            print(" ")
            print("Please enter the correct credentials and try again")
            print(" ")
            print("--------------------------xxxxxxxxxxxx-----------------------------")
            print(" ")
        else:

            drv_nid = None
            drv_curr = None
            query_fetch = ("Select * from Driver where Driver_Name = %s and password = %s;")
            cursor.execute(query_fetch, (name, drv_pass))
            row = cursor.fetchone()
            if row:
                drv_nid = row[1]
                drv_curr = row[0]

            drv_bkg_loc = None
            drv_pkp_loc = None
            query = ("Select * from bookings where driver_id = '"+ str(drv_nid) + "';")
            cursor.execute(query)
            row = cursor.fetchone()
            if row:
                drv_bkg_loc = row[4]
                drv_pkp_loc = row[3]
            
            loc = None
            pkp = None
            qry_loc = ("Select * from location_data where location_id = '" + str(drv_bkg_loc) + "'; ")
            cursor.execute(qry_loc)
            row = cursor.fetchone()
            if row:
                loc = row[1]

            qry_loc = ("Select * from location_data where location_id = '" + str(drv_pkp_loc) + "'; ")
            cursor.execute(qry_loc)
            row = cursor.fetchone()
            if row:
                pkp = row[1]


            print(" ")
            print("--------------------------xxxxxxxxxxxx-----------------------------")
            print(" ")
            print("Welcome Driver '" + name + "' to the Cab Booking System!")
            print("You can perform the following tasks...")
            print("1. You can check your current status")
            print("2. You can check all the locations")
            print("3. You can check the total money earned from all the trips")
            print("4. You can see the details of the bookings completed by you")
            drv_ipt = int(input("Please enter your choice : "))
            if(drv_ipt == 1):
                print(" ")
                print("You have decided to check your current status")
                if(drv_curr == 1):
                    print("You are currently free!")
                    print("Please wait you will be assigned a ride in due time!")
                    print("")
                if(drv_curr == 0):
                    print("You are currently booked!")
                    loc_chk = str(input("Do you want to check the location? "))
                    if(loc_chk == "Y" or loc_chk == "y"):
                        print(" ")
                        print("You have decided to check the locations")
                        print(" ")
                        print("The customer pickup location is : '" + pkp + "'")
                        print("The customer dropoff location is : '"+ loc +"'")
                        print(" ")
            if(drv_ipt == 2):
                print(" ")
                print("You have decided to check all the availabe locations!")
                print(" ")
                query = ("SELECT location_name FROM location_data")
                cursor.execute(query)
                for each in cursor:
                    print(each[0])
            if(drv_ipt == 3):
                print(" ")
                print("You have decided to check the total money earned by you from all the completed trips")
                print(" ")

                query = "Select SUM(fare) from bookings where driver_id = %s;"
                cursor.execute(query, (drv_nid,))
                for each in cursor:
                    print("The total money earned by you is Rs."+ str(each[0]) +"")
                print(" ")

            if(drv_ipt == 4):
                print(" ")
                print("You have decided to view all the bookings that you have completed")
                print(' ')
                query = "SELECT * FROM bookings WHERE driver_id = %s AND status = 'Completed';"
                cursor.fetchone()
                cursor.execute(query, (drv_nid,))
                for each in cursor:
                    print("Booking ID : " + str(each[0]))
                    print("Driver ID : " + str(each[2]))
                    print("Pickup Time : " + str(each[5]))
                    print("Payement Method : " + each[7])
                    print("Fare : " + str(each[6]))
                    print("Rating : " + str(each[10]))
                    print(" ")


            print("--------------------------xxxxxxxxxxxx-----------------------------")
            print(" ")

    if(Lg_Usr == 3):
        print(" ")
        print("--------------------------xxxxxxxxxxxx-----------------------------")
        print("You have decided to login as an Admin")
        print(" ")
        Admin_ID = int(input("Please enter the id of the admin : "))
        query_Name = ("Select Admin.Admin_Name from Admin where Admin.Admin_ID = '" +str(Admin_ID) + "'  ;")
        cursor.execute(query_Name)
        for each in cursor:
            print("Welcome Mr. " + each[0] + " to the Cab Booking System as an admin")
        print()
        print("As the admin you can perform various tasks")
        print("1. Update the location data")
        print("2. Remove an existing Customer/Driver")
        print("3. Run other queries on the database")
        print(" ")
        Adm_qry = int(input("Please enter the task that you wish to perform : "))
        
        if(Adm_qry == 1):
            print(" ")
            print("--------------------------xxxxxxxxxxxx-----------------------------")
            print("You have wished to update the location data")
            print(" ")

            cursor.execute("select * from location_data")
            last_entry = list(cursor)[-1]
            last_id = list(last_entry)[0]
            loc_id = last_id + 1
            loc_nm = str(input("Please enter the name of the city/region that you want to add : "))
            query_loc = "INSERT INTO location_data VALUES (" + str(loc_id) + ", '" + loc_nm + "', '" + str(Admin_ID) + "');"

            cursor.execute(query_loc)
            print(" ")
            print("You have successfully added the location into the database!")
            print(" ")

        if(Adm_qry == 2):
            print()
            print("--------------------------xxxxxxxxxxxx-----------------------------")
            print("You have wished to remove an existing Customer/Driver")
            print("Please select the user whose data needs to be removed...")
            print("1. Customer")
            print("2. Driver")
            Data_rem = int(input("Please select the natuer of the user : "))
            if(Data_rem == 1):
                print(" ")
                print("--------------------------xxxxxxxxxxxx-----------------------------")
                print("You have wished to remove the data of the customer!")
                print(" ")
                Usr_name = str(input("Please enter the name of the user here : "))
                try:
                    query = ("""Delete from Customer where Customer.Customer_Name = '" + Usr_name + "';""")
                    cursor.execute(query)
                    print("The record of the user '" + Usr_name + "' has been removed from the database successfully")
                except:
                    print("The record of the user '" + Usr_name + "' does not exist")
                    print("Please check the information and try again")
            
            if(Data_rem == 2):
                print(" ")
                print("--------------------------xxxxxxxxxxxx-----------------------------")
                print("You have wished to remove the data of the driver!")
                print(" ")
                Drv_name = str(input("Please enter the name of the user here : "))
                try:
                    query = ("""Delete from Driver where Driver.Driver_Name = '" + Drv_name + "';""")
                    cursor.execute(query)
                    print("The record of the user '" + Drv_name + "' has been removed from the database successfully")
                except:
                    print("The record of the user '" + Drv_name + "' does not exist")
                    print("Please check the information and try again")

        if(Adm_qry == 3):
            print(" ")
            print("--------------------------xxxxxxxxxxxx-----------------------------")
            print("You have wished to view other queries")
            print("")
            print("The queries that can be executed are...")
            print("1. Embedded SQL queries")
            print("2. OLAP queries")
            print("3. Triggers")
            print("4. Basic SQL queries")
            print(" ")
            adm_misc = int(input("Please enter the nature of the query that you wish to execute : "))

            if(adm_misc == 1):
                print(" ")
                print("--------------------------xxxxxxxxxxxx-----------------------------")
                print("You wish to see the embedded SQL queries!")
                print("The embedded queries are...")
                print("1. SQL query to find the details of the driver where the rating of the driver is higher than the average rating")
                print("2. SQl query to find out the details of customers that have to pay fare that is greater than the average")
                print(" ")
                inpt1 = int(input("Please enter the query that you wish to see : "))

                if(inpt1 == 1):
                    print(" ")
                    print("--------------------------xxxxxxxxxxxx-----------------------------")
                    print(" ")
                    print("The details of the driver where the rating of the driver is higher than the average rating are :")
                    query = ("""SELECT Driver.driver_id, Driver.Driver_Name, Driver.Phone_Number, Driver.Car_Model
                    FROM bookings
                    INNER JOIN Driver ON  Driver.driver_id = bookings.driver_id
                    WHERE rating > (SELECT AVG(rating) FROM bookings);
                    """)
                    cursor.execute(query)
                    for each in cursor:
                        print(each)
                    print(" ")
                    print("--------------------------xxxxxxxxxxxx-----------------------------")
                    print(" ")
                
                elif(inpt1 == 2):
                    print(" ")
                    print("--------------------------xxxxxxxxxxxx-----------------------------")
                    print(" ")
                    print("The details of customers that have to pay fare that is greater than the average are : ")
                    query = ("""SELECT Customer.PickupID, Customer.Customer_Name, Customer.EmailID, bookings.fare
                    FROM bookings
                    INNER JOIN Customer ON Customer.PickupID = bookings.customer_id
                    where fare > (SELECT AVG(fare) FROM bookings); 
                    """)
                    cursor.execute(query)
                    for each in cursor:
                        print(each)
                    print(" ")
                    print("--------------------------xxxxxxxxxxxx-----------------------------")
                    print(" ")
            
            if(adm_misc == 2):
                print(" ")
                print("--------------------------xxxxxxxxxxxx-----------------------------")
                print(" ")
                print("You wish to see the OLAP queries!")
                print("The OLAP queries are : ")
                print("1. Total number of bookings made for each combination of pickup location, dropoff location, year, and month")
                print("2. Total number of bookings per customer and driver, as well as overall")
                print("3. Total number of bookings per month and overall")
                print("4. Number of active and completed bookings for each driver and overall")
                print("5. Average fare for each driver, broken down by pickup location")
                print("6. Average fare of bookings made during a particular month")
                print("7. Total revenue of a particular year")
                print("8. Total revenue collected in cash for a particular month")
                print("9. Total revenue earned from bookings made by each driver, for each location and for each year")
                print("10. Total revenue earned from bookings made by each customer, driver and for each location, and for each year")
                inpt3 = int(input("Please enter the OLAP query that you wish to see : ")) 

                if(inpt3 == 1):
                    print(" ")
                    print("--------------------------xxxxxxxxxxxx-----------------------------")
                    print("The query to view the total number of bookings made for each combination of pickup location, dropoff location, year, and month has been selected!")
                    print("The output for the given query is : ")
                    queryO = ("""SELECT pickup_location_id, dropoff_location_id, YEAR(pickup_time) AS year, MONTH(pickup_time) AS month, COUNT(*) AS total_bookings
                            FROM bookings
                            GROUP BY pickup_location_id, dropoff_location_id, YEAR(pickup_time), MONTH(pickup_time) WITH ROLLUP;""")
                    cursor.execute(queryO)
                    for each in cursor:
                        print("Pickup_Location, Dropoff_location, Year, Month, Total Bookings")
                        print(each)
                        print()
                    print("--------------------------xxxxxxxxxxxx-----------------------------")
                    print()

                elif(inpt3 == 2):
                    print(" ")
                    print("--------------------------xxxxxxxxxxxx-----------------------------")
                    print("The query to view the total number of bookings per customer and driver, as well as overall has been selected!")

                    queryO = ("""SELECT customer_id, driver_id, COUNT(*) AS num_bookings
                            FROM bookings
                            GROUP BY customer_id, driver_id WITH ROLLUP;""")
                    cursor.execute(queryO)
                    for each in cursor:
                        print("Customer_ID, Driver_ID, Number of Bookings")
                        print(each)
                        print(" ")

                    print("--------------------------xxxxxxxxxxxx-----------------------------")
                    print(" ")

                elif(inpt3 == 3):
                    print(" ")
                    print("--------------------------xxxxxxxxxxxx-----------------------------")
                    print("The query to view the total number of bookings per month and overall has been selected!")

                    queryO = ("""SELECT customer_id, driver_id, COUNT(*) AS num_bookings
                            FROM bookings
                            GROUP BY customer_id, driver_id WITH ROLLUP;""")
                    cursor.execute(queryO)
                    for each in cursor:
                        print("Customer_ID, Driver_ID, Month")
                        print(each)
                        print()

                    print("--------------------------xxxxxxxxxxxx-----------------------------")
                    print(" ")

                elif(inpt3 == 4):
                    print(" ")
                    print("--------------------------xxxxxxxxxxxx-----------------------------")
                    print("The query to view the number of active and completed bookings for each driver and overall has been selected!")

                    queryO = ("""SELECT driver_id, status, COUNT(*) AS bookings 
                            FROM bookings 
                            GROUP BY driver_id, status WITH ROLLUP;""")
                    cursor.execute(queryO)
                    for each in cursor:
                        print("Driver_ID, Status, Number of Bookings")
                        print(each)
                        print(" ")

                    print("--------------------------xxxxxxxxxxxx-----------------------------")
                    print(" ")

                elif(inpt3 == 5):
                    print(" ")
                    print("--------------------------xxxxxxxxxxxx-----------------------------")
                    print("The query to find the Average fare for each driver, broken down by pickup location has been selected!")

                    queryO = ("""SELECT driver_id, pickup_location_id, AVG(fare) AS avg_fare
                            FROM bookings
                            GROUP BY driver_id, pickup_location_id WITH ROLLUP;
                            """)
                    cursor.execute(queryO)
                    for each in cursor:
                        print("Driver_ID, Pickup_Location, Average_Fare")
                        print(each)
                        print(" ")

                    print("--------------------------xxxxxxxxxxxx-----------------------------")
                    print(" ")
                elif(inpt3 == 6):
                    print(" ")
                    print("--------------------------xxxxxxxxxxxx-----------------------------")
                    print("The query to find the average fare of booking in a particular month has been selected")
                    month = int(input("Please enter the month whose fare you wish to see : "))

                    queryS = ("SELECT AVG(fare) AS average_fare FROM bookings WHERE MONTH(pickup_time) = '" + str(month) + "';")
                    cursor.execute(queryS)
                    for each in cursor:
                        res = functools.reduce(lambda sub, ele: sub * 10 + ele, each)
                        print("The average fare for the selected month is : " + str(res))
                        print(" ") 
                    print("--------------------------xxxxxxxxxxxx-----------------------------")
                    print(" ")

                elif(inpt3 == 7):
                    print(" ")
                    print("--------------------------xxxxxxxxxxxx-----------------------------")
                    print("The query to find the total revenue in a given year has been selected!")
                    year = int(input("Please enter the year whose revenue you wish to see : "))

                    queryS = ("SELECT SUM(fare) AS total_revenue FROM bookings WHERE YEAR(pickup_time) = '" + str(year) + "';")
                    cursor.execute(queryS)
                    for each in cursor:
                        res = functools.reduce(lambda sub, ele: sub * 10 + ele, each)
                        print("The total revenue for the year '"+str(year)+"' is '" + str(res) +"'")
                        print(" ")
                    print("--------------------------xxxxxxxxxxxx-----------------------------")
                    print(" ")

                elif(inpt3 == 8):
                    print(" ")
                    print("--------------------------xxxxxxxxxxxx-----------------------------")
                    print("The query to find the total revenue in a given month paid in cash has been selected!")
                    month = int(input("Please enter the month whose revenue you want to see : "))

                    queryS = ("SELECT SUM(fare) AS total_revenue FROM bookings WHERE MONTH(pickup_time) = '" + str(month) + "' AND payment_method = 'Cash';")
                    cursor.execute(queryS)
                    for each in cursor:
                        res = functools.reduce(lambda sub, ele: sub * 10 + ele, each)
                        print("The total revenue in Cash for the month '" + str(month) + "' is '" + str(res) +"'")
                        print()
                    print("--------------------------xxxxxxxxxxxx-----------------------------")
                    print()

                elif(inpt3 == 9):
                    print()
                    print("--------------------------xxxxxxxxxxxx-----------------------------")
                    print("The query to find the total revenue earned from bookings made by each driver, for each location and for each year!")
                    print()
                    print("Please note that the current query cannot be executed as it has been depreciated after being run in a foreign enviornment")
                    print("....")
                    print("Please select anoter query")
                    print("Process Terminated!")
                    print("--------------------------xxxxxxxxxxxx-----------------------------")
                    print()  
                
                elif(inpt3 == 10):
                    print()
                    print("--------------------------xxxxxxxxxxxx-----------------------------")
                    print("The query to find the total revenue earned from bookings made by each customer, driver and for each location, and for each year!")
                    print()
                    print("Please note that the current query cannot be executed as it has been depreciated after being run in a foreign enviornment")
                    print("....")
                    print("Please select anoter query")
                    print("Process Terminated!")
                    print("--------------------------xxxxxxxxxxxx-----------------------------")
                    print() 
            
            if(adm_misc == 3):
                print()
                print("--------------------------xxxxxxxxxxxx-----------------------------")
                print()
                print("The triggers that have been deployed in the database are...")
                print("1. Trigger to set the pending charges of the customer to 0 after the trip is compleated")
                print("2. Trigger to update the status of the driver after the trip is complete, cancelled, or active")
                print()
                ipt2 = int(input("Please enter the trigger that you want to see : "))
                if(ipt2 == 2):
                    print()
                    print("--------------------------xxxxxxxxxxxx-----------------------------")
                    print("The trigger to update the status of the driver after the trip is complete, cancelled, or active has been selected")
                    print()
                    name = []
                    CurrentState = []
                    driver_id = int(input("Please enter the ID of the driver here : "))

                    Driver_Info1 = ("select Driver.CurrentState, Driver.driver_id, Driver.Driver_Name from Driver where driver_id = '" +str(driver_id) + "'  ;")
                    cursor.execute(Driver_Info1)
                    for each in cursor:
                        print(each)
                    print()
                    
                    Driver_Name = ("Select Driver.Driver_Name from Driver where driver_id = '" +str(driver_id) + "'  ;")
                    cursor.execute(Driver_Name)
                    for each in cursor:
                        name.insert(0, each)
                    
                    Driver_Status = ("Select Driver.CurrentState from Driver where driver_id = '" +str(driver_id) + "'  ;")
                    cursor.execute(Driver_Status)
                    for each in cursor:
                        res = functools.reduce(lambda sub, ele: sub * 10 + ele, each)
                        if(res == 1):
                            CurrentState.insert(0, "Free")
                        if(res == 0):
                            CurrentState.insert(0, "Occupied")
                    print("The current status of the selected driver is : " + str(CurrentState[0]))
                    print()

                    yn = str(input("Do you wish to make changes to the driver data? "))
                    if(yn == "Y" or yn == "y"):
                        print("You have wished to make changes to the selected driver data!")
                        booking_Status = str(input("Please enter the status of the booked trip for the seleced driver : "))

                        if(booking_Status == "Active"):
                            print("The trip status has been set to 'Active' !")

                            Update_State1 = ("Update bookings set status = '" + str(booking_Status) + "' where booking_id = '" + str(driver_id) + "';")
                            cursor.execute(Update_State1)
                            print()

                            Driver_Status = ("Select Driver.CurrentState from Driver where driver_id = '" +str(driver_id) + "'  ;")
                            cursor.execute(Driver_Status)
                            for each in cursor:
                                res = functools.reduce(lambda sub, ele: sub * 10 + ele, each)
                                if(res == 1):
                                    CurrentState.insert(0, "Free")
                                if(res == 0):
                                    CurrentState.insert(0, "Occupied")
                            print("The current status of the selected driver is : " + str(CurrentState[0]))

                        if(booking_Status == "Compleated" or booking_Status == "Completed" or booking_Status == "Cancelled"):
                            print("The trip status has been set to '" + str(booking_Status) +"'! ")

                            Update_State2 = ("Update bookings set status = '" + str(booking_Status) + "' where booking_id = '" + str(driver_id) + "';")
                            cursor.execute(Update_State2)
                            print()

                            Driver_Status = ("Select Driver.CurrentState from Driver where driver_id = '" +str(driver_id) + "'  ;")
                            cursor.execute(Driver_Status)
                            for each in cursor:
                                res = functools.reduce(lambda sub, ele: sub * 10 + ele, each)
                                if(res == 1):
                                    CurrentState.insert(0, "Free")
                                if(res == 0):
                                    CurrentState.insert(0, "Occupied")
                            print("The current status of the selected driver is : " + str(CurrentState[0]))

                    if(yn == "N" or yn == "n"):
                        print("You have wished to not change the data of the given driver!")
                        print("No changes were made...")
                        print("The trigger was not executed!")

                    print()
                    print("--------------------------xxxxxxxxxxxx-----------------------------")
                    print()

                if(ipt2 == 1):
                    print()
                    print("--------------------------xxxxxxxxxxxx-----------------------------")
                    print("The trigger to set the pending charges of the customer to 0 after the trip is compleated has been selected")
                    print()
                    customer_id = int(input("Please enter id of the customer whose details you want to see : "))
                    print("The details of the customer with ID : " + str(customer_id) + " are : ")
                    master_set = ("update Customer set Pending_charges = 373 where customer_id = '" + str(customer_id) + "';")
                    cursor.execute(master_set)
                    Customer_INfo0 = ("Select Customer.PickupID, Customer.Customer_Name, Customer.Phone_Number, Customer.Pending_charges from Customer where customer_id = '" + str(customer_id) + "';")
                    cursor.execute(Customer_INfo0)
                    for each in cursor:
                        print(each)
                                    
                    name = []
                    pending_charges = []
                    print()
                    yn = str(input("Do you wish to change the status of the trip for the selected customer? "))
                    
                    if(yn == "Y" or yn == "y"):
                        print("You have wished to change the trip status for the given customer!")
                        print()
                        status = str(input("Please enter the status of the trip for the customer : "))

                        Customer_name = ("Select Customer.Customer_Name from Customer where customer_id = '" + str(customer_id) + "';")
                        cursor.execute(Customer_name)
                        for each in cursor:
                            res1 = functools.reduce(lambda sub, ele: sub * 10 + ele, each)
                            name.insert(0, res1)
                            
                        Customer_Charges =  ("Select Customer.Pending_charges from Customer where customer_id = '" + str(customer_id) + "';")
                        cursor.execute(Customer_Charges)
                        for each in cursor:
                            res = functools.reduce(lambda sub, ele: sub * 10 + ele, each)
                            pending_charges.insert(0, res)
                        print()

                        print()
                        master_set = ("update Customer set Pending_charges = 373 where customer_id = '" + str(customer_id) + "';")
                        cursor.execute(master_set)
                        Customer_Info = ("Select Customer.PickupID, Customer.Customer_Name, Customer.Phone_Number, Customer.Pending_charges from Customer where customer_id = '" + str(customer_id) + "';")
                        cursor.execute(Customer_Info)
                        for each in cursor:
                            print(each)

                        print("The pending charges of the customer '" + str(name[0]) + "' are : '" + str(pending_charges[0]) + "'")
                        print()

                        print("The status of the customer is being changed...")
                        Customer_Update = ("update bookings set status = '" + status + "' where booking_id = '" + str(customer_id)+ "';")
                        cursor.execute(Customer_Update)

                        print("The status of the customer after the trigger was executed is : ")
                        Customer_Info2 = ("Select Customer.PickupID, Customer.Customer_Name, Customer.Phone_Number, Customer.Pending_charges from Customer where customer_id = '" + str(customer_id) + "';")
                        cursor.execute(Customer_Info2)
                        for each in cursor:
                            print(each)
                        print()

                        Customer_name = ("Select Customer.Customer_Name from Customer where customer_id = '" + str(customer_id) + "';")
                        cursor.execute(Customer_name)
                        for each in cursor:
                            res1 = functools.reduce(lambda sub, ele: sub * 10 + ele, each)
                            name.insert(0, res1)
                        Customer_Charges = ("Select Customer.Pending_charges from Customer where customer_id = '" + str(customer_id) + "';")
                        cursor.execute(Customer_Charges)
                        for each in cursor:
                            res = functools.reduce(lambda sub, ele: sub * 10 + ele, each)
                            pending_charges.insert(0, res)
                        
                        print("The pending charges of the customer '" + str(name[0]) + "' are : '" + str(pending_charges[0]) + "'")
                        print()
                        master_set = ("update Customer set Pending_charges = 373 where customer_id = '" + str(customer_id) + "';")
                        cursor.execute(master_set)
                    elif(yn == "N" or yn == "n"):
                        print("You have choosen to not make any changes!")
                        print()

                    print("--------------------------xxxxxxxxxxxx-----------------------------")
                    print()
            
            if(adm_misc == 4):
                print()
                print("--------------------------xxxxxxxxxxxx-----------------------------")
                print("You have wished to see the basic SQL queries")
                print(" ")
                print("You can execute the following basic MySQL queries...")
                print("1. Show driver's information for a particular customer")
                print("2. Retrieve all bookings made by a particular customer")
                print("3. Show the total revenue generated by a specific taxi driver for a given time period")
                print("4. Find the average rating of a particular driver based on all the ratings given by customers")
                print("5. Show all active bookings for a particular driver")
                print("6. Get the total number of bookings made in a day/week/month.; start_date and end_date should be in the format YYYY-MM-DD HH:MM:SS")
                print("7. Display the details of a specific booking, including the pickup and drop-off locations, fare, and payment information")
                print("8. Retrieve a list of cancelled bookings for a particular time period.start_date and end_date should be in the format YYYY-MM-DD HH:MM:SS")
                print("9. Get the total number of completed bookings for a particular taxi driver")
                print("10. Get all the bookings for a specific driver on a specific date")
                print(" ")
                qu_ip = int(input("Please enter the query that you would like to execute : "))
                print(" ")
                if(qu_ip == 1):
                    print(" ")
                    print("--------------------------xxxxxxxxxxxx-----------------------------")
                    print("The query to retrive the drivers information for a particular has been selected")
                    print(" ")

                    query = ("SELECT Customer.Customer_Name, Driver.Driver_Name, Driver.Phone_Number, Driver.Car_Model FROM Customer INNER JOIN Driver ON Customer.PickupID=Driver.driver_id;")
                    cursor.execute(query)
                    for each in cursor:
                        print("Customer : " + each[0])
                        print("Driver : " + each[1])
                        print("Phone Number : " + each[2])
                        print("Car Model : " + each[3])
                        print(' ')
                    
                    print(" ")
                    print("--------------------------xxxxxxxxxxxx-----------------------------")
                    print(" ")

                if(qu_ip == 2):
                    print(" ")
                    print("--------------------------xxxxxxxxxxxx-----------------------------")
                    print("The query to retrieve all bookings made by a particular customer has been selected")
                    print(" ")

                    query = ("SELECT * FROM bookings WHERE customer_id = bookings.customer_id;")
                    cursor.execute(query)
                    for each in cursor:
                        print("Booking ID : " + str(each[0]))
                        print("Fare : " + str(each[6]))
                        print("Payement Method : " + each[7])
                        print("Status : " + each[8])
                        print("Customer Rating : " + str(each[10]))
                        print(' ')

                    print(" ")
                    print("--------------------------xxxxxxxxxxxx-----------------------------")
                    print(" ")
                
                if(qu_ip == 3):
                    print(" ")
                    print("--------------------------xxxxxxxxxxxx-----------------------------")
                    print("The query to show the total revenue generated by a specific taxi driver for a given time period has been selected")
                    print(" ")

                    driver_id = int(input("Please enter the driver is : "))
                    init_date = str(input("Please enter the start date (yyyy-mm-dd) : "))
                    end_date = str(input("Please enter the end date (yyyy-mm-dd) : "))

                    query = "SELECT SUM(fare) FROM bookings WHERE driver_id = %s AND pickup_time BETWEEN %s AND %s"
                    cursor.execute(query, (driver_id, init_date, end_date))

                    for each in cursor:
                        print("The money generated totals : " + each[0])
                    
                    print(" ")
                    print("--------------------------xxxxxxxxxxxx-----------------------------")
                    print(" ")


                if(qu_ip == 4):
                    print(" ")
                    print("--------------------------xxxxxxxxxxxx-----------------------------")
                    print("The query to find the average rating of a particular driver based on all the ratings given by customers has been selected")
                    print(" ")

                    driver_id = int(input("Please enter the driver id : "))
                    query = "SELECT AVG(rating) FROM bookings WHERE driver_id = %s AND status='Completed' AND rating>0;"
                    cursor.execute(query, (driver_id,))
                    for each in cursor:
                        print("Driver ID : " + str(driver_id))
                        print("Average Rating : " + str(each[0]))
                    
                    print(" ")
                    print("--------------------------xxxxxxxxxxxx-----------------------------")
                    print(" ")
                
                if(qu_ip == 5):
                    print(" ")
                    print("--------------------------xxxxxxxxxxxx-----------------------------")
                    print("The query to show all active bookings for a particular driver has been selected")
                    print(" ")

                    driver_id = int(input("Please enter the driver id : "))
                    query = "SELECT * FROM bookings WHERE driver_id = %s AND status = 'Active'"
                    cursor.execute(query, (driver_id,))
                    for each in cursor:
                        print("Booking ID : " + str(each[0]))
                        print("Driver ID : " + str(each[2]))
                        print("Pickup Time : " + str(each[5]))
                        print("Fare : " + str(each[6]))
                        print("Payement Method : " + each[7])
                        print(' ')
                    
                    print(" ")
                    print("--------------------------xxxxxxxxxxxx-----------------------------")
                    print(" ")
                
                if(qu_ip == 6):
                    print(" ")
                    print("--------------------------xxxxxxxxxxxx-----------------------------")
                    print("The query to get the total number of bookings made in a day/week/month.; start_date and end_date should be in the format YYYY-MM-DD HH:MM:SS has been selected")
                    print(" ")

                    init_date = str(input("Please enter the start date (yyyy-mm-dd) : "))
                    end_date = str(input("Please enter the end date (yyyy-mm-dd) : "))
                    query = "SELECT COUNT(*) FROM bookings WHERE pickup_time BETWEEN %s AND %s;"
                    cursor.execute(query, (init_date, end_date))
                    print(" ")
                    for each in cursor:
                        print("The number of bookings between " + str(init_date) +" and " + str(end_date) +" were "+ str(each[0]) + "")
                        print(" ")
                    
                    print(" ")
                    print("--------------------------xxxxxxxxxxxx-----------------------------")
                    print(" ")

                
                if(qu_ip == 7):
                    print(" ")
                    print("--------------------------xxxxxxxxxxxx-----------------------------")
                    print("The query to display the details of a specific booking, including the pickup and drop-off locations, fare, and payment information has been selected")
                    print(" ")

                    booking_id = int(input("Please enter the booking id : "))
                    query = "SELECT status, fare, payment_method FROM bookings WHERE booking_id = %s;"
                    cursor.execute(query, (booking_id,))
                    for each in cursor:
                        print("Status : " + each[0])
                        print("Fare : " + str(each[1]))
                        print("Payement Method : " + each[2])
                        print(" ")
                    
                    print(" ")
                    print("--------------------------xxxxxxxxxxxx-----------------------------")
                    print(" ")
                
                if(qu_ip == 8):
                    print(" ")
                    print("--------------------------xxxxxxxxxxxx-----------------------------")
                    print("The query to retrieve a list of cancelled bookings for a particular time period.start_date and end_date should be in the format YYYY-MM-DD HH:MM:SS has been selected")
                    print(" ")

                    init_date = str(input("Please enter the start date (yyyy-mm-dd) : "))
                    end_date = str(input("Please enter the end date (yyyy-mm-dd) : "))
                    query = "SELECT * FROM bookings WHERE status = 'Cancelled' AND cancel_time BETWEEN %s  AND %s;"
                    row = cursor.fetchone()
                    row = cursor.execute(query, (init_date, end_date))
                    if row:
                        for each in cursor:
                            print("Booking ID : " + str(each[0]))
                            print("Driver ID : " + str(each[2]))
                            print("Pickup Time : " + str(each[5]))
                            print("Fare : " + str(each[6]))
                            print("Payement Method : " + each[7])
                            print(' ')
                    else:
                        print(" ")
                        print("No booking was cancelled!")
                    
                    print(" ")
                    print("--------------------------xxxxxxxxxxxx-----------------------------")
                    print(" ")
                
                if(qu_ip == 9):
                    print(" ")
                    print("--------------------------xxxxxxxxxxxx-----------------------------")
                    print("The query to get the total number of completed bookings for a particular taxi driver has been selected")
                    print(" ")

                    driver_id = int(input("Please enter the driver id : "))
                    query = "SELECT COUNT(*) FROM bookings WHERE driver_id = %s AND status = 'Completed';"
                    for each in cursor:
                        print("Driver ID : " + str(driver_id))
                        print("Bookings Completed : " + str(each[0]))
                    
                    print(" ")
                    print("--------------------------xxxxxxxxxxxx-----------------------------")
                    print(" ")
                
                if(qu_ip == 10):
                    print(" ")
                    print("--------------------------xxxxxxxxxxxx-----------------------------")
                    print("The query to get all the bookings for a specific driver on a specific date has been selected")
                    print(" ")

                    driver_id = int(input("Please enter the driver id : "))
                    init_date = str(input("Please enter the pickup date (yyyy-mm-dd) : "))
                    query = "SELECT * FROM bookings WHERE driver_id = %s AND DATE(pickup_time) = %s;"
                    cursor.execute(query, (driver_id, init_date))
                    for each in cursor:
                        print(' ')
                        print("Booking ID : " + str(each[0]))
                        print("Driver ID : " + str(each[2]))
                        print("Pickup Time : " + str(each[5]))
                        print("Fare : " + str(each[6]))
                        print("Payement Method : " + each[7])
                    
                    print(" ")
                    print("--------------------------xxxxxxxxxxxx-----------------------------")
                    print(" ")
                    
            


if(lg_Sn == 2):
    print()
    print("You have deciced  to register yourself!")
    print("The roles that you can register as are as follows...")
    print("1. Admin")
    print("2. Customer")
    print("3. Driver")
    print()
    Sg_Usr = int(input("Please enter the role that you want to register yourself for : "))
    print()

    if(Sg_Usr == 1):
        print("You have decided to sign up as an Admin!")
        print("")
        cursor.execute("Select * from Admin")
        last_entry = list(cursor)[-1]
        last_id = list(last_entry)[0]
        addr_id = last_id + 1
        name = str(input("Please enter your name here : "))
        Addr = str(input("Please enter your address here : "))
        Phone = str(input("Please enter your phone number here : "))
        Email = str(input("Please enter your email here : "))
        cursor.execute("INSERT INTO Admin VALUES (" + str(addr_id) + ", '" + str(addr_id) + " ', '" + str(addr_id) + " ', '" + name + "', '" + Addr + "', '" + Phone + "', '" + Email + "');")
        cnx.commit()
        print(" ")
        print("Congratualtions, you have successfully registered as an admin!")
        print(" ")
        print("--------------------------xxxxxxxxxxxx-----------------------------")
        print(" ")

    if(Sg_Usr == 2):
        print("You have decided to sign up as a Customer")
        print(' ')
        cursor.execute("Select * from Customer")
        last_entry = list(cursor)[-1]
        last = list(last_entry)[0]
        pick_id = last + 1
        name = str(input("Please enter your name here : "))
        Phone = str(input("Please enter your phone number here : "))
        Email = str(input("Please enter your email here : "))
        pending_crg= 0
        password = str(input("Please enter a strong password : "))
        cursor.execute("INSERT INTO Customer VALUES (" + str(pick_id) + ", '" + str(pick_id) + "', '" + name + "', '" + Phone + "', '" + Email + "', '" + str(pending_crg) + "', '" + password + "');")
        cnx.commit()
        print(" ")
        print("Congratualtions, you have successfully registered as a customer!")
        print(" ")
        print("--------------------------xxxxxxxxxxxx-----------------------------")
        print(" ")
    
    if(Sg_Usr == 3):
        print("You have decided to sign up as a Driver")
        print(' ')
        cursor.execute("Select * from Customer")
        last_entry = list(cursor)[-1]
        last = list(last_entry)[0]
        drv_id = last + 1
        curSt = 1
        name = str(input("Please enter your name here : "))
        Phone = str(input("Please enter your phone number here : "))
        Car_mod = str(input("Please enter the model of your car here : "))
        car_num = str(input("Please enter the number of your car here : "))
        license_num = str(input("Please enter your license number here : "))
        EmailID = str(input("Please enter your emailID here : "))
        password = str(input("Please enter a strong password : "))
        cursor.execute("INSERT INTO Driver VALUES (" + str(curSt) + ", '" + str(drv_id) + " ', '" + name+ " ', '" + Phone + "', '" + Car_mod + "', '" + car_num + "', '" + license_num + "', '"+ str(EmailID) + "', '" + password + "');")
        cnx.commit()
        print(" ")
        print("Congratualtions, you have successfully registered as a driver!")
        print(" ")
        print("--------------------------xxxxxxxxxxxx-----------------------------")
        print(" ")


cursor.close()
cnx.close()

