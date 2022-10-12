from django.shortcuts import render, redirect

from .models import Master, Employee, Department,CURRENT_User
from .forms import EmployeeForm
import secrets
import string
from django.contrib.auth import authenticate
from django.contrib import messages
from django.core.paginator import Paginator

from django.http import  JsonResponse

ID_NUM = 10


# insert data randomly
def insertEmployee():
    import pandas as pd
    import random
    # from models import Department, Employee


    data = pd.read_csv("./account/MOCK_DATA.csv")

    for i in range(data.shape[0]):
        row = data.loc[i]
        name = dict(row)['name']
        address = row.address
        dept = row.Department
        salary = random.randint(1000, 43000)
        id = ''.join(secrets.choice(string.ascii_letters) for x in range(ID_NUM))
        #
        if Department.objects.filter(department = dept).exists():
            dept_obj = Department.objects.filter(department=dept)[0]
        else:
            dept_obj = Department(department=dept, id=''.join(secrets.choice(string.ascii_letters) for x in range(ID_NUM)))
            dept_obj.save()

        #save the data
        obj = Employee(name=name, salary=salary, address=address, emp_id=id, emp_department=dept_obj)
        obj.save()

# UNCOMMENT TO SAVE THEM.
# insertEmployee()



# set session to None
# request.session['user_id'] = None

# password functions
import bcrypt
import re

def generate_password_hash(user_password):
    encoded_password = user_password.encode('utf-8')
    hashed_password = bcrypt.hashpw(encoded_password, bcrypt.gensalt())
    app_regex = re.compile("b*'")
    encoding_removed = app_regex.sub("",str(hashed_password))
    return encoding_removed

def check_password_match(user_password, hashed_password):
    encoded_password = user_password.encode('utf-8')
    encoded_hashed_password = hashed_password.encode('utf-8')
    if bcrypt.checkpw(encoded_password, encoded_hashed_password):
        return True
    else:
        return False



def getPages(request, OBJECT, pageNum):
    p = Paginator(OBJECT, pageNum)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    return page_obj


def home(request):
    local = "127.0.0.1:8000/"
    res ={
    "title": "Here are paths for the application",
    "paths":{
    "Home page":f"{local}",
    "login Page":"{local}login/",
    "Sinup Page":"{local}signup/",

    "Master Home Page":"{local}mater/",
    "Master Edit data Page":"{local}mater/edit/<id>/",
    "Master Updated data Page":"{local}mater/update/<id>/",
    "Master Delete data  Page":"{local}mater/delete/<id>/",


    "Employee Home Page":"{local}emp/",
    "Department  Page":"{local}dept/",
    "Employee Edit data Page":"{local}emp/edit/<id>/",
    "Employee Updated data Page":"{local}emp/update/<id>/",
    "Employee Delete data  Page":"{local}emp/delete/<id>/",

    }
    }

    return JsonResponse(res)
