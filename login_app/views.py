from django.shortcuts import render, redirect
from requests import request
from login_app.models import Register_user
from django.contrib import messages
from django.http import HttpResponse
import datetime
import re
import json
import mysql.connector


# Create your views here.

# Get username details from user and authenticate with Stored details
def login(request):
    if request.method == "POST":
        user = Register_user()
        user.username = request.POST.get('username')
        user.pwd = request.POST.get('password')
        
        if user.username != None:
            # if input details matches with stored details Login successfull
            if authentication(user.username, user.pwd) == 'True':
                #print(user.username)
                messages.success(request,f' {user.username} !!')
                return render(request, 'profile.html')
                
                
            else:
                messages.info(request, f"Username or Password doesn\'t match")
                return render(request, 'login.html')
    else:
        return render(request, 'login.html')


# Signup new user by checking username doesn't exist
def Signup(request):
    if request.method == "POST":
        if request.POST.get('username') and request.POST.get('pwd') or request.POST.get('pwd_date') or request.POST.get('pwd_strength'):
            save_user = Register_user()
            save_user.username = request.POST.get('username') 
            save_user.pwd = request.POST.get('pwd')
            if save_user.pwd != None:
                if Repeat(save_user.username) == 'True':
                    messages.info(request, f"Username already exist")
                    return render(request,'signup.html')
                else:
                    pass
            
            save_user.pwd_strength = Strength(save_user.pwd) 
            save_user.pwd_date = datetime.date.today()
            save_user.save()
            messages.success(request,"Signup Successfull!")
            return render(request,'signup.html')
         
    else:
        return render(request,'signup.html')


# check user's password strength and store in Database.
def Strength(password):
    if len(password)>=8:
        if re.findall("[a-z]", password):
            if re.findall("[A-Z]", password):
                if re.findall("[0-9]", password):
                    if re.findall('[!"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~]', password):
                        # print("Strong Password")
                        return "Strong"
                    else:
                        # print("NO Special Characters")
                        return "Weak"

                else:
                    # print("NO digit")
                    return "Weak"    
            else:
                # print("NO upper")
                return "Weak" 
        else:
            # print("NO lower")
            return "Weak" 
    else:
        # print("Len < 8")
        return "Weak"  


# Check if username exist in database
def Repeat(name):
    connection = mysql.connector.connect(host='127.0.0.1',database='user_details',user='root',password='')
    username = "select username from user_data"
    c_name = connection.cursor()
    c_name.execute(username)
    names = c_name.fetchall()
    usernames = json.dumps(names)
    
    #print(f"present_name:{name} names:{usernames}")
    if name in usernames :
        # username already exist can't register
        return "True"
        
    else:
        # register user
        return "False"
    

# match user input with stored data
def authentication(name, password):
    connection = mysql.connector.connect(host='127.0.0.1',database='user_details',user='root',password='')
    sql_select_Password = "select pwd from user_data WHERE username = %s ORDER BY userid DESC LIMIT 1"
    username = "select username from user_data"
    c_name = connection.cursor()
    c_name.execute(username)
    names = c_name.fetchall()
    usernames = json.dumps(names)

    cursor_password = connection.cursor()
    cursor_password.execute(sql_select_Password, (name,))
    
    records = cursor_password.fetchall()
    last_password = json.dumps(records)

   
    
    rows = len(names)
    columns = len(names[0])
    match_names = []

    for i in range(rows):
        for j in range(columns):
            match_names.append(names[i][j])

    #print(f"present_names:{names} usernames:{match_names} \n and passowd is: {password} Last passwords-0:{last_password}")
    if name in match_names and password in last_password:
        return "True"
    else:
        return "False"
    

# Changing user password and making sure new password is not same as last 5 passwords 
def change_password(request):
    if request.method == "POST":
        if request.POST.get('username') and request.POST.get('pwd') or request.POST.get('pwd_date') or request.POST.get('pwd_strength'):
            save_user = Register_user()
            save_user.username = request.POST.get('username') 
            save_user.pwd = request.POST.get('pwd')
            if save_user.pwd != None:
                if check_pwd(save_user.username, save_user.pwd) == 'True':
                    messages.info(request, f"Password is same as last 5 passwords")
                    return render(request,'changePWD.html')
                else:
                    pass
            
            save_user.pwd_strength = Strength(save_user.pwd) 
            save_user.pwd_date = datetime.date.today()
            save_user.save()
            messages.success(request,"Password Change Successfull!")
            return render(request,'changePWD.html')
       
           
    else:
        return render(request,'changePWD.html')


def check_pwd(name, password):
    connection = mysql.connector.connect(host='127.0.0.1',database='user_details',user='root',password='')
    # Getting user's last 5 passwords by USERNAME
    sql_select_Password = "select username, pwd from user_data WHERE username = %s ORDER BY userid DESC LIMIT 5"
    username = "select username from user_data"

    cursor_password = connection.cursor()
    cursor_password.execute(sql_select_Password, (name,))
    
    records = cursor_password.fetchall()
    last_5_passwords = json.dumps(records)
   
    #print(f"present_name:{name} names:{usernames} \n and Last 5 passwords:{last_5_passwords}")
    if password in last_5_passwords :
        # can't change password
        return "True"
        
    else:
        # password change successfull
        return "False"


