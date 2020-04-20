from django.shortcuts import render
from .models import Employee
from django.http import HttpResponse
import pandas as pd
import datetime
from .models import Document
def index(request):
    months={1:"January",2:"February",3:"March",4:"April",5:"May",6:"June",7:"July",8:"August",9:"September",10:"October"
            ,11:"November",12:"December"}
    employees=Employee.objects.all()
    documents=Document.objects.all()
    print(documents)
    print(employees)
    doc=Document.objects.get(monthnumber=1)
    params={'employee':employees,'Document':doc,'month':months[1]}
    return render(request,'analysis/index.html',params)
def about(request):
    return render(request,'analysis/about.html')

def chosen(request,id):
    id=str(id)
    year=id[:4]
    month=id[4:]
    m=int(month)
    yr=int(year)
    documents=Document.objects.get(monthnumber=m,year=yr)
    months = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August",
              9: "September", 10: "October"
        , 11: "November", 12: "December"}
    employees = Employee.objects.all()
    params={}
    params['employee']=employees
    params['Document']=documents
    params['month']=months[m]
    s=months[m]+str(yr)
    params['name']=s

    print(documents)

    return render(request,'analysis/index2.html',params)


def chose(request):
    documents = Document.objects.all()
    n=len(documents)
    months = ["January","February","March","April","May","June","July","August","September","October"
        , "November","December"]
    params={'documents':documents,'number':n,'range':range(n),'months':months}
    return render(request,'analysis/chose.html',params)

def search(request):
    query=request.GET.get('search')

    emp=Employee.objects.get(employee_name=query).employee_position
    print(emp)


    return HttpResponse(request,"Search")