def signup(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        phone = request.POST['phone']
        if CURRENT_User.objects.filter(username = username).exists() or CURRENT_User.objects.filter(email = email).exists():
            messages.info(request, "Such User ALready Exists; Change username or email")
            return redirect("/signup/")
        user = CURRENT_User(name= name, username=username, password=generate_password_hash(password), phone=phone, email=email)

        user.save()
        request.session['user_id'] = user.id
        messages.success(request, 'User Regstered!')
        return redirect("/emp/")



    return render(request, "./account/signup.html")

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = CURRENT_User.objects.filter(username = username)
        if user.exists():
            #user = authenticate(username=username, password=password)
            if check_password_match(password, user[0].password):
                print(user[0].password)
                messages.success(request, 'Your Login  successfully!')
                print("User Authenticated")
                request.session['user_id'] = user[0].id
                return redirect("/emp/")
            else:
                messages.warning(request, 'Incorrect Details for Login!')
                print("Not yet Authenticated:  ")
                return redirect("/login/")
        else:
            user = None
            messages.error(request, 'No such user.!')
            return redirect("/login/")


    return render(request, "./account/login.html")


def saveMater(request):
    data = Master.objects.all()
    if request.method =="POST":
        status = request.POST['status']
        inital = request.POST['inital']
        id = ''.join(secrets.choice(string.ascii_letters) for x in range(ID_NUM))
        if "" in [status, inital]:
            messages.warning(request, 'Ensure all fields has data!')
            print("{Some are empty}:  No data to be saved")
        else:
            save_data = Master(initial = inital, status=status, id=id)

            try:
                save_data.save()
                messages.success(request, 'Master  Details saved well!')
                print("saved")
            except Exception as e:
                messages.warning(request, f'An error occured {e}!')
                print(f"Error  {e}")
            print(f"Data are {status} and {inital}")
    data = getPages(request, data,4)
    return render(request,'./account/index.html',{'data':data})

def editMater(request, id):
    obj = Master.objects.get(id = id)
    return render(request,'./account/edit_mater.html', {'obj':obj})


def updateMater(request, id):
    obj = Master.objects.get(id = id)
    if request.method == "POST":
        status = request.POST['status']
        inital = request.POST['inital']
        if "" not in [status, inital]:
            print("Updating contents")
            obj.status= status
            obj.initial = inital
            obj.save()
            messages.success(request, 'Updated  Details well!')
            return redirect("/mater/")
        else:
            messages.warning(request, 'Unable to update Deatils!')

    else:
        return render(request,'./account/edit_mater.html', {'obj':obj})




def destroy(request, id):
    if request.session.get('user_id', None):
        obj = Master.objects.get(id = id)
        obj.delete()
        messages.warning(request, 'Deatils Deleted!')
    else:
        messages.warning(request, "Only Logged User can delete A field")
    return redirect("/mater/")



# department

def addDept(request):

    data = Employee.objects.all()
    dept_obj = Department.objects.all()
    if request.method == "POST":
        dept = request.POST['department']
        if Department.objects.filter(department=dept):
            messages.warning(request, 'Such Department ALready Exists!')
            return redirect("/dept/")
            #return "ALready found"
        else:
            obj = Department(department=dept, id=''.join(secrets.choice(string.ascii_letters) for x in range(ID_NUM)))
            obj.save()
            messages.success(request, 'A department has beem added!')
            print("saved ")

    print(dept_obj)
    return render(request,'./account/emp_index.html',{"data":data, "dept_obj":dept_obj})


# Employee
def saveEmp(request):
    data = Employee.objects.all()
    dept_obj = Department.objects.all()
    if request.method == "POST":
        name = request.POST['name']
        salary = request.POST['salary']
        address = request.POST['address']
        try:
            department = Department.objects.get(department = request.POST['department'])
        except Exception as e:
            messages.warning(request, 'No department with siuch Details!')
            return render(request,'./account/emp_index.html',{ "data":data, "dept_obj":dept_obj})
        else:
            id =''.join(secrets.choice(string.ascii_letters) for x in range(ID_NUM))
            obj = Employee(name=name, salary=salary, address=address, emp_id=id, emp_department=department)
        try:
            obj.save()
            messages.success(request, 'Saved New Employee!')
            return redirect('/emp/')
        except:
            pass
    data = getPages(request, data,4)
    return render(request,'./account/emp_index.html',{ "data":data, "dept_obj":dept_obj})


def empEdit(request, id):
    dept_obj = Department.objects.all()
    employee = Employee.objects.get(emp_id = id)
    return render(request,'./account/emp_edit.html', {'employee':employee, "dept_obj":dept_obj})



def empUpdate(request, id):
    print("Update Emp")
    employee = Employee.objects.get(emp_id = id)
    data = Employee.objects.all()
    dept_obj = Department.objects.all()
    if request.method =="POST":
        name = request.POST['name']
        salary = request.POST['salary']
        address = request.POST['address']
        try:
            department = Department.objects.get(department = request.POST['department'])
        except Exception as e:
            messages.warning(request, 'Unable to update!')
            pass
        else:
            employee.name = name
            employee.salary = salary
            employee.address = address
            employee.emp_department = department

            employee.save()
            messages.success(request, 'Updated Employee Details!')
            print("Updated Employee")
            return redirect("/emp/")
            #return render(request,'./account/emp_index.html',{ "data":data, "dept_obj":dept_obj})

    return render(request,'./account/emp_edit.html', {'employee':employee, "dept_obj":dept_obj})



def empDestroy(request, id):
    if request.session.get('user_id', None):
        employee = Employee.objects.get(emp_id = id)
        employee.delete()
        messages.warning(request, 'Deleted details for employee!')
    else:
        messages.warning(request, "Only Logged User can delete A field")
    return redirect("/emp/")
