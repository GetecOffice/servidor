

from django.shortcuts import redirect, render
from django.contrib.auth.models import User

from .models import *

def vista(request):
    registro = Registro.objects.get(ID=1)
    return render(request, 'index.html', {'registro': registro})