def employeem(request,id,m):
    m = str(m)
    year = m[:4]
    month = m[4:]
    m = int(month)
    yr = int(year)
    months = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August",
              9: "September", 10: "October"
        , 11: "November", 12: "December"}
    name=""
    name+=months[m]
    name+=str(yr)
    name+=".xlsx"
    link="./media/analysis/files/"
    link+=name
    df = pd.read_excel(link)
    df['InTime'] = df['InTime'].fillna("00:00:00")
    df['OutTime'] = df['OutTime'].fillna("00:00:00")
    df['ODINTime'] = df['ODINTime'].fillna("00:00:00")
    df['ODOutTime'] = df['ODOutTime'].fillna("00:00:00")
    df['Leave'] = df['Leave'].fillna("N")
    df['INTimestamp'] = df["Date"].astype(str) + " " + df["InTime"].astype(str)
    df['OutTimestamp'] = df["Date"].astype(str) + " " + df["OutTime"].astype(str)
    df['ODINTimestamp'] = df["Date"].astype(str) + " " + df["ODINTime"].astype(str)
    df['ODOutTimestamp'] = df["Date"].astype(str) + " " + df["ODOutTime"].astype(str)
    emp_count = df['EmployeeID'].nunique()
    days = df['Date'].nunique()
    loop_count = emp_count * days

    l = []
    odleave = []
    leaves = {}

    for i in range(0, loop_count):
        intime = datetime.datetime.strptime(df["INTimestamp"][i], '%Y-%m-%d %H:%M:%S')
        outtime = datetime.datetime.strptime(df["OutTimestamp"][i], '%Y-%m-%d %H:%M:%S')
        odintime = datetime.datetime.strptime(df["ODINTimestamp"][i], '%Y-%m-%d %H:%M:%S')
        odouttime = datetime.datetime.strptime(df["ODOutTimestamp"][i], '%Y-%m-%d %H:%M:%S')

        total_out = (outtime.hour * 60 + outtime.minute)
        total_int = (intime.hour * 60 + intime.minute)
        total_od_out = (odouttime.hour * 60 + odouttime.minute)
        total_od_int = (odintime.hour * 60 + odintime.minute)
        od_leave_time = (total_od_int - total_od_out) / 60
        od_leave_time=float("%.2f" % round(od_leave_time,2))
        working_time = (total_out - total_int) / 60
        working_time = float("%.2f" % round(working_time, 2))
        l.append(working_time)
        odleave.append(od_leave_time)
        # print(intime,outtime,sep=" ")
    df['Working_time'] = l
    df['ODLeave'] = odleave

    grp_weekdays = df.groupby(['EmployeeID', 'Day']).mean()
    grp_total_working_time = df.groupby(['EmployeeID']).sum()

    # print(df)
    df11 = df.groupby('EmployeeID')['Leave'].apply(lambda x: (x == 'C').sum()).reset_index(name='Casualleavecount')
    df12 = df.groupby('EmployeeID')['Leave'].apply(lambda x: (x == 'M').sum()).reset_index(name='Medicalleavecount')
    df13 = df.groupby('EmployeeID')['Leave'].apply(lambda x: (x == 'OD').sum()).reset_index(name='ODleavecount')
    params={}
    medical= list(df12[df12['EmployeeID']==id]['Medicalleavecount'])[0]
    casual = list(df11[df11['EmployeeID'] == id]['Casualleavecount'])[0]
    odleave = list(df13[df13['EmployeeID'] == id]['ODleavecount'])[0]
    total_leaves=medical+casual+odleave
    gc = df.groupby(['EmployeeID', 'Day']).agg({'Working_time': ['mean']})
    gc.columns = ['Average_working_hrs']
    gc = gc.reset_index()
    gday = gc[gc['EmployeeID'] == id]
    monday = list(gday[gday['Day'] == 'Monday']['Average_working_hrs'])[0]
    monday = float("%.2f" % round(monday, 2))
    tuesday = list(gday[gday['Day'] == 'Tuesday']['Average_working_hrs'])[0]
    tuesday = float("%.2f" % round(tuesday, 2))
    wednesday =list(gday[gday['Day'] == 'Wednesday']['Average_working_hrs'])[0]
    wednesday = float("%.2f" % round(wednesday, 2))
    thursday = list(gday[gday['Day'] == 'Thursday']['Average_working_hrs'])[0]
    thursday = float("%.2f" % round(thursday, 2))
    friday = list(gday[gday['Day'] == 'Friday']['Average_working_hrs'])[0]
    friday = float("%.2f" % round(friday, 2))
    saturday = list(gday[gday['Day'] == 'Saturday']['Average_working_hrs'])[0]
    saturday = float("%.2f" % round(saturday, 2))
    l1=(list(df[df['EmployeeID'] == id]['Working_time']))
    g = df.groupby('EmployeeID')
    gp = g.get_group(id)
    gsum = gp.sum()
    totalworking=(gsum['Working_time'])
    totalworking = float("%.2f" % round(totalworking, 2))
    totalodleave=(gsum['ODLeave'])
    dates = (list(df[df['EmployeeID'] == id]['Date']))
    date = []
    for d in dates:
        s = str(d)
        s = s[8:10]
        date.append(s)


    emp = Employee.objects.get(employee_id=id)
    empid=emp.employee_id
    empname=emp.employee_name
    empposition=emp.employee_position
    empemail=emp.employee_email
    empcontact=emp.employee_contact
    empimage=emp.employee_image
    print(empimage)

    params['monthyr']=months[m]+" "+str(yr)
    params[emp]=emp
    params['empid']=empid
    params['empname']=empname
    params['empposition']=empposition
    params['empemail']=empemail
    params['empcontact']=empcontact
    params['empimage']=empimage


    params['totalleaves']=total_leaves
    params['medical']=medical
    params['casual']=casual
    params['odleave']=odleave
    print(odleave)
    all_leaves=[medical,casual,odleave]
    params['all_leaves']=all_leaves

    params['monday']=monday
    params['tuesday']=tuesday
    params['wednesday']=wednesday
    params['thursday']=thursday
    params['friday']=friday
    params['saturday']=saturday
    params['monthlyworking']=l1
    params['date']=date
    params['range']=range(len(l1))
    params['totalworking']=totalworking
    params['totalodleave']=totalodleave

    params['emp']=emp
    print("printing dates and work ")
    print(date)
    print(l1)

    days=""
    for i in date:
        days+=str(i)
        days+=","
    days=days[:-1]
    params["days"] = days
    work=""
    for i in l1:
        work+=str(i)
        work+=","
    work=work[:-1]
    params["w1"]=8.3
    params["w2"]=9.3
    params["w3"]=7.3
    params["work"]=work

    return render(request, 'analysis/employee.html',params)
