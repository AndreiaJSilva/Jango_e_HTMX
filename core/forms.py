from django import forms
from .models import Cliente, Medicamento, Compra
from django.contrib.auth.forms import AuthenticationForm


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'cpf', 'endereco', 'telefone']

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if len(cpf) != 11 or not cpf.isdigit():
            raise forms.ValidationError("O CPF deve ter 11 dígitos numéricos.")
        return cpf


class MedicamentoForm(forms.ModelForm):
    class Meta:
        model = Medicamento
        fields = ['nomeMedicamento', 'fabricante', 'descricao', 'preco']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 3, 'cols': 40}),
        }

    def clean_preco(self):
        preco = self.cleaned_data.get('preco')
        if preco <= 0:
            raise forms.ValidationError("O preço deve ser maior que zero.")
        return preco


class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = ['cliente', 'medicamento', 'quantidade']
        
    def clean_quantidade(self):
        quantidade = self.cleaned_data.get('quantidade')
        if quantidade <= 0:
            raise forms.ValidationError("A quantidade deve ser maior que zero.")
        return quantidade

class MeuLoginForm(AuthenticationForm):
    error_messages = {
        'invalid_login': 'Usuário ou senha incorretos. Verifique seus dados.',
        'inactive': 'Esta conta está inativa.',
    }