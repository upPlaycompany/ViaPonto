import json
import requests
import urllib3
import datetime
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth as autent
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import paginator
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import connections
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from datetime import *
from easy_pdf import rendering
from django.utils.six import BytesIO

def index(request, token):
    conexao = requests.api.request('GET', 'https://parseapi.back4app.com/users/me', headers={
                                    "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                                    "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
                                    "X-Parse-Session-Token": f"{token}"})
    usuario = conexao.json()
    if str(usuario['sessionToken']) != f"{token}":
        return redirect('login')
    elif usuario['empresa_confirmacao'] == False:
        return redirect('login')
    elif usuario['admin'] == True:
        return redirect('login')
    else:
        pass
    key = [{'id': token, 'emp': usuario['nome_empresa'], 'user': usuario['username']}]

    return render(request, 'index.html', {'lista': key})


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        conexao = requests.api.request('GET',
                                       f"https://parseapi.back4app.com/login?username={username}&password={password}",
                                       headers={
                                           "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                                           "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
                                           "X-Parse-Revocable-Session": '1'
                                       })
        abc = conexao.json()
        abp = str(conexao.status_code)
        
        if abp == '200' and abc['admin'] == True:
            return redirect('base_admin', token=abc['sessionToken'])
        elif abp == '200' and abc['empresa_confirmacao'] == True:
            return redirect('dashboard', token=abc['sessionToken'])
        elif abp == '200' and abc['admin'] == True:
            return redirect('base_admin', token=abc['sessionToken'])
        else:
            return redirect('login')

    return render(request, 'login.html')


def deslogar(request, token):
    requests.api.request('GET', 'https://parseapi.back4app.com/logout', headers={
        "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
        "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
        "X-Parse-Session-Token": f"{token}"})

    return redirect('login')


def redefinir_senha(request):
    if request.method == 'POST':
        email = request.POST['email']
        
        conexao = requests.api.request('POST', f"https://parseapi.back4app.com/requestPasswordReset",
                                        headers={
                                                "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                                                "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
                                                "Content-Type": "application/json"},
                                        json={
                                                "email": f"{email}",
                                        })
        response = conexao.json()
        status = str(conexao.status_code)
        print(status)
        if status == '200':
            return redirect('redefinir_senha_sucesso')
        else:
            return redirect('redefinir_senha_erro')

    return render(request, 'redefinir_senha.html')


def redefinir_senha_sucesso(request):
    return render(request, 'redefinir_senha_sucesso.html')


def redefinir_senha_erro(request):
    return render(request, 'redefinir_senha_erro.html')



