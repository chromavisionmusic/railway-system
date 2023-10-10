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
choice=None
while choice!=0:
    choice=int(input("""
                     1. SIGN UP\n
                     2. SIGN IN\n
                     3. ADMIN LOGIN\n
                     0. EXIT\n\n
                     Please enter your choice : 
                     """))
    
    if choice==0:       # Exit the program
        print("THANK YOU FOR USING e-Train Reservation System")
    elif choice==1:     # Proceed to Sign Up page
        F.SignUp()
    elif choice==2:     # Proceed to Sign In page
        sign_in=F.SignIn()
    elif choice==3:
        pass
    else:
        print("INVALID CHOICE")
