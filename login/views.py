from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.views.generic import View
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import connection
from preschool import validations
from preschool import views as PSviews
from .forms import UserForm
from preschool.validations import exists,validateEmail
# Create your views here.


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]		


def common(request):
	return render(request,'common.html')

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            with connection.cursor() as cursor :
                try:
                    print ("SELECT * FROM notice WHERE issued_to = '%s' order by notice_id desc " % (request.user.username) )
	            cursor.execute("SELECT * FROM notice WHERE issued_to = '%s' order by notice_id desc " % (request.user.username) )
	            Data = dictfetchall(cursor)
	            print Data
                    return render(request,"stud_detail.html",{'UserType':'Student','Data': Data[:10],'password_chage':True})
                except:
                    print "NO NOTICES"
                    return render(request,"stud_detail.html",{'UserType':'Student','password_fail':True})
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })

def student_login(request):
    
    print "Student logging in"
    if request.method == 'POST':	
        student_id = request.POST.get('StudentId')
        Password = request.POST.get('Password')
        user = authenticate(username=student_id, password=Password)
        if (user is not None) and exists(student_id,"student_id","student"):
            if user.is_active:
                login(request, user)
                with connection.cursor() as cursor :
                    try:
                        print ("SELECT * FROM notice WHERE issued_to = '%s' order by notice_id desc " % (student_id) )
	                cursor.execute("SELECT * FROM notice WHERE issued_to = '%s' order by notice_id desc " % (student_id) )
	                Data = dictfetchall(cursor)
	                print Data
                        return render(request,"stud_detail.html",{'UserType':'Student','Data': Data[:10]})
                    except:
                        print "NO NOTICES"
                        return render(request,"stud_detail.html",{'UserType':'Student'})
            else:
                return HttpResponse("Your account is disabled.")
        else:
            return render(request,"login.html",{'UserType':'Student','Invalid' : "Invalid login Details. Retry logging in !"})
    #elif (request.user.is_authenticated):
     #   with connection.cursor() as cursor :
      #      cursor.execute("SELECT * FROM notice WHERE issued_to = '%s' order by notice_id desc " % (request.user.username) )
	#    Data = dictfetchall(cursor)
	 #   print Data
          #  return render(request,"stud_detail.html",{'UserType':'Student','Data': Data[:10]})
    
    if ((request.user).is_authenticated) and exists(request.user.username,"student_id","student"):
         with connection.cursor() as cursor :
                    try:
                        print ("SELECT * FROM notice WHERE issued_to = '%s' order by notice_id desc " % (request.user.username) )
	                cursor.execute("SELECT * FROM notice WHERE issued_to = '%s' order by notice_id desc " % (request.user.username) )
	                Data = dictfetchall(cursor)
	                print Data
                        return render(request,"stud_detail.html",{'UserType':'Student','Data': Data[:10]})
                    except:
                        print "NO NOTICES"
                        return render(request,"stud_detail.html",{'UserType':'Student'})
    return render(request,"login.html",{'UserType':'Student'})



def teacher_profile(request):
    
    UserID = request.user.username
    if UserID[:2] != "te":
        return redirect(PSviews.homepage)
    with connection.cursor() as cursor :
	print ("SELECT * FROM teacher  WHERE teacher_id = '%s' " % (UserID) )
	cursor.execute("SELECT * FROM teacher  WHERE teacher_id = '%s' " % (UserID) )
	Data = dictfetchall(cursor)
	print Data
        print ("SELECT * FROM class  WHERE teacher_no = '%s' " % (UserID) )
	cursor.execute("SELECT * FROM class  WHERE teacher_no = '%s' " % (UserID) )
	Data2 = dictfetchall(cursor)
	print Data2
	return render(request,'teacher_profile.html',{'Data': Data,'Data2': Data2})

