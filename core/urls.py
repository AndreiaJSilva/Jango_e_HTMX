from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # Rotas cliente
    path('clientes/', views.clientes, name='clientes'),  # página principal
    path('clientes/', views.clientes_view, name='clientes'),
    path('clientes/listar/', views.listar_clientes, name='listar_clientes'),
    path('clientes/cadastrar/', views.cadastrar_cliente, name='cadastrar_cliente'),
    path('clientes/atualizar/<int:cliente_id>/', views.atualizar_cliente, name='atualizar_cliente'),
    path('clientes/excluir/<int:cliente_id>/', views.excluir_cliente, name='excluir_cliente'),

    # Rotas Medicamento
    path('medicamentos/', views.listar_medicamentos, name='listar_medicamentos'),
    path('cadastrar-medicamento/', views.cadastrar_medicamento, name='cadastrar_medicamento'),
    path('medicamentos/atualizar/<int:medicamento_id>/', views.atualizar_medicamento, name='atualizar_medicamento'),
    path('medicamentos/excluir/<int:medicamento_id>/', views.excluir_medicamento, name='excluir_medicamento'),

    # Rotas Compra
    path('compras/cadastrar/', views.registrar_compra, name='registrar_compra'),
    path('compras/', views.lista_compras, name='lista_compras'),
    path('compras/<int:pk>/editar/', views.editar_compra, name='editar_compra'),
    path('compras/<int:pk>/excluir/', views.excluir_compra, name='excluir_compra'),

    # Rotas Login

]
