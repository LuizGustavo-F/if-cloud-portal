from django.db import models
from django.contrib.auth.models import User

class Maquina(models.Model):
    dono = models.ForeignKey(User, on_delete=models.CASCADE)
    
    nome = models.CharField(max_length=100)
    tamanho = models.CharField(max_length=50)
    chave_ssh = models.TextField(blank=True, null=True)
    
    ip_flutuante = models.CharField(max_length=15, blank=True, null=True)
    
    status = models.CharField(max_length=20, default="Construindo")
    
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome} ({self.status})"