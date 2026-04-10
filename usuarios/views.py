from django.shortcuts import render

def inicio(request):
    return render(request, 'index.html')
from django.shortcuts import render

def inicio(request):
    return render(request, 'index.html')

def usuarios(request):
    return render(request, 'usuarios.html')