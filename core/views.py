from django.shortcuts import get_object_or_404, render, redirect
from .forms import ClienteForm, MedicamentoForm, CompraForm
from .models import Cliente, Medicamento, Compra
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

def home(request):
    if request.user.is_authenticated:
        return redirect('listar_clientes')

    clientes = Cliente.objects.all()
    medicamentos = Medicamento.objects.all()
    compras = Compra.objects.all()
    return render(request, 'core/home.html', {
        'clientes': clientes,
        'medicamentos': medicamentos,
        'compras': compras
    })

def clientes(request):
    form = ClienteForm()
    return render(request, 'core/clientes.html', {'form': form})

@login_required
def cadastrar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.user = request.user
            cliente.save()
            clientes = Cliente.objects.all()
            return render(request, 'core/listar_clientes.html', {'clientes': clientes})
    # Se não for POST, devolve um formulário novo
    form = ClienteForm()
    return render(request, 'core/partials/formulario_cliente.html', {'form': form})

def clientes_view(request):
    form = ClienteForm() if request.user.is_authenticated else None
    return render(request, 'core/cliente.html', {'form': form})

def listar_clientes(request):
    clientes = Cliente.objects.all()
    
    search = request.GET.get('search')
    if search:
        clientes = clientes.filter(
            nome__icontains=search
        ).union(
            Cliente.objects.filter(cpf__icontains=search)
        )
    
    return render(request, 'core/clientes/listar.html', {'clientes': clientes})

def buscar_clientes_htmx(request):
    clientes = Cliente.objects.all()
    
    search = request.GET.get('search', '').strip()
    if search:
        clientes = clientes.filter(
            nome__icontains=search
        ).union(
            Cliente.objects.filter(cpf__icontains=search)
        )
    
    return render(request, 'core/clientes/_resultados.html', {
        'clientes': clientes,
        'request': request
    })

@login_required
def formulario_cliente(request):
    form = ClienteForm()
    return render(request, 'core/partials/formulario_cadastro.html', {'form': form})

@login_required
def atualizar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)

    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            clientes = Cliente.objects.all()
            return render(request, 'core/listar_clientes.html', {'clientes': clientes})
    else:
        form = ClienteForm(instance=cliente)

    return render(request, 'core/partials/formulario_cliente.html', {
        'form': form,
        'cliente': cliente
    })

@login_required
@require_POST 
def excluir_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    cliente.delete()
    clientes = Cliente.objects.all()
    return render(request, 'core/listar_clientes.html', {'clientes': clientes})

@login_required
def cadastrar_medicamento(request):
    form = MedicamentoForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('listar_medicamentos')
    return render(request, 'core/medicamentos/cadastrar.html', {'form': form})

def listar_medicamentos(request):
    medicamentos = Medicamento.objects.all()
    
    search = request.GET.get('search')
    if search:
        medicamentos = medicamentos.filter(
            nomeMedicamento__icontains=search
        ).union(
            Medicamento.objects.filter(fabricante__icontains=search)
        )
    
    return render(request, 'core/medicamentos/listar.html', {'medicamentos': medicamentos})

def buscar_medicamentos_htmx(request):
    medicamentos = Medicamento.objects.all()
    
    search = request.GET.get('search', '').strip()
    if search:
        medicamentos = medicamentos.filter(
            nomeMedicamento__icontains=search
        ).union(
            Medicamento.objects.filter(fabricante__icontains=search)
        )
    
    return render(request, 'core/medicamentos/_resultados.html', {
        'medicamentos': medicamentos,
        'request': request
    })

@login_required
def atualizar_medicamento(request, medicamento_id):
    medicamento = get_object_or_404(Medicamento, id=medicamento_id)
    form = MedicamentoForm(request.POST or None, instance=medicamento)
    if form.is_valid():
        form.save()
        return redirect('listar_medicamentos')
    return render(request, 'core/medicamentos/cadastrar.html', {'form': form, 'medicamento': medicamento})

@login_required
def registrar_compra(request):
    if request.method == 'POST':
        form = CompraForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_compras')
    else:
        form = CompraForm()
    return render(request, 'core/compras/cadastrar.html', {'form': form})

def lista_compras(request):
    compras = Compra.objects.all()
    
    search = request.GET.get('search')
    if search:
        compras = compras.filter(
            cliente__nome__icontains=search
        ).union(
            Compra.objects.filter(medicamento__nomeMedicamento__icontains=search)
        )
    
    return render(request, 'core/compras/listar.html', {'compras': compras})

def buscar_compras_htmx(request):
    compras = Compra.objects.all()
    
    search = request.GET.get('search', '').strip()
    if search:
        compras = compras.filter(
            cliente__nome__icontains=search
        ).union(
            Compra.objects.filter(medicamento__nomeMedicamento__icontains=search)
        )
    
    return render(request, 'core/compras/_resultados.html', {
        'compras': compras,
        'request': request
    })

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
    return render(request, 'core/compras/cadastrar.html', {'form': form, 'compra': compra})

