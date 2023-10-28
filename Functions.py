import mysql.connector as mycon
import csv
import random
import pickle
import os
import datetime

def SignUp():
    con = mycon.connect(
        host='localhost',
        user='root',
        password='password',
        port=3306,
        database='railway_system_demo'
    )
    cur = con.cursor()
    print("SIGN UP\n")
    name = input("Enter your name: ")
    age = int(input("Enter your age: "))
    gender = input("Enter your gender (M/F): ")
    aadhaar = int(input("Enter your 12 digit AADHAAR No.: "))
    phone = int(input("Enter your phone no.: "))
    email = input("Enter email ID: ")
    username = input("Create your username: ")
    password = input("Create a new password: ")
    while len(password) > 16 or len(password) == 0:     # CHECKS IF THE PASSWORD IS CONTAINING LESS THAN 16 CHARECTERS AND IS NOT EMPTY
        print("PASSWORD SHOULD NOT BE EMPTY AND IT SHOULD NOT HAVE MORE THAN 16 CHARACTERS")
        password = input("Create a new password: ")
    conf_pass = input("Confirm your password: ")
    while conf_pass != password:        # CHECKS IF THE PASSWORD MATCHES WITH THE ORIGINAL PASSWORD
        print("PASSWORD DOESN'T MATCH")
        conf_pass = input("Confirm your password: ")

    user_query = "INSERT INTO user_details (username, name, age, gender, aadhaar, phone, email) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    login_query = "INSERT INTO login_details (username, password) VALUES (%s, %s)"

    user_data = (username, name, age, gender, aadhaar, phone, email)
    login_data = (username, password)

    try:
        cur.execute(user_query, user_data)
        con.commit()
        cur.execute(login_query, login_data)
        con.commit()
        print("\nYOUR ACCOUNT HAS BEEN CREATED SUCCESSFULLY.\nYOU CAN NOW PROCEED TO THE SIGN IN PAGE.")
    except Exception as e:
        print("Error:", e)
        con.rollback()
    finally:
        con.close()



def SignIn():
    con=mycon.connect(
        host='localhost',
        user='root',
        password='password',
        port=3306,
        database='railway_system_demo'
    )
    cur=con.cursor()
    print("SIGN IN\n")
    username=input("Enter your username : ")
    password=input("Enter password : ")
    query="select * from login_details"
    cur.execute(query)
    result=cur.fetchall()
    for i in result :
        if i[0]==username:      # SEARCH FOR THE USERNAME IN DATABASE
            if i[1]==password:      # CHECKS THE PASSWORD IN DATABASE
                print ("Sign In Successful")
                con.close()
                return True,username
            else:
                print("PASSWORD DOESN'T MATCH")
                return False,""
    else:
        print("USER NOT FOUND.\nPLEASE CHECK YOUR USERNAME AS IT MAY BE WRONG\nELSE YOU NEED TO SIGN UP AS A NEW USER.")
        return False,""
    




def AdminLogin():
    username=input("Enter admin username : ")
    password=input("Enter admin password : ")
    if username=="admin" and password=="login@Admin":       # admin username = "admin" & password = "login@Admin"
        return True
    else:
        print("INVALID LOGIN CREDENTIALS")
        return False
    



def CalculateFare(train_type,class_type,nop):
    train_fare={'Superfast':100,'Duronto':150,'Rajdhani':200,'Shatabdi':150,'Vande Bharat':200}
    class_fare={'1A':2000,'2A':1200,'3A':700,'SL':300,'EC':1500,'CC':900,'2S':200}
    reservation_charge={'1A':60,'2A':50,'3A':40,'SL':20,'EC':50,'CC':40,'2S':15}
    fare=train_fare[train_type] + class_fare[class_type] + reservation_charge[class_type]
    if class_type not in ('SL','2S'):
        gst=0.05*fare
        fare=fare+gst   # 5% GST for AC Classes
    fare=fare*nop
    print(f"Train fare = ₹{train_fare[train_type]*nop}\nClass fare = ₹{class_fare[class_type]*nop}\nReservation Charge = ₹{reservation_charge[class_type]*nop}\nGST = ₹{gst*nop}")
    return fare



