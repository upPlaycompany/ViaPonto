
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('register/success/', views.register_success, name='register_success'),
    path('login/', views.login_tipo, name='login_tipo'),
    path('login/fail/', views.login_fail, name='login_fail'),
    path('redefinir-senha/', views.redefinir_senha, name='redefinir_senha'),
    path('redefinir-senha/success/', views.redefinir_senha_success, name='redefinir_senha_success'),
    path('redefinir-senha/fail/', views.redefinir_senha_fail, name='redefinir_senha_fail'),
    path('deslogar/<str:token>/', views.deslogar, name='deslogar'),
    path('fail/<str:token>/', views.fail_default, name='fail_default'),
    # COLABORADOR DASHBOARD
    path('login/colaborador/', views.login_colaborador, name='login_colaborador'),
    path('fail/colaborador/<str:token>/', views.fail_default_colaborador, name='fail_default_colaborador'),
    path('dashboard/colaborador/<str:token>/', views.dashboard_colaborador, name='dashboard_colaborador'),
    path('perfil/colaborador/edit/<str:token>/', views.edit_perfil, name='edit_perfil'),
    path('ponto/colaborador/list/<str:token>/', views.list_ponto, name='list_ponto'),
    path('ponto/colaborador/registrar/<str:token>/', views.registro_ponto, name='registro_ponto'),
    path('ponto/colaborador/fail/<str:token>/', views.fail_registro_ponto, name='fail_registro_ponto'),

    # GESTOR DASHBOARD
    path('login/gestor/', views.login_gestor, name='login_gestor'),
    path('dashboard/<str:token>/', views.dashboard, name='dashboard'),
    path('total/registrados/<str:token>/', views.total_registrados, name='total_registrados'),
    path('total/pendentes/<str:token>/', views.total_pendentes, name='total_pendentes'),
    path('total/pendentes/edit-ponto/<str:token>/<str:id_colab>/<str:registro>/', views.edit_ponto_pendente, name='edit_ponto_pendente'),
    # EMPREGADOR
    path('empresa/edit/<str:token>/', views.edit_empresa, name='edit_empresa'),
    path('empresa/success/<str:token>/', views.edit_empresa_success, name='edit_empresa_success'),
    path('empresa/fail/<str:token>/', views.edit_empresa_fail, name='edit_empresa_fail'),
    path('departamento/<str:token>/', views.list_departamento, name='list_departamento'),
    path('departamento/cadastro/<str:token>/', views.cadastro_departamento, name='cadastro_departamento'),
    path('departamento/edit/<str:token>/<str:id>/', views.edit_departamento, name='edit_departamento'),
    path('departamento/delete/<str:token>/<str:id>/', views.delete_departamento, name='delete_departamento'),
    path('feriado/<str:token>/', views.list_feriado, name='list_feriado'),
    path('feriado/cadastro/<str:token>/', views.cadastro_feriado, name='cadastro_feriado'),
    path('feriado/edit/<str:token>/<str:id>/', views.edit_feriado, name='edit_feriado'),
    path('feriado/delete/<str:token>/<str:id>/', views.delete_feriado, name='delete_feriado'),
    # HORÁRIO
    path('horario/<str:token>/', views.list_horario, name='list_horario'),
    path('horario/cadastro/<str:token>/', views.cadastro_horario, name='cadastro_horario'),
    path('horario/edit/<str:token>/<str:id>/', views.edit_horario, name='edit_horario'),
    path('horario/delete/<str:token>/<str:id>/', views.delete_horario, name='delete_horario'),
    # LOCAL
    path('local/<str:token>/', views.list_local, name='list_local'),
    path('local/cadastro/<str:token>/', views.cadastro_local, name='cadastro_local'),
    path('local/edit/<str:token>/<str:id>/', views.edit_local, name='edit_local'),
    path('local/detail/<str:token>/<str:id>/', views.detail_local, name='detail_local'),
    path('local/delete/<str:token>/<str:id>/', views.delete_local, name='delete_local'),
    # COLABORADOR
    path('cargo/<str:token>/', views.list_cargo, name='list_cargo'),
    path('cargo/cadastro/<str:token>/', views.cadastro_cargo, name='cadastro_cargo'),
    path('cargo/edit/<str:token>/<str:id>/', views.edit_cargo, name='edit_cargo'),
    path('cargo/delete/<str:token>/<str:id>/', views.delete_cargo, name='delete_cargo'),
    path('colaborador/<str:token>/', views.list_colaborador, name='list_colaborador'),
    path('colaborador/cadastro/<str:token>/', views.cadastro_colaborador, name='cadastro_colaborador'),
    path('colaborador/cadastro/success/<str:token>/', views.cadastro_colaborador_success, name='cadastro_colaborador_success'),
    path('colaborador/demitir/<str:token>/<str:id>/', views.demitir_colaborador, name='demitir_colaborador'),
    path('colaborador/detail/<str:token>/<str:id>/', views.detail_colaborador, name='detail_colaborador'),
    path('colaborador/edit/<str:token>/<str:id>/', views.edit_colaborador, name='edit_colaborador'),
    path('demitidos/<str:token>/', views.list_demitidos, name='list_demitidos'),
    # RELATORIOS
    path('relatorio/pontos/<str:token>/', views.relatorio_pontos, name='relatorio_pontos'),
    path('relatorio/pontos/colab/<str:token>/<str:id_user>/', views.rel_registros_ponto, name='rel_registros_ponto'),
    path('relatorio/pontos-pendentes/<str:token>/', views.rel_pontos_pendentes, name='rel_pontos_pendentes'),
    path('relatorio/pontos-pendentes/colab/<str:token>/<str:id_user>/', views.rel_pendentes_colab, name='rel_pendentes_colab'),
    path('relatorio/espelho-registros/<str:token>/', views.rel_espelho_registros, name='rel_espelho_registros'),
    path('relatorio/folha-ponto/<str:token>/<str:id_user>/', views.rel_folha_ponto, name='rel_folha_ponto'),
    # PDFs
    path('pdf/folha-ponto/<str:token>/<str:id_user>/<str:mes>/', views.gerar_folha_ponto, name='gerar_folha_ponto'),
    path('relatorio-func/<str:token>/', views.gerar_relatorio_func, name='gerar_relatorio_func'),
    path('relatorio-ponto/<str:token>/<str:id_user>/', views.gerar_relatorio_ponto, name='gerar_relatorio_ponto'),


    # ÁREA ADMINSTRATIVA
    path('admin/dashboard/<str:token>/', views.admin_dashboard, name='admin_dashboard'),
    path('empresa/<str:token>/', views.list_empresa, name='list_empresa'),
    path('detail-empresa/<str:token>/<str:id>/', views.detail_empresa, name='detail_empresa'),
]