def staff_login(request):
    
    print "Staff logging in"
    if request.method == 'POST':	
        teacher_id = request.POST.get('TeacherId')
        Password = request.POST.get('Password')
        user = authenticate(username=teacher_id, password=Password)
        if (user is not None) and exists(teacher_id,"teacher_id","teacher"):
            if user.is_active:
                login(request, user)
                with connection.cursor() as cursor :
                    try:
                        #print ("SELECT * FROM notice WHERE issued_to = '%s' order by notice_id desc " % (student_id) )
	                #cursor.execute("SELECT * FROM notice WHERE issued_to = '%s' order by notice_id desc " % (student_id) )
	                #Data = dictfetchall(cursor)
	                #print Data
                        return render(request,"teacher.html",{'UserType':'Teacher'})
                    except:
                        #print "NO NOTICES"
                        return render(request,"teacher.html",{'UserType':'Teacher'})
            else:
                return HttpResponse("Your account is disabled.")
        else:
            return render(request,"login.html",{'UserType':'Teacher','Invalid' : "Invalid login Details. Retry logging in !"})

    if ((request.user).is_authenticated) and exists(request.user.username,"teacher_id","teacher"):
        return render(request,"teacher.html",{'UserType':'Teacher'})
    return render(request,"login.html",{'UserType':'Teacher'})


def admin_login(request):
    
    print "Admin logging in"
    if request.method == 'POST':	
        admin_id = request.POST.get('AdminId')
        Password = request.POST.get('Password')
        user = authenticate(username=admin_id, password=Password)
        if (user is not None):
            if user.is_active:
                login(request, user)
                with connection.cursor() as cursor :
                    try:
                        #print ("SELECT * FROM notice WHERE issued_to = '%s' order by notice_id desc " % (student_id) )
	                #cursor.execute("SELECT * FROM notice WHERE issued_to = '%s' order by notice_id desc " % (student_id) )
	                #Data = dictfetchall(cursor)
	                #print Data
                        return render(request,"admin.html",{'UserType':'Admin'})
                    except:
                        #print "NO NOTICES"
                        return render(request,"admin.html",{'UserType':'Admin'})
            else:
                return HttpResponse("Your account is disabled.")
        else:
            return render(request,"login.html",{'UserType':'Admin','Invalid' : "Invalid login Details. Retry logging in !"})

    
    return render(request,"login.html",{'UserType':'Admin'})

def student_detail(request):

    UserID = request.user.username
    if UserID[:2] != "st":
        return redirect(PSviews.homepage)
    with connection.cursor() as cursor :
	print ("SELECT * FROM student  WHERE student_id = '%s' " % (UserID) )
	cursor.execute("SELECT * FROM student  WHERE student_id = '%s' " % (UserID) )
	Data = dictfetchall(cursor)
	print Data
        print ("SELECT * FROM parent WHERE child= '%s';" % (UserID) )
	cursor.execute("SELECT * FROM parent WHERE child= '%s'" % (UserID) )
	Data2 = dictfetchall(cursor)
	print Data2
        print ("SELECT d.name,d.van_no,d.salary,d.dob,d.email_id,d.phone,d.address,d.joining_date,d.leaves_taken FROM driver as d,student as s WHERE s.student_id= '%s' and s.driver_no=d.driver_id;" % (UserID) )
	cursor.execute("SELECT d.name,d.van_no,d.salary,d.dob,d.email_id,d.phone,d.address,d.joining_date,d.leaves_taken FROM driver as d,student as s WHERE s.student_id= '%s' and s.driver_no=d.driver_id" % (UserID) )
	Data3 = dictfetchall(cursor)
	print Data3
	return render(request,'mydetails.html',{'Data2':Data2, 'Data': Data, 'Data3': Data3})








def academic_detail(request):

    UserID = request.user.username
    if UserID[:2] != "st":
        return redirect(PSviews.homepage)
    with connection.cursor() as cursor :
	print ("SELECT * FROM studies as s,subject as t  WHERE s.student_no = '%s' and s.subject_no=t.subject_id  " % (UserID) )
	cursor.execute("SELECT * FROM studies as s,subject as t  WHERE s.student_no = '%s' and s.subject_no=t.subject_id " % (UserID) )
	Data = dictfetchall(cursor)
	print Data
        print ("SELECT * FROM fees  WHERE payee = '%s' " % (UserID) )
	cursor.execute("SELECT * FROM fees  WHERE payee = '%s' " % (UserID) )
	Data1 = dictfetchall(cursor)
	print Data1
        
	return render(request,'academicdetails.html',{'Data': Data,"Data1":Data1})




