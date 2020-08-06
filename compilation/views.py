from django.shortcuts import render
from django.contrib.auth.models import Group
import json


# Create your views here.

def editor(request):
    return render(request,'compilation/new.html')


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