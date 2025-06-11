from django.contrib import admin
from .models import User, Cliente, Medicamento, Compra
from django.contrib.auth.admin import UserAdmin

admin.site.register(User, UserAdmin)
admin.site.register(Cliente)
admin.site.register(Medicamento)
admin.site.register(Compra)
