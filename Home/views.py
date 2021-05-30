from django.shortcuts import render, redirect
from django.contrib.auth.models import auth

# Create your views here.
def home(request):
    return render(request,"Home/home.html")

def about(request):
    return render(request, 'Home/about.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)

            if is_group(request.user) == "Student":
                return redirect('student')
            elif is_group(request.user) == "Teacher":
                return redirect('teacher')
            else:
                return HttpResponse("you are neither a student nor a teacher.")
        else:
            return render(request,'Home/login.html',{'mesg':'WRONG CREDENTIALS! Please Try Again.'})
    
    else:
        return render(request,'Home/login.html')



def logout(request):
    auth.logout(request)
    return redirect('/')

def is_group(user):
    if user.groups.filter(name='Student').exists():
        return "Student"
    elif user.groups.filter(name='Teacher').exists():
        return "Teacher"
    else:
        return False