def AddStation():
    f=open("Stations.dat","ab+")
    f.close()
    f=open("Stations.dat","rb")
    data={}
    flag=0
    station_code=input("Enter station code : ")
    station_name=input("Enter station name : ")
    while True:
        try:
            data=pickle.load(f)
            data[station_code]=station_name
            flag=1
        except:
            f.close()
            break
    if flag==0:
        print("Unable to add station")
    f=open("Stations.dat","wb")
    pickle.dump(data,f)
    if flag==1:
        print("Station added successfully")
    f.close()




def DeleteStation():
    f=open("Stations.dat","rb")
    data={}
    flag=0
    station_code=input("Enter station code : ")
    while True:
        try:
            data=pickle.load(f)
            del data[station_code]
            flag=1
        except:
            f.close()
            break
    if flag==0:
        print("Station not found")
    f=open("Stations.dat","wb")
    pickle.dump(data,f)
    print("Station deleted successfully")
    f.close()



def AddTrain():
    # Adding data to csv file
    f=open("Trains.csv","a+",newline="")
    wobj=csv.writer(f)
    train_no=int(input("Enter train no : "))
    train_name=input("Enter train name : ")
    stations=eval(input("Enter all stations (format=['HWH','DGR','NJP',...]) : "))
    src=stations[0]
    dstn=stations[len(stations)-1]
    category=input("Enter train category : ")
    data=[train_no,train_name]
    for i in stations:
        data.append(i)
    wobj.writerow(data)
    f.close()

    # Adding data to SQL
    con = mycon.connect(
        host='localhost',
        user='root',
        password='password',
        port=3306,
        database='railway_system_demo'
    )
    cur = con.cursor()
    query = "INSERT INTO train_details (train_no, train_name, category, source, destination) VALUES (%s, %s, %s, %s, %s)"
    row=(train_no,train_name,category,src,dstn)
    try:
        cur.execute(query,row)
        con.commit()
        print("NEW TRAIN ADDED SUCCESSFULLY")
    except Exception as e:
        print("Error:", e)
        con.rollback()
    finally:
        con.close()
    
    




def DeleteTrain():
    # REMOVING FROM CSV FILE
    f1=open("Trains.csv","r")
    f2=open("temp.csv","w",newline="")
    robj=csv.reader(f1)
    wobj=csv.writer(f2)
    train_no=int(input("Enter train no : "))
    flag=0
    for i in robj:
        if i[0]!=train_no:
            wobj.writerow(i)
        else:
            flag=1
    f1.close()
    f2.close()
    os.remove("Trains.csv")
    os.rename("temp.csv","Trains.csv")

    # REMOVING FROM DATABASE
    if flag==0:
        con = mycon.connect(
            host='localhost',
            user='root',
            password='password',
            port=3306,
            database='railway_system_demo'
        )
        cur = con.cursor()
        query = "delete from train_details where train_no="+str(train_no)
        cur.execute(query)
        con.close()
        print("Train deleted successfully")

    elif flag==1:
        print("Train not found")




def BookingDetails():
    con = mycon.connect(
        host='localhost',
        user='root',
        password='password',
        port=3306,
        database='railway_system_demo'
    )
    cur = con.cursor()
    cur.execute('select * from bookings')
    result=cur.fetchall()
    print("%10s"%"PNR",
          "%20s"%"username",
          "%8s"%"Train No",
          "%5s"%"Class",
          "%8s"%"Board At",
          "%11s"%"Destination",
          "%3s"%"NOP",
          "%12s"%"Booking Date",
          "%12s"%"Journey Date",
          "%7s"%"Fare"
          )
    for row in result:
        print("%10s"%row[0],
            "%20s"%row[1],
            "%8s"%row[2],
            "%5s"%row[3],
            "%8s"%row[4],
            "%11s"%row[5],
            "%3s"%row[6],
            "%12s"%row[7],
            "%12s"%row[8],
            "%7s"%row[9]
            )
    con.close()





