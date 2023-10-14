import mysql.connector as mycon
import csv
import pickle
import os

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
                return True
            else:
                print("PASSWORD DOESN'T MATCH")
                return False
    else:
        print("USER NOT FOUND.\nPLEASE CHECK YOUR USERNAME AS IT MAY BE WRONG\nELSE YOU NEED TO SIGN UP AS A NEW USER.")
        return False
    




def AdminLogin():
    username=input("Enter admin username : ")
    password=input("Enter admin password : ")
    if username=="admin" and password=="login@Admin":       # admin username = "admin" & password = "login@Admin"
        return True
    else:
        print("INVALID LOGIN CREDENTIALS")
        return False
    



def AddStation():
    f=open("D:\\Projects\\Computer\\Class 12\\File Handling\\Stations.dat","ab+")
    f.close()
    f=open("D:\\Projects\\Computer\\Class 12\\File Handling\\Stations.dat","rb")
    data=pickle.load(f)
    station_code=input("Enter station code : ")
    station_name=input("Enter station name : ")
    data[station_code]=station_name
    f.close()
    f=open("D:\\Projects\\Computer\\Class 12\\File Handling\\Stations.dat","wb")
    pickle.dump(data,f)
    print("Station added successfully")
    f.close()




def DeleteStation():
    pass




def AddTrain():
    # Adding data to csv file
    f=open("D:\\Projects\\Computer\\Class 12\\File Handling\\Trains.csv","a+")
    f.close()
    f=open("D:\\Projects\\Computer\\Class 12\\File Handling\\Trains.csv","a")
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
    
    




def ModifyTrain():
    pass





def DeleteTrain():
    pass





def BookingDetails():
    con = mycon.connect(
        host='localhost',
        user='root',
        password='password',
        port=3306,
        database='railway_system'
    )
    cur = con.cursor()
    cur.execute('select * from bookings')
    result=cur.fetchall()
    print("%10s"%"PNR",
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
        print(
            "%10s"%row[0],
            "%8s"%row[1],
            "%5s"%row[2],
            "%8s"%row[3],
            "%11s"%row[4],
            "%3s"%row[5],
            "%12s"%row[6],
            "%12s"%row[7],
            "%7s"%row[8]
            )
    con.close()




def BookTicket():
    pass




def CancelTicket():
    pass




def PNRStatus():
    pass




def MyBookings():
    pass