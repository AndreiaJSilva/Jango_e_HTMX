# python manage.py runserver
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # Já herda login e senha
    pass

class Cliente(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14, unique=True)
    endereco = models.TextField()
    telefone = models.CharField(max_length=15)

    def __str__(self):
        return self.nome


class Medicamento(models.Model):
    nomeMedicamento = models.CharField(max_length=100)
    fabricante = models.CharField(max_length=100)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)

    def __str__(self):
        return self.nomeMedicamento

    

class Compra(models.Model):
  cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='compras')
  medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE, related_name='compras', null=True)
  quantidade = models.PositiveIntegerField(default=1)
  data = models.DateField(auto_now_add=True)  # auto_now_add para registrar a data automaticamente
  valor = models.DecimalField(max_digits=10, decimal_places=2)

  def save(self, *args, **kwargs):
      self.valor = self.medicamento.preco * self.quantidade
      super().save(*args, **kwargs)

  def __str__(self):
      return f"Compra de {self.cliente.nome} em {self.data}"