def employee(request,id):

    months = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August",
              9: "September", 10: "October"
        , 11: "November", 12: "December"}
    name=""
    name+=months[1]
    name+=str(2020)
    name+=".xlsx"
    link="./media/analysis/files/"
    link+=name
    df = pd.read_excel(link)
    df['InTime'] = df['InTime'].fillna("00:00:00")
    df['OutTime'] = df['OutTime'].fillna("00:00:00")
    df['ODINTime'] = df['ODINTime'].fillna("00:00:00")
    df['ODOutTime'] = df['ODOutTime'].fillna("00:00:00")
    df['Leave'] = df['Leave'].fillna("N")
    df['INTimestamp'] = df["Date"].astype(str) + " " + df["InTime"].astype(str)
    df['OutTimestamp'] = df["Date"].astype(str) + " " + df["OutTime"].astype(str)
    df['ODINTimestamp'] = df["Date"].astype(str) + " " + df["ODINTime"].astype(str)
    df['ODOutTimestamp'] = df["Date"].astype(str) + " " + df["ODOutTime"].astype(str)
    emp_count = df['EmployeeID'].nunique()
    days = df['Date'].nunique()
    loop_count = emp_count * days

    l = []
    odleave = []
    leaves = {}

    for i in range(0, loop_count):
        intime = datetime.datetime.strptime(df["INTimestamp"][i], '%Y-%m-%d %H:%M:%S')
        outtime = datetime.datetime.strptime(df["OutTimestamp"][i], '%Y-%m-%d %H:%M:%S')
        odintime = datetime.datetime.strptime(df["ODINTimestamp"][i], '%Y-%m-%d %H:%M:%S')
        odouttime = datetime.datetime.strptime(df["ODOutTimestamp"][i], '%Y-%m-%d %H:%M:%S')

        total_out = (outtime.hour * 60 + outtime.minute)
        total_int = (intime.hour * 60 + intime.minute)
        total_od_out = (odouttime.hour * 60 + odouttime.minute)
        total_od_int = (odintime.hour * 60 + odintime.minute)
        od_leave_time = (total_od_int - total_od_out) / 60
        od_leave_time=float("%.2f" % round(od_leave_time,2))
        working_time = (total_out - total_int) / 60
        working_time = float("%.2f" % round(working_time, 2))
        l.append(working_time)
        odleave.append(od_leave_time)
        # print(intime,outtime,sep=" ")
    df['Working_time'] = l
    df['ODLeave'] = odleave

    grp_weekdays = df.groupby(['EmployeeID', 'Day']).mean()
    grp_total_working_time = df.groupby(['EmployeeID']).sum()

    # print(df)
    df11 = df.groupby('EmployeeID')['Leave'].apply(lambda x: (x == 'C').sum()).reset_index(name='Casualleavecount')
    df12 = df.groupby('EmployeeID')['Leave'].apply(lambda x: (x == 'M').sum()).reset_index(name='Medicalleavecount')
    df13 = df.groupby('EmployeeID')['Leave'].apply(lambda x: (x == 'OD').sum()).reset_index(name='ODleavecount')
    params={}
    medical= list(df12[df12['EmployeeID']==id]['Medicalleavecount'])[0]
    casual = list(df11[df11['EmployeeID'] == id]['Casualleavecount'])[0]
    odleave = list(df13[df13['EmployeeID'] == id]['ODleavecount'])[0]
    total_leaves=medical+casual+odleave
    gc = df.groupby(['EmployeeID', 'Day']).agg({'Working_time': ['mean']})
    gc.columns = ['Average_working_hrs']
    gc = gc.reset_index()
    gday = gc[gc['EmployeeID'] == id]
    monday = list(gday[gday['Day'] == 'Monday']['Average_working_hrs'])[0]
    monday = float("%.2f" % round(monday, 2))
    tuesday = list(gday[gday['Day'] == 'Tuesday']['Average_working_hrs'])[0]
    tuesday = float("%.2f" % round(tuesday, 2))
    wednesday =list(gday[gday['Day'] == 'Wednesday']['Average_working_hrs'])[0]
    wednesday = float("%.2f" % round(wednesday, 2))
    thursday = list(gday[gday['Day'] == 'Thursday']['Average_working_hrs'])[0]
    thursday = float("%.2f" % round(thursday, 2))
    friday = list(gday[gday['Day'] == 'Friday']['Average_working_hrs'])[0]
    friday = float("%.2f" % round(friday, 2))
    saturday = list(gday[gday['Day'] == 'Saturday']['Average_working_hrs'])[0]
    saturday = float("%.2f" % round(saturday, 2))
    l1=(list(df[df['EmployeeID'] == id]['Working_time']))
    g = df.groupby('EmployeeID')
    gp = g.get_group(id)
    gsum = gp.sum()
    totalworking=(gsum['Working_time'])
    totalworking = float("%.2f" % round(totalworking, 2))
    totalodleave=(gsum['ODLeave'])
    dates = (list(df[df['EmployeeID'] == id]['Date']))
    date = []
    for d in dates:
        s = str(d)
        s = s[8:10]
        date.append(s)


    emp = Employee.objects.get(employee_id=id)
    empid=emp.employee_id
    empname=emp.employee_name
    empposition=emp.employee_position
    empemail=emp.employee_email
    empcontact=emp.employee_contact
    empimage=emp.employee_image
    print(empimage)
    params[emp]=emp
    params['monthyr']=months[1]+" "+str(2020)
    params['empid']=empid
    params['empname']=empname
    params['empposition']=empposition
    params['empemail']=empemail
    params['empcontact']=empcontact
    params['empimage']=empimage


    params['totalleaves']=total_leaves
    params['medical']=medical
    params['casual']=casual
    params['odleave']=odleave
    print(odleave)
    all_leaves=[medical,casual,odleave]
    params['all_leaves']=all_leaves

    params['monday']=monday
    params['tuesday']=tuesday
    params['wednesday']=wednesday
    params['thursday']=thursday
    params['friday']=friday
    params['saturday']=saturday
    params['monthlyworking']=l1
    params['date']=date
    params['range']=range(len(l1))
    params['totalworking']=totalworking
    params['totalodleave']=totalodleave

    params['emp']=emp
    print("printing dates and work ")
    print(date)
    print(l1)

    days=""
    for i in date:
        days+=str(i)
        days+=","
    days=days[:-1]
    params["days"] = days
    work=""
    for i in l1:
        work+=str(i)
        work+=","
    work=work[:-1]
    params["w1"]=8.3
    params["w2"]=9.3
    params["w3"]=7.3
    params["work"]=work

    return render(request, 'analysis/employee.html',params)
