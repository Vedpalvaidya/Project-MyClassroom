from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.core.files.storage import FileSystemStorage
from main.models import Assignments
import os
import json

global flag
flag = False

# Create your views here.

def editor(request):
    global flag
    if flag is False:
        flag =False
        return render(request,'compilation/new.html')
    else:
        flag = False
        return render(request, 'compilation/new.html', {'mesg' : "code submitted successfully"})

def editorForSubmission(request, assn_no):
    return render(request,'compilation/new.html',{'assn_no' : assn_no})



def compiler(request,run_path):
    return render(request,'compilation/tp.html')

def compiler_n(request):
    return render(request,'compilation/tp.html')

def Teditor(request,run_path):
    l = run_path.split('-')
    file_path = f"media/{l[0]}/{l[1]}"
    file = open(file_path, 'r').read()
    
    print(file_path)
    extn = file_path[-1:file_path.find('.')]
    print(extn)

    file_json = json.dumps(file)
    print(file)
    return render(request,'compilation/new.html',{'file_path':file_json, 'mode':'Teacher'})

def submit(request):
    if not request.user.is_authenticated:
        return redirect('login')

    submit = False
    fs = FileSystemStorage()
    if request.method == 'POST':
        assn = Assignments.objects.all()
        # try:
        upload_file = open('submitted_code.txt', 'r');
        # except:
        #     global file_error
        #     file_error = True
        #     return redirect('student')

        user = request.user
        
        x = request.POST["assn_no"] 
        assn_no = x   
        file_name = "Assignment"+str(assn_no)
        folder_name = user.username+"_"+user.first_name
        storage_path = os.path.join('media',folder_name)
        url_raw = folder_name+"/"+file_name
        url = fs.url(url_raw)
        assignment_name = "assignment"+str(assn_no)
        print("assignment name : ", assignment_name)
        
        
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
        flag = True
        return redirect('/compilation/editor')

    return redirect('/compilation/editor')