@login_required
def editar_cliente_htmx(request, cliente_id):
    """Retorna o formulário de edição inline"""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    return render(request, 'core/clientes/editar.html', {'cliente': cliente})

@login_required
def salvar_cliente_htmx(request, cliente_id):
    """Salva as alterações e retorna o item atualizado"""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    
    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        cpf = request.POST.get('cpf', '').strip()
        endereco = request.POST.get('endereco', '').strip()
        telefone = request.POST.get('telefone', '').strip()
        
        # Validação dos campos obrigatórios
        if not all([nome, cpf, endereco, telefone]):
            return render(request, 'core/clientes/editar.html', {
                'cliente': cliente,
                'erro': 'Todos os campos são obrigatórios'
            })
        
        # Atualiza os dados do cliente
        cliente.nome = nome
        cliente.cpf = cpf
        cliente.endereco = endereco
        cliente.telefone = telefone
        cliente.save()
        
        # Retorna o item atualizado
        return render(request, 'core/clientes/_item.html', {'cliente': cliente})
    
    # Se não for POST, retorna o item sem alterações
    return render(request, 'core/clientes/_item.html', {'cliente': cliente})

@login_required
def cancelar_edicao_htmx(request, cliente_id):
    """Cancela a edição e retorna o item original"""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    return render(request, 'core/clientes/_item.html', {'cliente': cliente})

# VIEWS HTMX - MEDICAMENTOS
@login_required
def editar_medicamento_htmx(request, medicamento_id):
    """Retorna o formulário de edição inline para medicamento"""
    medicamento = get_object_or_404(Medicamento, id=medicamento_id)
    return render(request, 'core/medicamentos/editar.html', {'medicamento': medicamento})

@login_required
def salvar_medicamento_htmx(request, medicamento_id):
    """Salva as alterações do medicamento e retorna o item atualizado"""
    medicamento = get_object_or_404(Medicamento, id=medicamento_id)
    
    if request.method == 'POST':
        nome = request.POST.get('nomeMedicamento', '').strip()
        fabricante = request.POST.get('fabricante', '').strip()
        descricao = request.POST.get('descricao', '').strip()
        preco = request.POST.get('preco', '0').strip()
        
        try:
            preco_decimal = float(preco)
            if nome and fabricante and descricao and preco_decimal >= 0:
                medicamento.nomeMedicamento = nome
                medicamento.fabricante = fabricante
                medicamento.descricao = descricao
                medicamento.preco = preco_decimal
                medicamento.save()
                return render(request, 'core/medicamentos/_item.html', {'medicamento': medicamento})
            else:
                return render(request, 'core/medicamentos/editar.html', {
                    'medicamento': medicamento,
                    'erro': 'Todos os campos são obrigatórios e preço deve ser válido'
                })
        except ValueError:
            return render(request, 'core/medicamentos/editar.html', {
                'medicamento': medicamento,
                'erro': 'Preço deve ser um número válido'
            })
    
    return render(request, 'core/medicamentos/_item.html', {'medicamento': medicamento})

@login_required
def cancelar_edicao_medicamento_htmx(request, medicamento_id):
    """Cancela a edição do medicamento e retorna o item original"""
    medicamento = get_object_or_404(Medicamento, id=medicamento_id)
    return render(request, 'core/medicamentos/_item.html', {'medicamento': medicamento})

# VIEWS HTMX - COMPRAS
@login_required
def editar_compra_htmx(request, compra_id):
    """Retorna o formulário de edição inline para compra"""
    compra = get_object_or_404(Compra, id=compra_id)
    clientes = Cliente.objects.all()
    medicamentos = Medicamento.objects.all()
    return render(request, 'core/compras/editar.html', {
        'compra': compra,
        'clientes': clientes,
        'medicamentos': medicamentos
    })

@login_required
def salvar_compra_htmx(request, compra_id):
    """Salva as alterações da compra e retorna o item atualizado"""
    compra = get_object_or_404(Compra, id=compra_id)
    
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente')
        medicamento_id = request.POST.get('medicamento')
        quantidade = request.POST.get('quantidade', '1')
        data = request.POST.get('data')
        
        try:
            cliente = Cliente.objects.get(id=cliente_id)
            medicamento = Medicamento.objects.get(id=medicamento_id)
            quantidade_int = int(quantidade)
            
            compra.cliente = cliente
            compra.medicamento = medicamento
            compra.quantidade = quantidade_int
            
            from datetime import datetime
            if data:
                compra.data = datetime.strptime(data, '%Y-%m-%d').date()
            
            if cliente and medicamento and quantidade_int > 0:
                compra.save()
                return render(request, 'core/compras/_item.html', {'compra': compra})
            else:
                clientes = Cliente.objects.all()
                medicamentos = Medicamento.objects.all()
                return render(request, 'core/compras/editar.html', {
                    'compra': compra,
                    'clientes': clientes,
                    'medicamentos': medicamentos,
                    'erro': 'Todos os campos são obrigatórios e quantidade deve ser maior que zero'
                })
        except (Cliente.DoesNotExist, Medicamento.DoesNotExist, ValueError):
            clientes = Cliente.objects.all()
            medicamentos = Medicamento.objects.all()
            return render(request, 'core/compras/editar.html', {
                'compra': compra,
                'clientes': clientes,
                'medicamentos': medicamentos,
                'erro': 'Dados inválidos fornecidos'
            })
    
    return render(request, 'core/compras/_item.html', {'compra': compra})

