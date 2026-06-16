from django.contrib import admin
from django.urls import path, include
from portal_ifmt import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.landing_page, name='landing'),
    path('painel/', views.pagina_inicial, name='painel_maquinas'),
    path('criar/', views.pagina_criacao, name='criar_vm'),
    path('sucesso/', views.pagina_sucesso, name='sucesso'),
    path('processar/', views.processar_pedido, name='processar'),
    path('contas/', include('django.contrib.auth.urls')), 
    path('contas/cadastrar/', views.cadastrar_usuario, name='cadastrar_usuario'),
    
    path('visao-global/', views.visao_global, name='visao_global'),
    
    path('gerenciar/<str:nome_vm>/', views.gerenciar_maquina, name='gerenciar_maquina'),
    path('deletar/<str:nome_vm>/', views.deletar_maquina, name='deletar_vm'),
    
    path('api/metricas/<str:nome_vm>/', views.metricas_maquina_api, name='api_metricas_maquina'),
    path('api/webhook/', views.webhook_ansible, name='webhook'), # Nossa nova rota secreta para os robôs
]