def complaint_user(request):
    UserID = request.user.username
    if UserID[:2] != "te" and UserID[:2]!="st":
        return redirect(PSviews.homepage)
    if request.method == "POST":
        matter = request.POST['subject']
        date_of_issue = request.POST['date_of_issue']
        issuer = request.POST['issuer']

        with connection.cursor() as cursor :
            try:
	        print ("INSERT INTO complaint (matter,issuer,date_of_issue) values('%s','%s','%s') " % (matter,issuer,date_of_issue) )
	        cursor.execute("INSERT INTO complaint (matter,issuer,date_of_issue) values('%s','%s','%s') " % (matter,issuer,date_of_issue) )
	        if UserID[:2] == "st":
                    return render(request,'stud_detail.html',{'Submit': True})
	        elif UserID[:2] == "te":
                    return render(request,'teacher.html',{'Submit': True})
            except:
                print("Complaint not registered")
	        if UserID[:2] == "st":
                    return render(request,'stud_detail.html',{'Error': True})
	        elif UserID[:2] == "te":
                    return render(request,'teacher.html',{'Error': True})

    if UserID[:2] == "st":
        return render(request, 'complaint_form.html')
    elif UserID[:2] == "te":
        return render(request,'complaint_teacher.html')

def send_notice(request):
    UserID = request.user.username
    if UserID[:2] == "st":
        return redirect(PSviews.homepage)
    if request.method == "POST":
        matter = request.POST['matter']
        date_of_issue = request.POST['date_of_issue']
        issued_to = request.POST['issued_to']

        with connection.cursor() as cursor :
            try:
	        print ("INSERT INTO notice (matter,issued_to,date_of_issue) values('%s','%s','%s') " % (matter,issued_to,date_of_issue) )
	        cursor.execute("INSERT INTO notice (matter,issued_to,date_of_issue) values('%s','%s','%s') " % (matter,issued_to,date_of_issue) )
	        if UserID[:2] == "te":
                    return render(request,'teacher.html',{'Submit3': True})
                return render(request,'admin.html',{'Submit3': True})
            except:
                print("Notice not registered")
	        if UserID[:2] == "te":
                    return render(request,'teacher.html',{'Error3': True})
                return render(request,'admin.html',{'Error3': True})
    if UserID[:2] == "te":
        return render(request, 'send_notice.html')
    with connection.cursor() as cursor :
        print ("select * from notice" )
	cursor.execute("select * from notice" )
        Data = dictfetchall(cursor)
	print Data
	return render(request,'send_notice2.html',{'Data':Data,'Submit2': True})

def add_marks(request):
    UserID = request.user.username
    if UserID[:2] != "te":
        return redirect(PSviews.homepage)
    if request.method == "POST":
        student_no = request.POST['student_no']
        subject_no = request.POST['subject_no']
        half_yearly_marks = request.POST['half_yearly_marks']
        final_marks = request.POST['final_marks']

        with connection.cursor() as cursor :
            try:
	        print ("INSERT INTO studies values('%s','%s','%s','%s') " % (student_no,subject_no,half_yearly_marks,final_marks) )
	        cursor.execute("INSERT INTO studies values('%s','%s','%s','%s') " % (student_no,subject_no,half_yearly_marks,final_marks) )
	        return render(request,'teacher.html',{'Submit1': True})
            except:
                print("Marks not registered")
                return render(request,'teacher.html',{'Error1': True})

    with connection.cursor() as cursor :
        print ("select st.student_no,st.subject_no,st.half_yearly_marks,st.final_marks,s.name from studies as st,student as s where s.student_id=st.student_no" )
	cursor.execute("select st.student_no,st.subject_no,st.half_yearly_marks,st.final_marks,s.name,su.title from studies as st,class as c,student as s,subject as su where s.student_id=st.student_no and st.subject_no=su.subject_id and c.class_id= s.class_no and c.teacher_no='%s'" %(UserID) )
        Data = dictfetchall(cursor)
	print Data
	return render(request,'add_marks.html',{'Data':Data,'Submit2': True})

def modify_marks(request):
    UserID = request.user.username
    if UserID[:2] != "te":
        return redirect(PSviews.homepage)
    if request.method == "POST":
        student_no = request.POST['student_no']
        subject_no = request.POST['subject_no']
        half_yearly_marks = request.POST['half_yearly_marks']
        final_marks = request.POST['final_marks']

        with connection.cursor() as cursor :
            try:
	        print ("update studies set half_yearly_marks='%s' and final_marks='%s' where student_no='%s' and subject_no='%s'" % (half_yearly_marks,final_marks,student_no,subject_no) )
	        cursor.execute ("update studies set half_yearly_marks='%s',final_marks='%s' where student_no='%s' and subject_no='%s'" % (half_yearly_marks,final_marks,student_no,subject_no) )
	        return render(request,'teacher.html',{'Submit2': True})
            except:
                print("Marks not modified")
                return render(request,'teacher.html',{'Error2': True})

    return render(request, 'modify_marks.html')