def BookTicket(username):
    # Board_at
    f = open("Stations.dat", "rb")
    data = {}
    while True:
        try:
            data = pickle.load(f)
        except:
            f.close()
            break
    for i in data:
        print(f"{i} - {data[i]}")
    src = input("Enter Boarding Station Code: ")
    src_name = data[src]
    print()

    # Destination
    for i in data:
        if i != src:
            print(f"{i} - {data[i]}")
    dstn = input("Enter Destination Station Code: ")
    dstn_name = data[dstn]

    # Train Schedule
    f = open("Trains.csv", "r")
    robj = csv.reader(f)
    flag = 0
    for i in robj:
        try:
            s = i.index(src)
            d = i.index(dstn)
            if s < d:  # Check if the source station comes before the destination
                print(f"Train no : {i[0]}   Train name : {i[1]}")
                flag += 1
        except ValueError:
            continue

    if flag == 0:
        print("NO TRAINS FOUND IN THE GIVEN ROUTE")



    # Booking Train
    train_no=int(input("Enter train no : "))
    con = mycon.connect(
        host='localhost',
        user='root',
        password='password',
        port=3306,
        database='railway_system_demo'
    )
    cur = con.cursor()
    query="SELECT train_name,category FROM train_details"
    cur.execute(query)
    result=cur.fetchall()
    con.close()
    for row in result:
        train_name,category=(row[0],row[1])
    print(f"{train_no} - {train_name}")
    print("\nAvailable Class Type :")
    if category=="Rajdhani":
        print("3A\n2A\n1A\n")
    elif category=="Vande Bharat" or category=="Shatabdi":
        print("EC\nCC\n")
    elif category=="Duronto":
        print("3A\n2A\n1A\nSL\n2S\n")
    else:
        print("3A\n2A\n1A\nSL\n2S\n")
    class_type=input("Enter your choice : ")
    coach={'1A':'H','2A':'A','3A':'B','SL':'S','EC':'E','CC':'C','2S':'D'}
    coach_no=coach[class_type]+str(random.randint(1,8))
    doj=input("Enter date of journey (YYYY-MM-DD) : ")
    seats={'1A':24,'2A':52,'3A':72,'SL':72,'EC':56,'CC':78,'2S':108}
    seat_no=random.randint(1,seats[class_type]-4)


    # Passenger Details
    nop=int(input("Enter total no. of passengers : "))
    passenger_details=[]
    for i in range(1,nop+1):
        print("Enter details of passenger",i)
        name=str(input("Name : "))
        age=int(input("Age : "))
        gender=str(input("Gender (M/F) : "))
        data=[name,age,gender,seat_no]
        passenger_details.append(data)
        seat_no+=1
    pnr=random.randint(1000000000,9999999999)
    dob=datetime.date.today()


    # Printing Ticket
    print("\nTicket\n")
    print(f"PNR = {pnr}")
    print(f"Train : {train_no}-{train_name}")
    print(f"Class = {class_type}")
    print(f"Board at : {src} - {src_name}")
    print(f"Destination : {dstn} - {dstn_name}")
    print(f"Date of Booking : {dob}")
    print(f"Date of Journey : {doj}")
    print("Passenger Details : ")
    print("%30s"%"Name",
          "%3s"%"Age",
          "%6s"%"Gender",
          "%5s"%"Coach",
          "%4s"%"Seat",
          "%6s"%"Status"
          )
    for data in passenger_details:
        print("%30s"%data[0],
              "%3s"%data[1],
              "%6s"%data[2],
              "%5s"%coach_no,
              "%4s"%data[3],
              "%6s"%"CNF"
            )
    fare=CalculateFare(category,class_type,nop)
    print(f"Total fare = ₹{fare}")


    # Updating to database
    con = mycon.connect(
        host='localhost',
        user='root',
        password='password',
        port=3306,
        database='railway_system_demo'
    )
    cur = con.cursor()
    query="INSERT INTO bookings(PNR, username, train_no, class, board_at, destination, NOP, booking_date, journey_date, fare) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    row=(pnr,username,train_no,class_type,src,dstn,nop,dob,doj,fare)
    try:
        cur.execute(query,row)
        con.commit()
        print("BOOKING SUCCESSFUL")
    except Exception as e:
        print("Error:", e)
        con.rollback()
    finally:
        con.close()

    # Creating a CSV file
    f_name=str(pnr)+'.csv'
    f=open(f_name,"w")
    wobj=csv.writer(f)
    for data in passenger_details:
        row=[data[0],data[1],data[2],coach_no,data[3],"CNF"]
        wobj.writerow(row)
    f.close()




