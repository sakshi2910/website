from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import connection
from preschool import validations
from preschool.validations import exists,validateEmail


# Create your views here.

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]		


def homepage(request):
    with connection.cursor() as cursor :
        try:
	    print ("select * from news order by news_id desc")
	    cursor.execute("select * from news order by news_id desc")
            Data = dictfetchall(cursor)
            print Data[:7]
	    return render(request,'homepage.html',{'Data': Data[:7]})
        except:
            print("news not displayed")
            return render(request,'homepage.html',{'Error': True})

def all_news(request):
    with connection.cursor() as cursor :
        try:
	    print ("select * from news order by news_id desc")
	    cursor.execute("select * from news order by news_id desc")
            Data = dictfetchall(cursor)
            print Data
	    return render(request,'all_news.html',{'Data': Data})
        except:
            print("news not displayed")
            return render(request,'homepage.html',{'Error': True})

def about(request):
    return render(request, 'about.html', {})

def admission(request):
    return render(request, 'admission.html', {})

def help(request):
    with connection.cursor() as cursor :
        try:
	    print ("select * from faqs ")
	    cursor.execute("select * from faqs ")
            Data = dictfetchall(cursor)
            print Data[:7]
	    return render(request,'faq.html',{'Data': Data[:7]})
        except:
            print("faqs not displayed")
            return render(request,'faq.html',{'Error': True})

    return render(request, 'faq.html', {})

def contact(request):
    return render(request, 'contact.html', {})


