from django.shortcuts import get_object_or_404, render, redirect
from .forms import ClienteForm, MedicamentoForm, CompraForm
from .models import Cliente, Medicamento, Compra
from django.contrib.auth.decorators import login_required

def home(request):
    clientes = Cliente.objects.all()
    medicamentos = Medicamento.objects.all()
    compras = Compra.objects.all()
    return render(request, 'core/home.html', {
        'clientes': clientes,
        'medicamentos': medicamentos,
        'compras': compras
    })

@login_required
def cadastrar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.user = request.user
            cliente.save()
            if request.headers.get('HX-Request'):  # HTMX detectado
                clientes = Cliente.objects.all()
                return render(request, 'core/listar_clientes.html', {'clientes': clientes})
            return redirect('listar_clientes')
    else:
        form = ClienteForm()
    clientes = Cliente.objects.all()
    return render(request, 'core/cadastrar_cliente.html', {'form': form, 'clientes': clientes})

def listar_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'core/listar_clientes.html', {'clientes': clientes})

@login_required
def atualizar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return render(request, 'core/listar_clientes.html', {'clientes': Cliente.objects.all()})
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'core/atualizar_cliente.html', {'form': form, 'cliente': cliente, 'cliente_id': cliente_id})

@login_required
def excluir_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        cliente.delete()
        # Retorna apenas a lista atualizada como fragmento
        clientes = Cliente.objects.all()
        return render(request, 'core/listar_clientes.html', {'clientes': clientes})
    return render(request, 'core/excluir_cliente.html', {'cliente': cliente})

@login_required
def cadastrar_medicamento(request):
  form = MedicamentoForm(request.POST or None)
  if form.is_valid():
      form.save()
      return redirect('listar_medicamentos')
  return render(request, 'core/cadastrar_medicamento.html', {'form': form})

def listar_medicamentos(request):
  medicamentos = Medicamento.objects.all()
  return render(request, 'core/listar_medicamentos.html', {'medicamentos': medicamentos})

@login_required
def atualizar_medicamento(request, medicamento_id):
  medicamento = get_object_or_404(Medicamento, id=medicamento_id)
  form = MedicamentoForm(request.POST or None, instance=medicamento)
  if form.is_valid():
      form.save()
      return redirect('listar_medicamentos')
  return render(request, 'core/cadastrar_medicamento.html', {'form': form})

@login_required
def excluir_medicamento(request, medicamento_id):
  medicamento = get_object_or_404(Medicamento, id=medicamento_id)
  if request.method == 'POST':
      medicamento.delete()
      return redirect('listar_medicamentos')
  return render(request, 'core/excluir_medicamento.html', {'medicamento': medicamento})

@login_required
def registrar_compra(request):
  if request.method == 'POST':
      form = CompraForm(request.POST)
      if form.is_valid():
          form.save()
          return redirect('lista_compras')
  else:
      form = CompraForm()
  return render(request, 'core/registrar_compra.html', {'form': form})

def lista_compras(request):
  compras = Compra.objects.all()
  return render(request, 'core/lista_compras.html', {'compras': compras})

@login_required
def editar_compra(request, pk):
  compra = get_object_or_404(Compra, pk=pk)
  if request.method == 'POST':
      form = CompraForm(request.POST, instance=compra)
      if form.is_valid():
          form.save()
          return redirect('lista_compras')
  else:
      form = CompraForm(instance=compra)
  return render(request, 'core/editar_compra.html', {'form': form})

@login_required
def excluir_compra(request, pk):
  compra = get_object_or_404(Compra, pk=pk)
  if request.method == 'POST':
      compra.delete()
      return redirect('lista_compras')
  return render(request, 'core/excluir_compra.html', {'compra': compra})


def teste_css(request):
    return render(request, 'core/teste_css.html')
