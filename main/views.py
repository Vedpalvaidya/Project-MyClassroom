from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib.auth.models import auth, User, Group
from django.core.files.storage import FileSystemStorage
from .models import Assignments, Assignment_structure
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.core.mail import send_mail
import os
import time
import datetime as dt
from .forms import NameForm

# Create your views here.
flag = False
file_error = False
assn_num = 0
result_list = []
status = []

def is_group(user):
    if user.groups.filter(name='Student').exists():
        return "Student"
    elif user.groups.filter(name='Teacher').exists():
        return "Teacher"
    else:
        return False

@login_required(redirect_field_name='main/',login_url='login')
def student(request):
    if not is_group(request.user) == "Student":
        return HttpResponseNotFound("<h1>Page not found</h1>")
   
    global flag
    global file_error
    user_obj = request.user
    if not Assignments.objects.filter(user_id = user_obj.id).exists():
        status = Assignments(user_id = user_obj.id)
        status.save

    status = Assignments.objects.filter(user_id = user_obj.id)
    print("\n\nStatus ",status)
    error_mesg = "Please select the file first"
   
    if flag:
        flag = False
        return render(request, 'main/new_student.html',{'num': [1,2,3,4,5,6,7,8],'mesg':"Submitted Successfully", 'status': status})
    elif file_error:
         file_error = False
         return render(request, 'main/new_student.html',{'num': [1,2,3,4,5,6,7,8], 'error_mesg':error_mesg, 'status': status})
    else:
        return render(request, 'main/new_student.html',{'num': [1,2,3,4,5,6,7,8], 'status': status})



@login_required(redirect_field_name='main/',login_url='login')
def teacher(request):
    if not is_group(request.user) == "Teacher":
        return HttpResponseNotFound("<h1>Page not found</h1>")

    assns = Assignment_structure.objects.order_by('assn_no')
    return render(request,'main/teacher.html',{'assns':assns})



@login_required(redirect_field_name='main/',login_url='login')
def assign_structure(request):
    if not is_group(request.user) == "Teacher":
        return HttpResponseNotFound("<h1>Page not found</h1>")

    if request.method == 'POST':
        assn_no = request.POST['no']
        assn_name = request.POST['name']
        assn_desc = request.POST['description']
        assn_due_date = request.POST['due_date']
        author = request.POST['author']

        assn_struct = Assignment_structure.objects.all()
        assn_exist = False

        for x in assn_struct:
            if assn_struct is not None and x.assn_no == assn_no:
                assn_exist = True
                break
    
        if assn_exist:
            assn_struct = Assignment_structure.objects.filter(assn_no=assn_no).update(assn_name=assn_name,assn_description=assn_desc,due_date=assn_due_date,author=author)
            assn_struct.save()
        else:
            assn_struct = Assignment_structure(assn_no=assn_no,assn_name=assn_name,assn_description=assn_desc,due_date=assn_due_date,author=author)
            assn_struct.save()
        
        all_users = User.objects.all()

        send_to = list()
        for user in all_users:
            if user.groups.filter(name='Student').exists():
                send_to.append(user.email)
        
        send_to.append(request.user.email)
        body = f""" \n Name: {assn_name}\n\n Description : \n\t{assn_desc}\n\n Due date : {assn_due_date}
               
                                                                            \nBy: {author}
        """
        
        x = send_mail('Myclassroom - New Assignment',body,'harshbeprime@gmail.com',send_to,fail_silently=False)
        if x == 1:
            assns = Assignment_structure.objects.order_by('assn_no')
            return render(request,'main/teacher.html',{'assns':assns})
        else:     
            return HttpResponse('Error')          
        
    return render(request,'main/assignment_structure.html')



@login_required(redirect_field_name='main/',login_url='login')        
def remove_assn(request,assn_no):
    if not is_group(request.user) == "Teacher":
        return HttpResponseNotFound("<h1>Page not found</h1>")

    assign_structure = Assignment_structure.objects.all()
    assign_structure = Assignment_structure.objects.filter(assn_no=assn_no).delete()

    return redirect('teacher')



@login_required(redirect_field_name='main/',login_url='login')
def batch(request):
    if not is_group(request.user) == "Teacher":
        return HttpResponseNotFound("<h1>Page not found</h1>")

    assns = Assignments.objects.all()
    return render(request,'main/batch.html',{'assns':assns})

def submit(request, assn_no):
    try:
        assn_obj = Assignment_structure.objects.filter(assn_no = assn_no)
        print(assn_obj[0].due_date)
    except:
        assn_obj = "assignment not yet initiated"

    return render(request, 'main/submit.html', {'assignment' : assn_obj[0]})

@login_required(redirect_field_name='/',login_url='login')
def upload(request, assn_no):
    if not request.user.is_authenticated:
        return redirect('login')

    submit = False
    fs = FileSystemStorage()
    if request.method == 'POST':
        assn = Assignments.objects.all()
        try:
            upload_file = request.FILES['myfile1']
        except:
            global file_error
            file_error = True
            return redirect('student')

        user = request.user
        for x in range(1,9):
            if x == assn_no:
                file_name = "Assignment"+str(assn_no)
                folder_name = user.username+"_"+user.first_name
                storage_path = os.path.join('media',folder_name)
                url_raw = folder_name+"/"+file_name
                url = fs.url(url_raw)
        assignment_name = "assignment"+str(assn_no)
        print("assignment name : ", assignment_name)
        
        for x in range(1,9):
            if assn_no == x:
                if Assignments.objects.filter(user_id = user.id):
                    assn = eval(f'Assignments.objects.filter(user_id = user.id).update(assignment{x}=url, status_{x} = True)')
                    file_path = os.path.join(storage_path,file_name)
                    
                    if os.path.isfile(file_path):
                        os.remove(file_path)

                    submit = True
            
                else:
                    assn = eval(f'Assignments(assignment{x}=url, user=user, status_{x} = True)')
                    assn.save()
                    submit = True

        fs = FileSystemStorage(location=storage_path)
        fs.save(file_name,upload_file) 
       
        global flag
        global assn_num
        assn_num = assn_no
        flag = True
        return redirect('student')
    
    return render(request,'main/student.html')



def test(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            print("\n\n\n NAme: ", form.your_name)
            return HttpResponse('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'main/test.html', {'form': form})

