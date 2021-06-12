
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('register-success/', views.register_success, name='register_success'),
    path('login-colaborador/', views.login_colaborador, name='login_colaborador'),
    path('login-gestor/', views.login_gestor, name='login_gestor'),
    path('login-fail/', views.login_fail, name='login_fail'),
    path('redefinir-senha/', views.redefinir_senha, name='redefinir_senha'),
    path('redefinir-senha-success/', views.redefinir_senha_success, name='redefinir_senha_success'),
    path('redefinir-senha-fail/', views.redefinir_senha_fail, name='redefinir_senha_fail'),
    path('deslogar/<str:token>/', views.deslogar, name='deslogar'),
    path('dashboard/<str:token>/', views.dashboard, name='dashboard'),
    path('fail/<str:token>/', views.fail_default, name='fail_default'),
    # EMPREGADOR
    path('empresa/edit/<str:token>/', views.edit_empresa, name='edit_empresa'),
    path('empresa/success/<str:token>/', views.edit_empresa_success, name='edit_empresa_success'),
    path('empresa/fail/<str:token>/', views.edit_empresa_fail, name='edit_empresa_fail'),
    path('departamento/<str:token>/', views.list_departamento, name='list_departamento'),
    path('departamento/cadastro/<str:token>/', views.cadastro_departamento, name='cadastro_departamento'),
    path('departamento/edit/<str:token>/<str:id>/', views.edit_departamento, name='edit_departamento'),
    path('departamento/delete/<str:token>/<str:id>/', views.delete_departamento, name='delete_departamento'),
    path('feriado/<str:token>/', views.list_feriado, name='list_feriado'),
    # HORÁRIO
    path('horario/<str:token>/', views.list_horario, name='list_horario'),
    path('horario/cadastro/<str:token>/', views.cadastro_horario, name='cadastro_horario'),
    path('horario/edit/<str:token>/<str:id>', views.edit_horario, name='edit_horario'),
    # LOCAL
    path('local/<str:token>/', views.list_local, name='list_local'),
    path('cadastro-local/<str:token>/', views.cadastro_local, name='cadastro_local'),
    # COLABORADOR
    path('cargo/<str:token>/', views.list_cargo, name='list_cargo'),
    path('colaborador/<str:token>/', views.list_colaborador, name='list_colaborador'),
    path('cadastro-colaborador/<str:token>/', views.cadastro_colaborador, name='cadastro_colaborador'),
    path('cadastro-colaborador-success/<str:token>/', views.cadastro_colaborador_success, name='cadastro_colaborador_success'),
    path('demitidos/<str:token>/', views.list_demitidos, name='list_demitidos'),


    path('pontos-colaborador/<str:token>/<str:id_user>/', views.pontos_colaborador, name='pontos_colaborador'),
    path('relatorio-func/<str:token>/', views.gerar_relatorio_func, name='gerar_relatorio_func'),
    path('relatorio-ponto/<str:token>/<str:id_user>/<str:start_date>/<str:end_date>/', views.gerar_relatorio_ponto, name='gerar_relatorio_ponto'),


    # ÁREA ADMINSTRATIVA
    path('base_admin/<str:token>/', views.base_admin, name='base_admin'),
    path('empresa/<str:token>/', views.list_empresa, name='list_empresa'),
    path('detail-empresa/<str:token>/<str:id>/', views.detail_empresa, name='detail_empresa'),
]