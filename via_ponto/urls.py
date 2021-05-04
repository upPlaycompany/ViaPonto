
from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('login_erro/', views.login_erro, name='login_erro'),
    path('redefinir_senha/', views.redefinir_senha, name='redefinir_senha'),
    path('redefinir_senha_sucesso/', views.redefinir_senha_sucesso, name='redefinir_senha_sucesso'),
    path('redefinir_senha_erro/', views.redefinir_senha_erro, name='redefinir_senha_erro'),
    path('dashboard/<str:token>/', views.index, name='dashboard'),
    path('deslogar/<str:token>/', views.deslogar, name='deslogar'),
    path('criar_usuario/', views.criar_usuario, name='criar_usuario'),
    path('criar_usuario_sucesso/', views.criar_usuario_sucesso, name='criar_usuario_sucesso'),
    path('criar_funcionario/<str:token>/', views.criar_funcionario, name='criar_funcionario'),
    path('criar_funcionario_sucesso/<str:token>/', views.criar_funcionario_sucesso, name='criar_funcionario_sucesso'),
    path('listar_funcionario/<str:token>/', views.listar_funcionario, name='listar_funcionario'),
    path('exibir_perfil/<str:token>/<str:id_user>/', views.exibir_perfil, name='exibir_perfil'),
    path('gerar_relatorio_func/<str:token>/', views.gerar_relatorio_func, name='gerar_relatorio_func'),
    path('gerar_relatorio_ponto/<str:token>/<str:id_user>/<str:start_date>/<str:end_date>/', views.gerar_relatorio_ponto, name='gerar_relatorio_ponto'),
    path('editar_empresa/<str:token>/', views.editar_empresa, name='editar_empresa'),
    path('editar_empresa_sucesso/<str:token>/', views.editar_empresa_sucesso, name='editar_empresa_sucesso'),
    path('editar_empresa_erro/<str:token>/', views.editar_empresa_erro, name='editar_empresa_erro'),


    # ÁREA ADMINSTRATIVA
    path('base_admin/<str:token>/', views.base_admin, name='base_admin'),
    path('listar_empresa/<str:token>/', views.listar_empresa, name='listar_empresa'),
    path('ver_empresa/<str:token>/<str:id>/', views.ver_empresa, name='ver_empresa'),
]
