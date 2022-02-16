
#from django.conf import settings
from unicodedata import name
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User #to save user to database
from django.contrib import messages 
from django.contrib.auth import authenticate,login,logout
from chatter.models import Person
#from authentication.models import Person
#from . import settings
#from gfg.gfg import settings
from django.core.mail import send_mail
# Create your views here.
def home(request):
    return render(request,'chatter/index.html')

def signup(request):
    if request.method=="POST":
        username=request.POST.get('username')
        name=request.POST['name']
        email=request.POST['email']
        pass1=request.POST.get('pass1')
        pass2=request.POST.get('pass2')

        # if User.objects.filter(username=username):
        #     messages.error(request,'User already exists')
        #     return redirect('home')
        # if User.objects.filter(email=email):
        #     messages.error(request,'email already taken')
        #     return redirect('home')

        # if len(username)>10:
        #     messages.error(request,'username length should be less than 10')

        # if pass1!=pass2:
        #     messages.error(request,"password didn't match")

        # myuser=User.objects.create_user(username,email,pass1)
        # myuser.name= name
        # myuser.save()
        # messages.success(request,'Account is created')
        if Person.objects.filter(username=username):
            messages.error(request,'User already exists')
            return redirect('home')
        if Person.objects.filter(email=email):
            messages.error(request,'email already taken')
            return redirect('home')

        if len(username)>10:
            messages.error(request,'username length should be less than 10')

        if pass1!=pass2:
            messages.error(request,"password didn't match")

        myuser=Person.objects.create_user(username,email,pass1)
        myuser.name= name
        myuser.save()
        messages.success(request,'Account is created')
        

        return redirect('signin')

    return render(request,'chatter/signup.html')
    
def signin(request):
    if request.method=="POST":
        username=request.POST.get('username')
        pass1 = request.POST.get('pass1')

        user= authenticate(username=username,password=pass1)
        if user is not None:
            login(request,user)
            fname=user.username
            return render(request,'chatter/index.html',{'fname':fname})
        else:
            messages.error(request,'Wrong inputs')
            return redirect('home')

    return render(request,'chatter/signin.html')

def signout(request):
    logout(request)
    messages.success(request,'Logged out')
    return redirect('home')

def see_post(request):
    return render(request,'get_post.html')
def posts(request):
    if request.method=='POST':
        name=request.POST['name']
        desc=request.POST['text']
        if name !='':
            if desc !='':
                ins=Person(name=name,desc=desc)
                ins.save()
                print('data sent to database')
    return render(request,'chatter/posts.html')
def see_post(request):
     posts=Person.objects.all()
     #print(posts)
     # for i in posts:
     #     print(i.desc)
     #context=list(posts)
     #context={'tasks':posts}
     return render (request,'chatter/get_post.html',{'tasks':posts})
def delete_post(request,id):
    post=Person.objects.get(id=id)
    post.delete()
    messages.success(request,'post has been deleted!')
    return redirect('see_post')