def logout_user(request):
    print("logging out")
    username=request.user.username
    if username[:2] =="te":
        UserType='Teacher'
    elif username[:2] =='st':
        UserType='Student'
    else:
        UserType='Admin'
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,'UserType': UserType,
    }
    return render(request, 'login.html', context)

def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        print("form saved")
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        print ("registered user")
        return render(request, 'admin.html', {'form':form,'reg':True})    
    return render(request, 'admin.html', {'form':form,'error':True})



def register_student(request):
    UserID = request.user.username
    if UserID[:2] == "te" or UserID[:2] =="st":
        return redirect(PSviews.homepage)
    if request.method == "POST":
        student_id = request.POST['student_id']
        dob = request.POST['date_of_birth']
        name = request.POST['name']
        percentage = request.POST['percentage']
        attendance = request.POST['attendance']
        driver_no = request.POST['driver_no']
        class_no = request.POST['class_no']
        rollno = request.POST['rollno']
        year = request.POST['year']

        with connection.cursor() as cursor :
            try:
	        print ("INSERT INTO student values ('%s','%s','%s','%s','%s','%s','%s','%s','%s') " % (student_id,rollno,name,dob,percentage,attendance,driver_no,class_no,year) )
	        cursor.execute("INSERT INTO student values ('%s','%s','%s','%s','%s','%s','%s','%s','%s') " % (student_id,rollno,name,dob,percentage,attendance,driver_no,class_no,year) )
	        return render(request,'register.html',{'Submit1': True})
            except:
                print("Student not registered")
	        return render(request,'admin.html',{'Error1': True})
    with connection.cursor() as cursor :
        print ("select s.student_id,s.rollno,s.name,s.dob,s.percentage,s.attendance,s.driver_no,s.class_no,s.year from student as s,auth_user as a where a.username=s.student_id " )
	cursor.execute("select s.student_id,s.rollno,s.name,s.dob,s.percentage,s.attendance,s.driver_no,s.class_no,s.year from student as s,auth_user as a where a.username=s.student_id " )
        Data = dictfetchall(cursor)
	print Data
	return render(request,'register_student.html',{'Data':Data,'Submit1': True})
    


def modify_student(request):
    UserID = request.user.username
    if UserID[:2] == "te" or UserID[:2] =="st":
        return redirect(PSviews.homepage)
    if request.method == "POST":
        student_id = request.POST['student_id']
        dob = request.POST['date_of_birth']
        name = request.POST['name']
        percentage = request.POST['percentage']
        attendance = request.POST['attendance']
        driver_no = request.POST['driver_no']
        class_no = request.POST['class_no']
        rollno = request.POST['rollno']
        year = request.POST['year']

        with connection.cursor() as cursor :
            try:
	        print ("update student set rollno='%s', name='%s',dob='%s',percentage='%s',attendance='%s',driver_no='%s',class_no='%s',year='%s' where student_id='%s'" % (rollno,name,dob,percentage,attendance,driver_no,class_no,year,student_id) )
	        cursor.execute("update student set rollno='%s', name='%s',dob='%s',percentage='%s',attendance='%s',driver_no='%s',class_no='%s',year='%s' where student_id='%s'" % (rollno,name,dob,percentage,attendance,driver_no,class_no,year,student_id) )
	        return render(request,'admin.html',{'Submit10': True})
            except:
                print("Student not updated")
	        return render(request,'admin.html',{'Error10': True})

    return render(request, 'modify_student.html')


def deregister(request):
    UserID = request.user.username
    if UserID[:2] == "te" or UserID[:2] =="st":
        return redirect(PSviews.homepage)
    if request.method == "POST":
        
        username = request.POST['username']

        with connection.cursor() as cursor :
            try:
	        print ("delete from auth_user where username='%s'" % (username) )
	        cursor.execute("delete from auth_user where username='%s'" % (username) )
	        return render(request,'admin.html',{'Submit9': True})
            except:
                print("User not deregistered")
	        return render(request,'admin.html',{'Error9': True})

    return render(request, 'deregister.html')