@login_required
def cancelar_edicao_compra_htmx(request, compra_id):
    """Cancela a edição da compra e retorna o item original"""
    compra = get_object_or_404(Compra, id=compra_id)
    return render(request, 'core/compras/_item.html', {'compra': compra})

# VIEWS HTMX - EXCLUSÃO
@login_required
def excluir_cliente_htmx(request, cliente_id):
    """Mostra o formulário de confirmação de exclusão inline"""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    return render(request, 'core/clientes/excluir.html', {'cliente': cliente})

@login_required
def confirmar_exclusao_cliente_htmx(request, cliente_id):
    """Confirma e executa a exclusão do cliente"""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    
    if request.method == 'POST':
        cliente.delete()
        return render(request, 'core/partials/_item_excluido.html')
    return render(request, 'core/clientes/_item.html', {'cliente': cliente})

@login_required
def cancelar_exclusao_cliente_htmx(request, cliente_id):
    """Cancela a exclusão e retorna o item original"""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    return render(request, 'core/clientes/_item.html', {'cliente': cliente})

@login_required
def excluir_medicamento_htmx(request, medicamento_id):
    """Mostra o formulário de confirmação de exclusão inline"""
    medicamento = get_object_or_404(Medicamento, id=medicamento_id)
    return render(request, 'core/medicamentos/excluir.html', {'medicamento': medicamento})

@login_required
def confirmar_exclusao_medicamento_htmx(request, medicamento_id):
    """Confirma e executa a exclusão do medicamento"""
    medicamento = get_object_or_404(Medicamento, id=medicamento_id)
    if request.method == 'POST':
        medicamento.delete()
        return render(request, 'core/partials/_item_excluido.html')
    return render(request, 'core/medicamentos/_item.html', {'medicamento': medicamento})

@login_required
def cancelar_exclusao_medicamento_htmx(request, medicamento_id):
    """Cancela a exclusão e retorna o item original"""
    medicamento = get_object_or_404(Medicamento, id=medicamento_id)
    return render(request, 'core/medicamentos/_item.html', {'medicamento': medicamento})

@login_required
def excluir_compra_htmx(request, compra_id):
    """Mostra o formulário de confirmação de exclusão inline"""
    compra = get_object_or_404(Compra, id=compra_id)
    return render(request, 'core/compras/excluir.html', {'compra': compra})

@login_required
def confirmar_exclusao_compra_htmx(request, compra_id):
    """Confirma e executa a exclusão da compra"""
    compra = get_object_or_404(Compra, id=compra_id)
    if request.method == 'POST':
        compra.delete()
        return render(request, 'core/partials/_item_excluido.html')
    return render(request, 'core/compras/_item.html', {'compra': compra})

@login_required
def cancelar_exclusao_compra_htmx(request, compra_id):
    """Cancela a exclusão e retorna o item original"""
    compra = get_object_or_404(Compra, id=compra_id)
    return render(request, 'core/compras/_item.html', {'compra': compra})

# VIEWS HTMX - DETALHES
def ver_detalhes_cliente_htmx(request, cliente_id):
    """Mostra os detalhes completos do cliente"""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    return render(request, 'core/clientes/_item_detalhado.html', {'cliente': cliente})

def ocultar_detalhes_cliente_htmx(request, cliente_id):
    """Volta para a visualização resumida do cliente"""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    return render(request, 'core/clientes/_item.html', {'cliente': cliente})

# VIEWS HTMX - DETALHES MEDICAMENTOS
def ver_detalhes_medicamento_htmx(request, medicamento_id):
    """Mostra os detalhes completos do medicamento"""
    medicamento = get_object_or_404(Medicamento, id=medicamento_id)
    return render(request, 'core/medicamentos/_item_detalhado.html', {'medicamento': medicamento})

def ocultar_detalhes_medicamento_htmx(request, medicamento_id):
    """Volta para a visualização resumida do medicamento"""
    medicamento = get_object_or_404(Medicamento, id=medicamento_id)
    return render(request, 'core/medicamentos/_item.html', {'medicamento': medicamento})

# VIEWS HTMX - DETALHES COMPRAS
def ver_detalhes_compra_htmx(request, compra_id):
    """Mostra os detalhes completos da compra"""
    compra = get_object_or_404(Compra, id=compra_id)
    return render(request, 'core/compras/_item_detalhado.html', {'compra': compra})

def ocultar_detalhes_compra_htmx(request, compra_id):
    """Volta para a visualização resumida da compra"""
    compra = get_object_or_404(Compra, id=compra_id)
    return render(request, 'core/compras/_item.html', {'compra': compra})