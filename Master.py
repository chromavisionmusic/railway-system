# Modules
import mysql.connector as mycon
import random
import Functions as F

# Variables
sign_in=False
admin_login=False

# Program
print("Welcome to e-Train Reservation System")
print()

# LOGIN PAGE
choice=None
while choice!=0:
    choice=int(input("1. SIGN UP\n2. SIGN IN\n3. ADMIN LOGIN\n0. EXIT\n\nPlease enter your choice : "))
    if choice==0:       # Exit the program
        print("THANK YOU FOR USING e-Train Reservation System")
    elif choice==1:     # Proceed to Sign Up page
        F.SignUp()
    elif choice==2:     # Proceed to Sign In page
        sign_in=F.SignIn()
    elif choice==3:
        admin_login=F.AdminLogin()
    else:
        print("Invalid Choice! Try Again.")

# ADMIN PAGE
if admin_login==True:
    choice=None
    while choice!=0:
        choice=int(input("1. ADD STATION\n2. DELETE STATION\n3. ADD TRAIN\n4.MODIFY TRAIN\n5.DELETE TRAIN\n6.SHOW ALL ACTIVE BOOKINGS\n0. LOGOUT\n\nPlease enter your choice : "))
        if choice==0:
            admin_login=False
            print("THANK YOU")
        elif choice==1:
            F.AddStation()
        elif choice==2:
            F.DeleteStation()
        elif choice==3:
            F.AddTrain()
        elif choice==4:
            F.ModifyTrain()
        elif choice==5:
            F.DeleteTrain()
        elif choice==6:
            F.BookingDetails()
        else:
            print("Invalid Choice! Try Again.")


# HOMEPAGE
if sign_in==True:
    choice=None
    while choice!=0:
        choice=int(input("1. BOOK TICKET\n2. CANCEL TICKET\n3. PNR STATUS\n4. MY BOOKINGS\n0. SIGN OUT\n\nPlease enter your choice : "))
        if choice==0:
            sign_in==False
            print("THANK YOU FOR USING e-Train Reservation System")
        elif choice==1:
            F.BookTicket()
        elif choice==2:
            F.CancelTicket()
        elif choice==3:
            F.PNRStatus()
        elif choice==4:
            F.MyBookings()
        else:
            print("Invalid Choice! Try Again.")