def register_teacher(request):
    UserID = request.user.username
    if UserID[:2] == "te" or UserID[:2] =="st":
        return redirect(PSviews.homepage)
    if request.method == "POST":
        teacher_id = request.POST['teacher_id']
        dob = request.POST['date_of_birth']
        name = request.POST['name']
        joining_date = request.POST['joining_date']
        leaves_taken = request.POST['leaves_taken']
        email_id = request.POST['email_id']
        phone = request.POST['phone']
        address = request.POST['address']
        salary = request.POST['salary']

        with connection.cursor() as cursor :
            try:
	        print ("INSERT INTO teacher values ('%s','%s','%s','%s','%s','%s','%s','%s','%s') " % (teacher_id,name,salary,dob,email_id,phone,address,joining_date,leaves_taken) )
	        cursor.execute("INSERT INTO teacher values ('%s','%s','%s','%s','%s','%s','%s','%s','%s') " % (teacher_id,name,salary,dob,email_id,phone,address,joining_date,leaves_taken) )
	        return render(request,'register.html',{'Submit2': True})
            except:
                print("Teacher not registered")
	        return render(request,'admin.html',{'Error2': True})

    with connection.cursor() as cursor :
        print ("select t.teacher_id,t.salary,t.name,t.dob,t.address,t.phone,t.email_id,t.joining_date,t.leaves_taken from teacher as t,auth_user as a where a.username=t.teacher_id " )
	cursor.execute("select t.teacher_id,t.salary,t.name,t.dob,t.address,t.phone,t.email_id,t.joining_date,t.leaves_taken from teacher as t,auth_user as a where a.username=t.teacher_id " )
        Data = dictfetchall(cursor)
	print Data
	return render(request,'register_teacher.html',{'Data':Data,'Submit2': True})

def modify_teacher(request):
    UserID = request.user.username
    if UserID[:2] == "te" or UserID[:2] =="st":
        return redirect(PSviews.homepage)
    if request.method == "POST":
        teacher_id = request.POST['teacher_id']
        dob = request.POST['date_of_birth']
        name = request.POST['name']
        joining_date = request.POST['joining_date']
        leaves_taken = request.POST['leaves_taken']
        email_id = request.POST['email_id']
        phone = request.POST['phone']
        address = request.POST['address']
        salary = request.POST['salary']

        with connection.cursor() as cursor :
            try:
	        print ("update teacher set name='%s', salary='%s',dob='%s',email_id='%s',phone='%s',address='%s',joining_date='%s',leaves_taken='%s' where teacher_id='%s'" % (name,salary,dob,email_id,phone,address,joining_date,leaves_taken,teacher_id) )
	        cursor.execute("update teacher set name='%s', salary='%s',dob='%s',email_id='%s',phone='%s',address='%s',joining_date='%s',leaves_taken='%s' where teacher_id='%s'" % (name,salary,dob,email_id,phone,address,joining_date,leaves_taken,teacher_id) )
	        return render(request,'admin.html',{'Submit11': True})
            except:
                print("Teacher details not updated")
	        return render(request,'admin.html',{'Error11': True})

    return render(request, 'modify_teacher.html')


def add_news(request):
    UserID = request.user.username
    if UserID[:2] == "te" or UserID[:2] =="st":
        return redirect(PSviews.homepage)
    if request.method == "POST":
        matter = request.POST['matter']
        news_date = request.POST['news_date']

        with connection.cursor() as cursor :
            try:
	        print ("INSERT INTO news(news_date,matter) values('%s','%s') " % (news_date,matter) )
	        cursor.execute("INSERT INTO news(news_date,matter) values('%s','%s') " % (news_date,matter) )
	        return render(request,'admin.html',{'Submit4': True})
            except:
                print("news not registered")
                return render(request,'admin.html',{'Error4': True})
    with connection.cursor() as cursor :
        print ("select * from news" )
	cursor.execute("select * from news" )
        Data = dictfetchall(cursor)
	print Data
	return render(request,'add_news.html',{'Data':Data,'Submit2': True})




def view_complaint(request):

    UserID = request.user.username
    if UserID[:2] == "te" or UserID[:2] =="st":
        return redirect(PSviews.homepage)
    if request.method=="POST":
        complaint_id = request.POST['complaint_id']
        status = request.POST['status']
        with connection.cursor() as cursor :
	    cursor.execute("update complaint set status='%s' where complaint_id='%s' "%(status,complaint_id) )
            cursor.execute("SELECT * FROM complaint" )
	    Data = dictfetchall(cursor)
	    print Data
            return render(request,'view_complaint.html',{'Data': Data,'Message':True})
        
    with connection.cursor() as cursor :
	print ("SELECT * FROM complaint " )
	cursor.execute("SELECT * FROM complaint" )
	Data = dictfetchall(cursor)
	print Data
        
	return render(request,'view_complaint.html',{'Data': Data})