def CancelTicket():
    # Removing from SQL
    con = mycon.connect(
        host='localhost',
        user='root',
        password='password',
        port=3306,
        database='railway_system_demo'
    )
    cur = con.cursor()
    pnr = int(input("Enter the PNR of the ticket to be cancelled : "))
    query = "DELETE FROM bookings WHERE PNR=%s;" % (pnr)
    cur.execute(query)
    con.commit()
    f_name=str(pnr)+'.csv'
    os.remove(f_name)
    print("Ticket cancelled successfully.")




def PNRStatus(pnr):
    con = mycon.connect(
        host='localhost',
        user='root',
        password='password',
        port=3306,
        database='railway_system_demo'
    )
    cur = con.cursor()
    query="SELECT * FROM bookings where PNR="+str(pnr)
    cur.execute(query)
    result=cur.fetchall()
    for row in result:
        train_no=row[2]
        class_type=row[3]
        src=row[4]
        dstn=row[5]
        dob=row[7]
        doj=row[8]
        fare=row[9]
    
    query="SELECT * FROM train_details where train_no="+str(train_no)
    cur.execute(query)
    result=cur.fetchall()
    for row in result:
        train_name=row[1]
    con.close()

    f = open("Stations.dat", "rb")
    data = {}
    while True:
        try:
            data = pickle.load(f)
        except:
            f.close()
            break
    src_name=data[src]
    dstn_name=data[dstn]
    f.close()

    f_name=str(pnr)+'.csv'
    f=open(f_name,"r",newline="")
    robj=csv.reader(f)

    print(f"PNR : {pnr}")
    print(f"Train : {train_no}-{train_name}")
    print(f"Class = {class_type}")
    print(f"Board at : {src} - {src_name}")
    print(f"Destination : {dstn} - {dstn_name}")
    print(f"Date of Booking : {dob}")
    print(f"Date of Journey : {doj}")
    print(f"Fare = ₹{fare}")
    print("Passenger Details : ")
    print("%30s"%"Name",
          "%3s"%"Age",
          "%6s"%"Gender",
          "%5s"%"Coach",
          "%4s"%"Seat",
          "%6s"%"Status"
        )
    for row in robj:
        try:
            print("%30s"%row[0],
                "%3s"%row[1],
                "%6s"%row[2],
                "%5s"%row[3],
                "%4s"%row[4],
                "%6s"%row[5]
                )
        except:
            continue
    f.close()



def MyBookings(username):
    con = mycon.connect(
        host='localhost',
        user='root',
        password='password',
        port=3306,
        database='railway_system_demo'
    )
    cur = con.cursor()
    query = "select PNR from bookings where username='"+username+"'"
    cur.execute(query)
    result=cur.fetchall()
    pnr=[]
    for row in result:
        pnr.append(row[0])
    for i in pnr:
        PNRStatus(i)
        print()
    con.close()
    
