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
from dateutil.parser import *

from datetime import timedelta, date


def index(request, token):
    conexao = requests.api.request('GET', 'https://parseapi.back4app.com/users/me', headers={
        "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
        "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
        "X-Parse-Session-Token": f"{token}"})
    abc = conexao.json()
    if str(abc['sessionToken']) != f"{token}":
        return redirect('login')
    elif abc['empresa_confirmacao'] == False:
        return redirect('login')
    elif abc['admin'] == True:
        return redirect('login')
    else:
        pass
    key = [{'id': token, 'emp': abc['nome_empresa']}]
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
        if abp == '200' and abc['empresa_confirmacao'] == True:
            return redirect('base', token=abc['sessionToken'])
        elif abp == '200' and abc['admin'] == True:
            return redirect('base_admin', token=abc['sessionToken'])
        else:
            return redirect('login')
    return render(request, 'login.html')


def deslogar(request, token):
    requests.api.request('POST', 'https://parseapi.back4app.com/logout', headers={
        "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
        "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
        "X-Parse-Session-Token": f"{token}"})
    logout(request)
    return redirect('login')


def base(request, token):
    conexao = requests.api.request('GET', 'https://parseapi.back4app.com/users/me', headers={
        "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
        "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
        "X-Parse-Session-Token": f"{token}"})
    abc = conexao.json()
    if str(abc['sessionToken']) != f"{token}":
        return redirect('login')
    elif abc['empresa_confirmacao'] == False:
        return redirect('login')
    elif abc['admin'] == True:
        return redirect('login')
    else:
        pass
    key = [{'id': token, 'emp': abc['nome_empresa'], 'user': abc['username']}]
    return render(request, 'base.html', {'lista': key})


def criar_usuario(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        cpf = request.POST['cpf']
        nome = request.POST['nome']
        datanasc = request.POST['datanasc']
        email = request.POST['email']
        telefone = request.POST['telefone']
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
        abc = conexao1.json()
        aaa = str(conexao1.status_code)
        dee = abc['objectId']
        if aaa != '201':
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
                                            "telefone": f"{telefone}",
                                            "celular": f"{celular}",
                                            "cargo": f"{cargo}",
                                            "departamento": f"{departamento}",
                                            "empresa_confirmacao": bool(True),
                                            "nome_empresa": f"{nome_empresa}",
                                            "admin": bool(False),
                                            "id_empresa": {
                                                '__type': "Pointer",
                                                "className": "Empresa",
                                                "objectId": dee}
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
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        cpf = request.POST['cpf']
        nome = request.POST['nome']
        datanasc = request.POST['datanasc']
        email = request.POST['email']
        telefone = request.POST['telefone']
        celular = request.POST['celular']
        cargo = request.POST['cargo']
        departamento = request.POST['departamento']
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
                                            "telefone": f"{telefone}",
                                            "celular": f"{celular}",
                                            "cargo": f"{cargo}",
                                            "departamento": f"{departamento}",
                                            "empresa_confirmacao": bool(False),
                                            "nome_empresa": abc['nome_empresa'],
                                            "admin": bool(False),
                                            "id_empresa": {
                                                '__type': "Pointer",
                                                "className": "Empresa",
                                                "objectId": empresa}
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

    



    date_input = request.GET.get('date_input')
    conexao3 = requests.api.request('GET',
                                    f"https://parseapi.back4app.com/classes/Ponto?where=%7B%20%22createdAt%22%3A%20%22{date_input}%22%20%7D",
                                    headers={
                                        "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                                        "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9"})
    p_data = conexao3.json()
    ponto_por_data = [x for x in p_data['results']]
    
    
    return render(request, 'exibir_perfil.html', {'lista': key, 'funcionarios': funcionario, 'Id_user': id_user, 'pontos': ponto, 'pontos_data': ponto_por_data})


# ÁREA DO ADMINISTRADOR #
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