def register_caretaker(request):
    UserID = request.user.username
    if UserID[:2] == "te" or UserID[:2] =="st":
        return redirect(PSviews.homepage)
    if request.method == "POST":
        caretaker_id = request.POST['caretaker_id']
        dob = request.POST['date_of_birth']
        name = request.POST['name']
        joining_date = request.POST['joining_date']
        leaves_taken = request.POST['leaves_taken']
        email_id = request.POST['email_id']
        phone = request.POST['phone']
        address = request.POST['address']
        salary = request.POST['salary']

        with connection.cursor() as cursor :
            try:
	        print ("INSERT INTO caretaker values ('%s','%s','%s','%s','%s','%s','%s','%s','%s') " % (caretaker_id,name,salary,dob,email_id,phone,address,joining_date,leaves_taken) )
	        cursor.execute("INSERT INTO caretaker values ('%s','%s','%s','%s','%s','%s','%s','%s','%s') " % (caretaker_id,name,salary,dob,email_id,phone,address,joining_date,leaves_taken) )
	        return render(request,'admin.html',{'Submit5': True})
            except:
                print("Caretaker not registered")
	        return render(request,'admin.html',{'Error5': True})
    with connection.cursor() as cursor :
        print ("select * from caretaker " )
	cursor.execute("select * from caretaker " )
        Data = dictfetchall(cursor)
	print Data
	return render(request,'register_caretaker.html',{'Data':Data,'Submit2': True})


def register_driver(request):
    UserID = request.user.username
    if UserID[:2] == "te" or UserID[:2] =="st":
        return redirect(PSviews.homepage)
    if request.method == "POST":
        driver_id = request.POST['driver_id']
        dob = request.POST['date_of_birth']
        name = request.POST['name']
        van_no = request.POST['van_no']
        joining_date = request.POST['joining_date']
        leaves_taken = request.POST['leaves_taken']
        email_id = request.POST['email_id']
        phone = request.POST['phone']
        address = request.POST['address']
        salary = request.POST['salary']

        with connection.cursor() as cursor :
            try:
	        print ("INSERT INTO driver values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s') " % (driver_id,name,van_no,salary,dob,email_id,phone,address,joining_date,leaves_taken) )
	        cursor.execute("INSERT INTO driver values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s') " % (driver_id,name,van_no,salary,dob,email_id,phone,address,joining_date,leaves_taken) )
	        return render(request,'admin.html',{'Submit6': True})
            except:
                print("Student not registered")
	        return render(request,'admin.html',{'Error6': True})

    with connection.cursor() as cursor :
        print ("select * from driver " )
	cursor.execute("select * from driver " )
        Data = dictfetchall(cursor)
	print Data
	return render(request,'register_driver.html',{'Data':Data,'Submit2': True})


def update_fees(request):
    UserID = request.user.username
    if UserID[:2] == "te" or UserID[:2] =="st":
        return redirect(PSviews.homepage)
    if request.method == "POST":
        payee = request.POST['payee']
        date_of_payment = request.POST['date_of_payment']
        month = request.POST['month']
        amount = request.POST['amount']

        with connection.cursor() as cursor :
            try:
	        print ("INSERT INTO fees(payee,date_of_payment,month,amount) values('%s','%s','%s','%s') " % (payee,date_of_payment,month,amount) )
	        cursor.execute("INSERT INTO fees(payee,date_of_payment,month,amount) values('%s','%s','%s','%s') " % (payee,date_of_payment,month,amount) )
	        return render(request,'admin.html',{'Submit12': True})
            except:
                print("fees not updated")
                return render(request,'admin.html',{'Error12': True})

    with connection.cursor() as cursor :
        print ("select * from fees order by date_of_payment desc" )
	cursor.execute("select * from fees order by date_of_payment desc" )
        Data = dictfetchall(cursor)
	print Data
	return render(request,'update_fees.html',{'Data':Data,'Submit2': True})

def admin_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return render(request,"admin.html",{'UserType':'Admin','password_change':True})
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })

def teacher_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return render(request,"teacher.html",{'UserType':'Admin','password_change':True})
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })
