from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import MeuLoginForm


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='core/home.html', authentication_form=MeuLoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # Rotas cliente
    path('clientes/', views.listar_clientes, name='listar_clientes'),
    path('clientes/buscar/', views.buscar_clientes_htmx, name='buscar_clientes_htmx'),
    path('cadastrar-cliente/', views.cadastrar_cliente, name='cadastrar_cliente'),
    path('clientes/atualizar/<int:cliente_id>/', views.atualizar_cliente, name='atualizar_cliente'),
    # URLs HTMX para clientes
    path('clientes/editar-htmx/<int:cliente_id>/', views.editar_cliente_htmx, name='editar_cliente_htmx'),
    path('clientes/salvar-htmx/<int:cliente_id>/', views.salvar_cliente_htmx, name='salvar_cliente_htmx'),
    path('clientes/cancelar-htmx/<int:cliente_id>/', views.cancelar_edicao_htmx, name='cancelar_edicao_htmx'),
    path('clientes/excluir-htmx/<int:cliente_id>/', views.excluir_cliente_htmx, name='excluir_cliente_htmx'),
    path('clientes/confirmar-exclusao-htmx/<int:cliente_id>/', views.confirmar_exclusao_cliente_htmx, name='confirmar_exclusao_cliente_htmx'),
    path('clientes/cancelar-exclusao-htmx/<int:cliente_id>/', views.cancelar_exclusao_cliente_htmx, name='cancelar_exclusao_cliente_htmx'),

    # Rotas Medicamento
    path('medicamentos/', views.listar_medicamentos, name='listar_medicamentos'),
    path('medicamentos/buscar/', views.buscar_medicamentos_htmx, name='buscar_medicamentos_htmx'),
    path('cadastrar-medicamento/', views.cadastrar_medicamento, name='cadastrar_medicamento'),
    path('medicamentos/atualizar/<int:medicamento_id>/', views.atualizar_medicamento, name='atualizar_medicamento'),
    # URLs HTMX para medicamentos
    path('medicamentos/editar-htmx/<int:medicamento_id>/', views.editar_medicamento_htmx, name='editar_medicamento_htmx'),
    path('medicamentos/salvar-htmx/<int:medicamento_id>/', views.salvar_medicamento_htmx, name='salvar_medicamento_htmx'),
    path('medicamentos/cancelar-htmx/<int:medicamento_id>/', views.cancelar_edicao_medicamento_htmx, name='cancelar_edicao_medicamento_htmx'),
    path('medicamentos/excluir-htmx/<int:medicamento_id>/', views.excluir_medicamento_htmx, name='excluir_medicamento_htmx'),
    path('medicamentos/confirmar-exclusao-htmx/<int:medicamento_id>/', views.confirmar_exclusao_medicamento_htmx, name='confirmar_exclusao_medicamento_htmx'),
    path('medicamentos/cancelar-exclusao-htmx/<int:medicamento_id>/', views.cancelar_exclusao_medicamento_htmx, name='cancelar_exclusao_medicamento_htmx'),

    # Rotas Compra
    path('compras/cadastrar/', views.registrar_compra, name='registrar_compra'),
    path('compras/', views.lista_compras, name='lista_compras'),
    path('compras/buscar/', views.buscar_compras_htmx, name='buscar_compras_htmx'),
    path('compras/<int:pk>/editar/', views.editar_compra, name='editar_compra'),
    # URLs HTMX para compras
    path('compras/editar-htmx/<int:compra_id>/', views.editar_compra_htmx, name='editar_compra_htmx'),
    path('compras/salvar-htmx/<int:compra_id>/', views.salvar_compra_htmx, name='salvar_compra_htmx'),
    path('compras/cancelar-htmx/<int:compra_id>/', views.cancelar_edicao_compra_htmx, name='cancelar_edicao_compra_htmx'),
    path('compras/excluir-htmx/<int:compra_id>/', views.excluir_compra_htmx, name='excluir_compra_htmx'),
    path('compras/confirmar-exclusao-htmx/<int:compra_id>/', views.confirmar_exclusao_compra_htmx, name='confirmar_exclusao_compra_htmx'),
    path('compras/cancelar-exclusao-htmx/<int:compra_id>/', views.cancelar_exclusao_compra_htmx, name='cancelar_exclusao_compra_htmx'),

    path('clientes/ver-detalhes-htmx/<int:cliente_id>/', views.ver_detalhes_cliente_htmx, name='ver_detalhes_cliente_htmx'),
    path('clientes/ocultar-detalhes-htmx/<int:cliente_id>/', views.ocultar_detalhes_cliente_htmx, name='ocultar_detalhes_cliente_htmx'),

    path('medicamentos/ver-detalhes-htmx/<int:medicamento_id>/', views.ver_detalhes_medicamento_htmx, name='ver_detalhes_medicamento_htmx'),
    path('medicamentos/ocultar-detalhes-htmx/<int:medicamento_id>/', views.ocultar_detalhes_medicamento_htmx, name='ocultar_detalhes_medicamento_htmx'),

    path('compras/ver-detalhes-htmx/<int:compra_id>/', views.ver_detalhes_compra_htmx, name='ver_detalhes_compra_htmx'),
    path('compras/ocultar-detalhes-htmx/<int:compra_id>/', views.ocultar_detalhes_compra_htmx, name='ocultar_detalhes_compra_htmx'),
]