def criar_usuario(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        cpf = request.POST['cpf']
        nome = request.POST['nome']
        datanasc = request.POST['datanasc']
        email = request.POST['email']
        celular = request.POST['celular']
        cargo = request.POST['cargo']
        departamento = request.POST['departamento']
        cnpj = request.POST['cnpj']
        cep = request.POST['cep']
        tel_comercial = request.POST['tel_comercial']
        nome_empresa = request.POST['nome_empresa']
        celular_empresa = request.POST['celular_empresa']
        razaosocial = request.POST['razaosocial']
        ie = request.POST['ie']
        atividade = request.POST['atividade']
        uf = request.POST['uf']
        email_empresa = request.POST['email_empresa']
        logradouro = request.POST['logradouro']
        numero = request.POST['numero']
        bairro = request.POST['bairro']
        conexao1 = requests.api.request('POST', f"https://parseapi.back4app.com/classes/Empresa/",

                                        headers={
                                            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                                            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
                                            "Context-Type": "application/json"},
                                        json={
                                            "cep": f"{cep}",
                                            "cnpj": f"{cnpj}",
                                            "tel_comercial": f"{tel_comercial}",
                                            "nome_empresa": f"{nome_empresa}",
                                            "celular_empresa": f"{celular_empresa}",
                                            "razaosocial": f"{razaosocial}",
                                            "ie": f"{ie}",
                                            "atividade": f"{atividade}",
                                            "uf": f"{uf}",
                                            "email_empresa": f"{email_empresa}",
                                            "logradouro": f"{logradouro}",
                                            "numero": f"{numero}",
                                            "bairro": f"{bairro}",
                                        })
        empresa = conexao1.json()
        status = str(conexao1.status_code)
        empresa_id = empresa['objectId']

        if status != '201':
            return redirect('login')

        conexao2 = requests.api.request('POST', f"https://parseapi.back4app.com/users",
                                        headers={"X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                                                 "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
                                                 "X-Parse-Revocable-Session": "1",
                                                 "Content-Type": "application/json"},
                                        json={
                                            "username": f"{username}",
                                            "password": f"{password}",
                                            "cpf": f"{cpf}",
                                            "nome": f"{nome}",
                                            "data_nasc": f"{datanasc}",
                                            "email": f"{email}",
                                            "celular": f"{celular}",
                                            "cargo": f"{cargo}",
                                            "departamento": f"{departamento}",
                                            "empresa_confirmacao": bool(True),
                                            "nome_empresa": f"{nome_empresa}",
                                            "admin": bool(False),
                                            "id_empresa": {
                                                '__type': "Pointer",
                                                "className": "Empresa",
                                                "objectId": empresa_id}
                                        })
        ppp = conexao2.json()
        ppa = str(conexao2.status_code)
        if ppa == '201':
            return redirect('criar_usuario_sucesso')
        else:
            return redirect('login')

    return render(request, 'criar_usuario.html', {})


def criar_usuario_sucesso(request):
    return render(request, 'criar_usuario_sucesso.html')


def criar_funcionario(request, token, empresa):
    conexao = requests.api.request('GET', 'https://parseapi.back4app.com/users/me', headers={
                                        "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                                        "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
                                        "X-Parse-Session-Token": f"{token}"})

    abc = conexao.json()
    if str(abc['sessionToken']) != f"{token}":
        return redirect('login')
    elif abc['empresa_confirmacao'] == False:
        return redirect('login')
    else:
        pass

    key = [{'id': token, 'emp': abc['nome_empresa'], 'user': abc['username']}]
    empresa_id = abc['id_empresa']['objectId']

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        cpf = request.POST['cpf']
        nome = request.POST['nome']
        datanasc = request.POST['datanasc']
        email = request.POST['email']
        celular = request.POST['celular']
        cargo = request.POST['cargo']
        departamento = request.POST['departamento']
        hora_semana_entrada_1 = request.POST['hora_semana_entrada_1']
        if hora_semana_entrada_1 == "":
            hora_semana_entrada_1 = "nao definido"

        hora_semana_saida_1 = request.POST['hora_semana_saida_1']
        if hora_semana_saida_1 == "":
            hora_semana_saida_1 = "nao definido"

        hora_semana_entrada_2 = request.POST['hora_semana_entrada_2']
        if hora_semana_entrada_2 == "":
            hora_semana_entrada_2 = "nao definido"

        hora_semana_saida_2 = request.POST['hora_semana_saida_2']
        if hora_semana_saida_2 == "":
            hora_semana_saida_2 = "nao definido"

        hora_sabado_entrada_1 = request.POST['hora_sabado_entrada_1']
        if hora_sabado_entrada_1 == "":
            hora_sabado_entrada_1 = "nao definido"

        hora_sabado_saida_1 = request.POST['hora_sabado_saida_1']
        if hora_sabado_saida_1 == "":
            hora_sabado_saida_1 = "nao definido"

        hora_sabado_entrada_2 = request.POST['hora_sabado_entrada_2']
        if hora_sabado_entrada_2 == "":
            hora_sabado_entrada_2 = "nao definido"

        hora_sabado_saida_2 = request.POST['hora_sabado_saida_2']
        if hora_sabado_saida_2 == "":
            hora_sabado_saida_2 = "nao definido"

        hora_domingo_entrada_1 = request.POST['hora_domingo_entrada_1']
        if hora_domingo_entrada_1 == "":
            hora_domingo_entrada_1 = "nao definido"

        hora_domingo_saida_1 = request.POST['hora_domingo_saida_1']
        if hora_domingo_saida_1 == "":
            hora_domingo_saida_1 = "nao definido"

        hora_domingo_entrada_2 = request.POST['hora_domingo_entrada_2']
        if hora_domingo_entrada_2 == "":
            hora_domingo_entrada_2 = "nao definido"

        hora_domingo_saida_2 = request.POST['hora_domingo_saida_2']
        if hora_domingo_saida_2 == "":
            hora_domingo_saida_2 = "nao definido"

        conexao1 = requests.api.request('POST', f"https://parseapi.back4app.com/users",
                                        headers={"X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                                                 "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
                                                 "X-Parse-Revocable-Session": "1",
                                                 "Content-Type": "application/json"},
                                        json={
                                            "username": f"{username}",
                                            "password": f"{password}",
                                            "cpf": f"{cpf}",
                                            "nome": f"{nome}",
                                            "data_nasc": f"{datanasc}",
                                            "email": f"{email}",
                                            
                                            "celular": f"{celular}",
                                            "cargo": f"{cargo}",
                                            "departamento": f"{departamento}",
                                            "hora_semana_entrada_1": f"{hora_semana_entrada_1}",
                                            "hora_semana_saida_1": f"{hora_semana_saida_1}",
                                            "hora_semana_entrada_2": f"{hora_semana_entrada_2}",
                                            "hora_semana_saida_2": f"{hora_semana_saida_2}",
                                            "hora_sabado_entrada_1": f"{hora_sabado_entrada_1}",
                                            "hora_sabado_saida_1": f"{hora_sabado_saida_1}",
                                            "hora_sabado_entrada_2": f"{hora_sabado_entrada_2}",
                                            "hora_sabado_saida_2": f"{hora_sabado_saida_2}",
                                            "hora_domingo_entrada_1": f"{hora_domingo_entrada_1}",
                                            "hora_domingo_saida_1": f"{hora_domingo_saida_1}",
                                            "hora_domingo_entrada_2": f"{hora_domingo_entrada_2}",
                                            "hora_domingo_saida_2": f"{hora_domingo_saida_2}",
                                            "empresa_confirmacao": bool(False),
                                            "nome_empresa": abc['nome_empresa'],
                                            "admin": bool(False),
                                            "id_empresa": {
                                                '__type': "Pointer",
                                                "className": "Empresa",
                                                "objectId": empresa_id}
                                        })
        return redirect('criar_funcionario_sucesso', token=token)
    return render(request, 'criar_funcionario.html', {'lista': key})


def criar_funcionario_sucesso(request, token):
    conexao = requests.api.request('GET', 'https://parseapi.back4app.com/users/me', headers={
        "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
        "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
        "X-Parse-Session-Token": f"{token}"})
    abc = conexao.json()
    if str(abc['sessionToken']) != f"{token}":
        return redirect('login')
    elif abc['empresa_confirmacao'] == False:
        return redirect('login')
    else:
        pass
    key = [{'id': token, 'emp': abc['nome_empresa'], 'user': abc['username']}]
    return render(request, 'criar_funcionario_sucesso.html', {'lista': key})


def listar_funcionario(request, token, empresa):
    conexao = requests.api.request('GET', 'https://parseapi.back4app.com/users/me', headers={
        "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
        "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
        "X-Parse-Session-Token": f"{token}"})
    abc = conexao.json()
    if str(abc['sessionToken']) != f"{token}":
        return redirect('login')
    elif abc['empresa_confirmacao'] == False:
        return redirect('login')

    key = [{'id': token, 'emp': empresa, 'user': abc['username']}]
    empresa_id = abc['id_empresa']['objectId']
    
    conexao1 = requests.api.request('GET',
                                    f"https://parseapi.back4app.com/classes/_User?where=%7B%22nome_empresa%22%3A%20%22{empresa}%22%7D",
                                    headers={
                                        "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                                        "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9"})
    dop = conexao1.json()
    dap = [x for x in dop['results']]
    a = len(dap)
    [dap[x].update({'cod': token}) for x in range(a)]
    
    return render(request, 'listar_funcionario.html', {'lista': key, 'order': dap})


def exibir_perfil(request, token, empresa, id_user):
    conexao = requests.api.request('GET', 'https://parseapi.back4app.com/users/me', headers={
        "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
        "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
        "X-Parse-Session-Token": f"{token}"})
    abc = conexao.json()
    if str(abc['sessionToken']) != f"{token}":
        return redirect('login')
    elif abc['empresa_confirmacao'] == False:
        return redirect('login')
    key = [{'id': token, 'emp': empresa, 'id_user': abc['objectId']}]
    conexao1 = requests.api.request('GET', 
                                    f"https://parseapi.back4app.com/classes/_User?where=%7B%22nome_empresa%22%3A%20%22{empresa}%22%7D",
                                    headers={
                                        "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                                        "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9"})
    f = conexao1.json()
    funcionario = [x for x in f['results']]

    conexao2 = requests.api.request('GET',
                                    f"https://parseapi.back4app.com/classes/Ponto",
                                    headers={
                                        "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                                        "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9"})
    p = conexao2.json()
    ponto = [x for x in p['results']]

    for x in ponto:
        data = x['createdAt']
        data = data[:9]
        date = datetime.strptime(data, '%Y-%m-%d').date()
        date = date.strftime('%d/%m/%Y')
        x['createdAt'] = date

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    if start_date and end_date:
        start = datetime.strptime(start_date, '%Y-%m-%d').date()
        end = datetime.strptime(end_date, '%Y-%m-%d').date()
        dia_start = start.day
        mes_start = start.month
        ano_start = start.year
        dia_end = end.day
        mes_end = end.month
        ano_end = end.year

        lista = list(range(dia_start, dia_end + 1))
        a = len(lista)
        
        datas = tuple([f"0{lista[x]}" + '/' + f"0{mes_start}" + '/' + f"{ano_start}" if x < 10 else f"{lista[x]}" + '/' + f"{mes_start}" + '/' + f"{ano_start}" for x in range(a)])
        ponto_date = [{'createdAt': x['createdAt'], 'id_funcionario': {'objectId': x['id_funcionario']['objectId']}, 'horario': x['horario'], 'registro': x['registro'], 'local_registro': x['local_registro']} if str(x['createdAt']) in datas else {'createdAt': 'sem registro', 'id_funcionario': {'objectId': x['id_funcionario']['objectId']}, 'horario': 'sem registro', 'registro': 'sem registro', 'local_registro': 'sem registro'} for x in ponto]
    else:
        ponto_date = ponto
        start = "0"
        end = "0"
    
    return render(request, 'exibir_perfil.html', {'lista': key, 'funcionarios': funcionario, 'Id_user': id_user, 'pontos': ponto_date, 'start_data': start, 'end_data': end})


def gerar_relatorio_func(request, token):
    conexao = requests.api.request('GET', 'https://parseapi.back4app.com/users/me', headers={
        "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
        "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
        "X-Parse-Session-Token": f"{token}"})
    abc = conexao.json()
    if str(abc['sessionToken']) != f"{token}":
        return redirect('login')
    elif abc['empresa_confirmacao'] == False:
        return redirect('login')
    empresa = abc['nome_empresa']
    conexao1 = requests.api.request('GET',
                                    f"https://parseapi.back4app.com/classes/_User?where=%7B%22nome_empresa%22%3A%20%22{empresa}%22%7D",
                                    headers={
                                        "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                                        "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9"})
    dop = conexao1.json()
    dap = [x for x in dop['results']]

    return rendering.render_to_pdf_response(request=request,
                                            context={'funcionarios': dap},
                                            template='relatorio-funcionarios.html',
                                            encoding='utf-8')


def gerar_relatorio_ponto(request, token, empresa, id_user, start_date, end_date):
    conexao = requests.api.request('GET', 'https://parseapi.back4app.com/users/me', headers={
        "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
        "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
        "X-Parse-Session-Token": f"{token}"})
    abc = conexao.json()
    if str(abc['sessionToken']) != f"{token}":
        return redirect('login')
    elif abc['empresa_confirmacao'] == False:
        return redirect('login')

    conexao1 = requests.api.request('GET', 
                                    f"https://parseapi.back4app.com/classes/_User?where=%7B%22nome_empresa%22%3A%20%22{empresa}%22%7D",
                                    headers={
                                        "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                                        "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9"})
    f = conexao1.json()
    funcionario = [x for x in f['results']]

    conexao2 = requests.api.request('GET',
                                    f"https://parseapi.back4app.com/classes/Ponto",
                                    headers={
                                        "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                                        "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9"})
    p = conexao2.json()
    ponto = [x for x in p['results']]

    for x in ponto:
        data = x['createdAt']
        data = data[:9]
        date = datetime.strptime(data, '%Y-%m-%d').date()
        date = date.strftime('%d/%m/%Y')
        x['createdAt'] = date

    if start_date != "0" and end_date != "0":
        start = datetime.strptime(start_date, '%Y-%m-%d').date()
        end = datetime.strptime(end_date, '%Y-%m-%d').date()
        dia_start = start.day
        mes_start = start.month
        ano_start = start.year
        dia_end = end.day
        mes_end = end.month
        ano_end = end.year

        lista = list(range(dia_start, dia_end + 1))
        a = len(lista)
        
        datas = tuple([f"0{lista[x]}" + '/' + f"0{mes_start}" + '/' + f"{ano_start}" if x < 10 else f"{lista[x]}" + '/' + f"{mes_start}" + '/' + f"{ano_start}" for x in range(a)])
        ponto_date = [{'createdAt': x['createdAt'], 'id_funcionario': {'objectId': x['id_funcionario']['objectId']}, 'horario': x['horario'], 'registro': x['registro'], 'local_registro': x['local_registro']} if str(x['createdAt']) in datas else {'createdAt': 'sem registro', 'id_funcionario': {'objectId': x['id_funcionario']['objectId']}, 'horario': 'sem registro', 'registro': 'sem registro', 'local_registro': 'sem registro'} for x in ponto]
    else:
        ponto_date = ponto
        

    return rendering.render_to_pdf_response(request=request,
                                            context={'funcionarios': funcionario, 'Id_user': id_user, 'pontos': ponto_date},
                                            template='relatorio-pontos.html',
                                            encoding='utf-8')



# ÁREA ADMINISTRATIVA #

def base_admin(request, token):
    conexao = requests.api.request('GET', 'https://parseapi.back4app.com/users/me', headers={
        "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
        "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
        "X-Parse-Session-Token": f"{token}"})
    abc = conexao.json()
    if str(abc['sessionToken']) != f"{token}":
        return redirect('login')
    elif abc['admin'] == False:
        return redirect('login')
    else:
        pass
    conexao1 = requests.api.request('GET',
                                    f"https://parseapi.back4app.com/classes/_User",
                                    headers={
                                        "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                                        "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9"})
    dop = conexao1.json()
    dap = [x for x in dop['results']]
    dip = [{'numero_funcionario': len(dap)}]
    conexao2 = requests.api.request('GET', f"https://parseapi.back4app.com/classes/Empresa",
                                    headers={
                                        "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                                        "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
                                        "accept": "application/json"})

    dep = conexao2.json()
    dup = [{'numero_empresa': len(dep)}]
    key = [{'id': token, 'user': abc['username']}]
    return render(request, 'base_admin.html', {'lista': key, 'lista2': dip, 'lista3': dup})

  
def index_admin(request, token):
    conexao = requests.api.request('GET', 'https://parseapi.back4app.com/users/me', headers={
        "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
        "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
        "X-Parse-Session-Token": f"{token}"})
    abc = conexao.json()
    if str(abc['sessionToken']) != f"{token}":
        return redirect('login')
    elif abc['admin'] == False:
        return redirect('login')
    else:
        pass
    key = [{'id': token, 'user': abc['username']}]
    return render(request, 'index_admin.html', {'lista': key})


def listar_empresa(request, token):
    conexao = requests.api.request('GET', 'https://parseapi.back4app.com/users/me', headers={
        "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
        "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
        "X-Parse-Session-Token": f"{token}"})
    abc = conexao.json()
    if str(abc['sessionToken']) != f"{token}":
        return redirect('login')
    elif abc['admin'] == False:
        return redirect('login')
    else:
        pass
    conexao1 = requests.api.request('GET', f"https://parseapi.back4app.com/classes/Empresa",
                                    headers={
                                        "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                                        "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
                                        "accept": "application/json"})


    key = [{'id': token, 'user': abc['username']}]
    dop = conexao1.json()
    dap = [x for x in dop['results']]
    a = len(dap)
    [dap[x].update({'token': token}) for x in range(a)]
    return render(request, 'listar_empresa.html', {'lista': key, 'lista2': dap})


def ver_empresa(request, token, id):
    conexao = requests.api.request('GET', 'https://parseapi.back4app.com/users/me', headers={
        "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
        "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
        "X-Parse-Session-Token": f"{token}"})
    abc = conexao.json()
    if str(abc['sessionToken']) != f"{token}":
        return redirect('login')
    elif abc['admin'] == False:
        return redirect('login')
    else:
        pass
    conexao1 = requests.api.request('GET', f"https://parseapi.back4app.com/classes/Empresa?where=%7B%22objectId%22%3A%20%22{id}%22%7D",
                                    headers={
                                        "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                                        "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
                                        "accept": "application/json"})
    key = [{'id': token, 'user': abc['username']}]
    dop = conexao1.json()
    dap = [x for x in dop['results']]
    return render(request, 'ver_empresa.html', {'lista': key, 'lista2': dap})

