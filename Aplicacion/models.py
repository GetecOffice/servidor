# models.py
from django.db import models

class Registro(models.Model):
    ID = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=100)
    estatus = models.IntegerField(default=0)
    actualizado = models.DateTimeField(auto_now=True)
