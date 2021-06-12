from django.shortcuts import render
from django.contrib import auth as autent
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
import datetime
from datetime import *
from easy_pdf import rendering
from django.utils.six import BytesIO
import requests
import urllib3




def home(request):
    return render(request, 'home.html')


def login_colaborador(request):
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
        response = conexao.json()
        status = str(conexao.status_code)
        
        if status == '200' and response['admin'] == True:
            return redirect('base_admin', token=response['sessionToken'])
        elif status == '200' and response['empresa_confirmacao'] == True:
            return redirect('dashboard', token=response['sessionToken'])
        elif status == '200' and response['admin'] == True:
            return redirect('base_admin', token=response['sessionToken'])
        else:
            return redirect('login_fail')

    return render(request, 'login_colaborador.html')


def login_gestor(request):
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
        response = conexao.json()
        status = str(conexao.status_code)
        
        if status == '200' and response['admin'] == True:
            return redirect('base_admin', token=response['sessionToken'])
        elif status == '200' and response['empresa_confirmacao'] == True:
            return redirect('dashboard', token=response['sessionToken'])
        elif status == '200' and response['admin'] == True:
            return redirect('base_admin', token=response['sessionToken'])
        else:
            return redirect('login_fail')

    return render(request, 'login_gestor.html')


def login_fail(request):
    return render(request, 'fail_login.html')


def deslogar(request, token):
    requests.api.request('GET', 'https://parseapi.back4app.com/logout', headers={
        "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
        "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
        "X-Parse-Session-Token": f"{token}"})
    logout(request)
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
        conexao.json()
        status = str(conexao.status_code)
        
        if status == '200':
            return redirect('redefinir_senha_success')
        else:
            return redirect('redefinir_senha_fail')

    return render(request, 'redefinir_senha.html')


def redefinir_senha_success(request):
    return render(request, 'success_redefinir_senha.html')


def redefinir_senha_fail(request):
    return render(request, 'fail_redefinir_senha.html')


def register(request):
    if request.method == 'POST':
        # Dados do Usuário
        username = request.POST['username']
        password = request.POST['password']
        cpf = request.POST['cpf']
        # Dados da Empresa
        cnpj = request.POST['cnpj']
        razaosocial = request.POST['razaosocial']
        # Endereço da Empresa
        cep = request.POST['cep']
        uf = request.POST['uf']
        cidade = request.POST['cidade']
        logradouro = request.POST['logradouro']
        bairro = request.POST['bairro']
        numero = request.POST['numero']
        
        req_emp = requests.api.request('POST', f"https://parseapi.back4app.com/classes/Empresa/",
                                        headers={
                                            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                                            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
                                            "Context-Type": "application/json"},
                                        json={
                                            "cnpj": f"{cnpj}",
                                            "razaosocial": f"{razaosocial}",
                                            "cep": f"{cep}",
                                            "uf": f"{uf}",
                                            "logradouro": f"{logradouro}",
                                            "numero": f"{numero}",
                                            "cidade": f"{cidade}",
                                            "bairro": f"{bairro}",
                                        })
        empresa = req_emp.json()
        status = str(req_emp.status_code)
        empresa_id = empresa['objectId']

        if status != '201':
            return redirect('login')

        req_user = requests.api.request('POST', f"https://parseapi.back4app.com/users",
                                        headers={"X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                                                 "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
                                                 "X-Parse-Revocable-Session": "1",
                                                 "Content-Type": "application/json"},
                                        json={
                                            "username": f"{username}",
                                            "password": f"{password}",
                                            "cpf": f"{cpf}",
                                            "empresa_confirmacao": bool(True),
                                            "admin": bool(False),
                                            "id_empresa": {
                                                '__type': "Pointer",
                                                "className": "Empresa",
                                                "objectId": empresa_id}
                                        })
        req_user.json()
        status = str(req_user.status_code)
        if status == '201':
            return redirect('register_success')
        else:
            return redirect('login')

    return render(request, 'register.html')


def register_success(request):
    return render(request, 'success_register.html')


def dashboard(request, token):
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
    key = [{'id': token, 'user': usuario['username']}]

    return render(request, 'dashboard.html', {'lista': key})


def fail_default(request, token):
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
    key = [{'id': token, 'user': usuario['username']}]

    return render(request, 'fail_default.html', {'lista': key})


# EMPREGADOR
def edit_empresa(request, token):
    conexao = requests.api.request('GET', 'https://parseapi.back4app.com/users/me',
                                    headers={"X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                                        "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
                                        "X-Parse-Session-Token": f"{token}"})
    response = conexao.json()
    if str(response['sessionToken']) != f"{token}":
        return redirect('login')
    elif response['empresa_confirmacao'] == False:
        return redirect('login')
    else:
        pass
    key = [{'id': token, 'user': response['username']}]
    empresa_id = response['id_empresa']['objectId']
    
    req_emp = requests.api.request('GET', f"https://parseapi.back4app.com/classes/Empresa/{empresa_id}",
                                    headers={
                                        "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                                        "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9"})
    emp = req_emp.json()

    if request.method == 'POST':
        # Dados da Empresa
        nome_empresa = request.POST['nome_empresa']
        cnpj = request.POST['cnpj']
        ie = request.POST['ie']
        razaosocial = request.POST['razaosocial']
        atividade = request.POST['atividade']
        tel_comercial = request.POST['tel_comercial']
        celular_empresa = request.POST['celular_empresa']
        email_empresa = request.POST['email_empresa']
        # Endereço da Empresa
        cep = request.POST['cep']
        uf = request.POST['uf']
        cidade = request.POST['cidade']
        logradouro = request.POST['logradouro']
        bairro = request.POST['bairro']
        numero = request.POST['numero']
        
        req_emp = requests.api.request('PUT', f"https://parseapi.back4app.com/classes/Empresa/{empresa_id}",
                                        headers={
                                            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                                            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
                                            "Content-Type": "application/json"},
                                        json={
                                            "nome_empresa": f"{nome_empresa}",
                                            "cnpj": f"{cnpj}",
                                            "ie": f"{ie}",
                                            "razaosocial": f"{razaosocial}",
                                            "atividade": f"{atividade}",
                                            "tel_comercial": f"{tel_comercial}",
                                            "celular_empresa": f"{celular_empresa}",
                                            "email_empresa": f"{email_empresa}",
                                            "cep": f"{cep}",
                                            "uf": f"{uf}",
                                            "cidade": f"{cidade}",
                                            "logradouro": f"{logradouro}",
                                            "bairro": f"{bairro}",
                                            "numero": f"{numero}",
                                        })

        status = str(req_emp.status_code)
        if status == '200':
            return redirect('edit_empresa_success', token=token)
        else:
            return redirect('edit_empresa_fail', token=token)

    return render(request, 'edit_empresa.html', {'lista': key, 'empresa': emp })


def edit_empresa_success(request, token):
    conexao = requests.api.request('GET', 'https://parseapi.back4app.com/users/me',
                                    headers={"X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                                        "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
                                        "X-Parse-Session-Token": f"{token}"})
    response = conexao.json()
    if str(response['sessionToken']) != f"{token}":
        return redirect('login')
    elif response['empresa_confirmacao'] == False:
        return redirect('login')
    else:
        pass
    key = [{'id': token, 'user': response['username']}]

    return render(request, 'success_edit_empresa.html', {'lista': key})


def edit_empresa_fail(request, token):
    conexao = requests.api.request('GET', 'https://parseapi.back4app.com/users/me',
                                    headers={"X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                                        "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
                                        "X-Parse-Session-Token": f"{token}"})
    response = conexao.json()
    if str(response['sessionToken']) != f"{token}":
        return redirect('login')
    elif response['empresa_confirmacao'] == False:
        return redirect('login')
    else:
        pass
    key = [{'id': token, 'user': response['username']}]

    return render(request, 'fail_edit_empresa.html', {'lista': key})


def list_departamento(request, token):
    conexao = requests.api.request('GET', 'https://parseapi.back4app.com/users/me',
                                    headers={"X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                                        "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
                                        "X-Parse-Session-Token": f"{token}"})
    response = conexao.json()
    if str(response['sessionToken']) != f"{token}":
        return redirect('login')
    elif response['empresa_confirmacao'] == False:
        return redirect('login')
    else:
        pass
    key = [{'id': token, 'user': response['username']}]
    empresa_id = response['id_empresa']['objectId']

    req_dep = requests.api.request('GET', f"https://parseapi.back4app.com/classes/Departamento?where=%7B%22id_empresa%22%3A%20%7B%20%22__type%22%3A%20%22Pointer%22%2C%20%22className%22%3A%20%22Empresa%22%2C%20%22objectId%22%3A%20%22{empresa_id}%22%20%7D%20%7D",
                                    headers={
                                        "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                                        "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9"})
    res_dep = req_dep.json()
    departamento = [x for x in res_dep['results']]

    return render(request, 'list_departamento.html', {'lista': key, 'departamentos': departamento})


def cadastro_departamento(request, token):
    conexao = requests.api.request('GET', 'https://parseapi.back4app.com/users/me',
                                    headers={"X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                                        "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
                                        "X-Parse-Session-Token": f"{token}"})
    response = conexao.json()
    if str(response['sessionToken']) != f"{token}":
        return redirect('login')
    elif response['empresa_confirmacao'] == False:
        return redirect('login')
    else:
        pass
    key = [{'id': token, 'user': response['username']}]
    empresa_id = response['id_empresa']['objectId']

    if request.method == 'POST':
        nome = request.POST['nome_departamento']

        req_dep = requests.api.request('POST', f"https://parseapi.back4app.com/classes/Departamento",
                                        headers={
                                            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                                            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
                                            "Content-Type": "application/json"},
                                        json={
                                            "nome": f"{nome}",
                                            "id_empresa": {
                                                '__type': "Pointer",
                                                "className": "Empresa",
                                                "objectId": empresa_id
                                            }})
        status = str(req_dep.status_code)
        if status == '201':
            return redirect('list_departamento', token=token)
        else:
            return redirect('fail_default', token=token)

    return render(request, 'cadastro_departamento.html', {'lista': key})


def edit_departamento(request, token, id):
    conexao = requests.api.request('GET', 'https://parseapi.back4app.com/users/me',
                                    headers={"X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                                        "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
                                        "X-Parse-Session-Token": f"{token}"})
    response = conexao.json()
    if str(response['sessionToken']) != f"{token}":
        return redirect('login')
    elif response['empresa_confirmacao'] == False:
        return redirect('login')
    else:
        pass
    key = [{'id': token, 'user': response['username']}]
    empresa_id = response['id_empresa']['objectId']

    req_dep = requests.api.request('GET', f"https://parseapi.back4app.com/classes/Departamento/{id}",
                                    headers={
                                        "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                                        "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9"})
    dep = req_dep.json()

    if request.method == 'POST':
        nome = request.POST['nome_departamento']

        req_dep = requests.api.request('PUT', f"https://parseapi.back4app.com/classes/Departamento/{id}",
                                        headers={
                                            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                                            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
                                            "Content-Type": "application/json"},
                                        json={
                                            "nome": f"{nome}",
                                            "id_empresa": {
                                                '__type': "Pointer",
                                                "className": "Empresa",
                                                "objectId": empresa_id
                                            }})
        status = str(req_dep.status_code)
        if status == '200':
            return redirect('list_departamento', token=token)
        else:
            return redirect('fail_default', token=token)

    return render(request, 'edit_departamento.html', {'lista': key, 'departamento': dep})


def delete_departamento(request, token, id):
    conexao = requests.api.request('GET', 'https://parseapi.back4app.com/users/me',
                                    headers={"X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                                        "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
                                        "X-Parse-Session-Token": f"{token}"})
    response = conexao.json()
    if str(response['sessionToken']) != f"{token}":
        return redirect('login')
    elif response['empresa_confirmacao'] == False:
        return redirect('login')
    else:
        pass

    req_dep = requests.api.request('DELETE', f"https://parseapi.back4app.com/classes/Departamento/{id}",
                                    headers={
                                        "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                                        "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9"})

    status = str(req_dep.status_code)
    if status == '200':
        return redirect('list_departamento', token=token)
    else:
        return redirect('fail_default', token=token)


def list_feriado(request, token):
    conexao = requests.api.request('GET', 'https://parseapi.back4app.com/users/me',
                                    headers={"X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                                        "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
                                        "X-Parse-Session-Token": f"{token}"})
    response = conexao.json()
    if str(response['sessionToken']) != f"{token}":
        return redirect('login')
    elif response['empresa_confirmacao'] == False:
        return redirect('login')
    else:
        pass
    key = [{'id': token, 'user': response['username']}]

    return render(request, 'list_feriado.html', {'lista': key})


# HORÁRIOS
def list_horario(request, token):
    conexao = requests.api.request('GET', 'https://parseapi.back4app.com/users/me',
                                    headers={"X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                                        "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
                                        "X-Parse-Session-Token": f"{token}"})
    response = conexao.json()
    if str(response['sessionToken']) != f"{token}":
        return redirect('login')
    elif response['empresa_confirmacao'] == False:
        return redirect('login')
    else:
        pass
    key = [{'id': token, 'user': response['username']}]
    empresa_id = response['id_empresa']['objectId']

    req_horario = requests.api.request('GET', f"https://parseapi.back4app.com/classes/Horario?where=%7B%20%22id_empresa%22%3A%20%7B%20%22__type%22%3A%20%22Pointer%22%2C%20%22className%22%3A%20%22Empresa%22%2C%20%22objectId%22%3A%20%22{empresa_id}%22%20%7D%20%7D",
                                        headers={"X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                                            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9"})
    res_horario = req_horario.json()
    horario = [x for x in res_horario['results']]

    return render(request, 'list_horario.html', {'lista': key, 'horarios': horario})


def cadastro_horario(request, token):
    conexao = requests.api.request('GET', 'https://parseapi.back4app.com/users/me',
                                    headers={"X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                                        "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
                                        "X-Parse-Session-Token": f"{token}"})
    response = conexao.json()
    if str(response['sessionToken']) != f"{token}":
        return redirect('login')
    elif response['empresa_confirmacao'] == False:
        return redirect('login')
    else:
        pass
    key = [{'id': token, 'user': response['username']}]
    empresa_id = response['id_empresa']['objectId']

    req_dep = requests.api.request('GET', f"https://parseapi.back4app.com/classes/Departamento?where=%7B%22id_empresa%22%3A%20%7B%20%22__type%22%3A%20%22Pointer%22%2C%20%22className%22%3A%20%22Empresa%22%2C%20%22objectId%22%3A%20%22{empresa_id}%22%20%7D%20%7D",
                                    headers={
                                        "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                                        "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9"})
    res_dep = req_dep.json()
    departamento = [x for x in res_dep['results']]

    if request.method == 'POST':
        nome = request.POST['nome_horario']
        departamento_id = request.POST['departamento']
        inicio_periodo_manha = request.POST['inicio_periodo_manha']
        fim_periodo_manha = request.POST['fim_periodo_manha']
        inicio_periodo_tarde = request.POST['inicio_periodo_tarde']
        fim_periodo_tarde = request.POST['fim_periodo_tarde']
        segunda = request.POST.get('segunda', False)
        terca = request.POST.get('terca', False)
        quarta = request.POST.get('quarta', False)
        quinta = request.POST.get('quinta', False)
        sexta = request.POST.get('sexta', False)
        sabado = request.POST.get('sabado', False)
        domingo = request.POST.get('domingo', False)

        req_horario = requests.api.request('POST', f"https://parseapi.back4app.com/classes/Horario",
                                        headers={
                                            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                                            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
                                            "Content-Type": "application/json"},
                                        json={
                                            "nome": f"{nome}",
                                            "inicio_periodo_manha": f"{inicio_periodo_manha}",
                                            "fim_periodo_manha": f"{fim_periodo_manha}",
                                            "inicio_periodo_tarde": f"{inicio_periodo_tarde}",
                                            "fim_periodo_tarde": f"{fim_periodo_tarde}",
                                            "segunda": bool(segunda),
                                            "terca": bool(terca),
                                            "quarta": bool(quarta),
                                            "quinta": bool(quinta),
                                            "sexta": bool(sexta),
                                            "sabado": bool(sabado),
                                            "domingo": bool(domingo),
                                            "id_empresa": {
                                                '__type': "Pointer",
                                                "className": "Empresa",
                                                "objectId": empresa_id
                                            },
                                            "id_departamento": {
                                                '__type': "Pointer",
                                                "className": "Departamento",
                                                "objectId": departamento_id
                                            }})
        status = str(req_horario.status_code)
        if status == '201':
            return redirect('list_horario', token=token)
        else:
            return redirect('fail_default', token=token)

    return render(request, 'cadastro_horario.html', {'lista': key, 'departamentos': departamento})


def edit_horario(request, token, id):
    conexao = requests.api.request('GET', 'https://parseapi.back4app.com/users/me',
                                    headers={"X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                                        "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
                                        "X-Parse-Session-Token": f"{token}"})
    response = conexao.json()
    if str(response['sessionToken']) != f"{token}":
        return redirect('login')
    elif response['empresa_confirmacao'] == False:
        return redirect('login')
    else:
        pass
    key = [{'id': token, 'user': response['username']}]
    empresa_id = response['id_empresa']['objectId']

    req_dep = requests.api.request('GET', f"https://parseapi.back4app.com/classes/Departamento?where=%7B%22id_empresa%22%3A%20%7B%20%22__type%22%3A%20%22Pointer%22%2C%20%22className%22%3A%20%22Empresa%22%2C%20%22objectId%22%3A%20%22{empresa_id}%22%20%7D%20%7D",
                                    headers={
                                        "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                                        "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9"})
    res_dep = req_dep.json()
    departamento = [x for x in res_dep['results']]

    req_horario = requests.api.request('GET', f"https://parseapi.back4app.com/classes/Horario/{id}",
                                        headers={"X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                                            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9"})
    hor = req_horario.json()

    if request.method == 'POST':
        nome = request.POST['nome_horario']
        departamento_id = request.POST['departamento']
        inicio_periodo_manha = request.POST['inicio_periodo_manha']
        fim_periodo_manha = request.POST['fim_periodo_manha']
        inicio_periodo_tarde = request.POST['inicio_periodo_tarde']
        fim_periodo_tarde = request.POST['fim_periodo_tarde']
        segunda = request.POST.get('segunda', False)
        terca = request.POST.get('terca', False)
        quarta = request.POST.get('quarta', False)
        quinta = request.POST.get('quinta', False)
        sexta = request.POST.get('sexta', False)
        sabado = request.POST.get('sabado', False)
        domingo = request.POST.get('domingo', False)

        req_dep = requests.api.request('PUT', f"https://parseapi.back4app.com/classes/Horario/{id}",
                                        headers={
                                            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                                            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
                                            "Content-Type": "application/json"},
                                        json={
                                            "nome": f"{nome}",
                                            "inicio_periodo_manha": f"{inicio_periodo_manha}",
                                            "fim_periodo_manha": f"{fim_periodo_manha}",
                                            "inicio_periodo_tarde": f"{inicio_periodo_tarde}",
                                            "fim_periodo_tarde": f"{fim_periodo_tarde}",
                                            "segunda": bool(segunda),
                                            "terca": bool(terca),
                                            "quarta": bool(quarta),
                                            "quinta": bool(quinta),
                                            "sexta": bool(sexta),
                                            "sabado": bool(sabado),
                                            "domingo": bool(domingo),
                                            "id_empresa": {
                                                '__type': "Pointer",
                                                "className": "Empresa",
                                                "objectId": empresa_id
                                            },
                                            "id_departamento": {
                                                '__type': "Pointer",
                                                "className": "Departamento",
                                                "objectId": departamento_id
                                            }})
        status = str(req_dep.status_code)
        if status == '200':
            return redirect('list_horario', token=token)
        else:
            return redirect('fail_default', token=token)

    return render(request, 'edit_horario.html', {'lista': key, 'horario': hor, 'departamentos': departamento})


def delete_horario(request, token, id):
    conexao = requests.api.request('GET', 'https://parseapi.back4app.com/users/me',
                                    headers={"X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                                        "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
                                        "X-Parse-Session-Token": f"{token}"})
    response = conexao.json()
    if str(response['sessionToken']) != f"{token}":
        return redirect('login')
    elif response['empresa_confirmacao'] == False:
        return redirect('login')
    else:
        pass

    req_hor = requests.api.request('DELETE', f"https://parseapi.back4app.com/classes/Horario/{id}",
                                    headers={
                                        "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                                        "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9"})

    status = str(req_hor.status_code)
    if status == '200':
        return redirect('list_horario', token=token)
    else:
        return redirect('fail_default', token=token)


# LOCAIS
def list_local(request, token):
    conexao = requests.api.request('GET', 'https://parseapi.back4app.com/users/me',
                                    headers={"X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                                        "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
                                        "X-Parse-Session-Token": f"{token}"})
    response = conexao.json()
    if str(response['sessionToken']) != f"{token}":
        return redirect('login')
    elif response['empresa_confirmacao'] == False:
        return redirect('login')
    else:
        pass
    key = [{'id': token, 'user': response['username']}]

    return render(request, 'list_local.html', {'lista': key})


def cadastro_local(request, token):
    conexao = requests.api.request('GET', 'https://parseapi.back4app.com/users/me',
                                    headers={"X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                                        "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
                                        "X-Parse-Session-Token": f"{token}"})
    response = conexao.json()
    if str(response['sessionToken']) != f"{token}":
        return redirect('login')
    elif response['empresa_confirmacao'] == False:
        return redirect('login')
    else:
        pass
    key = [{'id': token, 'user': response['username']}]

    return render(request, 'cadastro_local.html', {'lista': key})


# COLABORADORES
def list_cargo(request, token):
    conexao = requests.api.request('GET', 'https://parseapi.back4app.com/users/me',
                                    headers={"X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                                        "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
                                        "X-Parse-Session-Token": f"{token}"})
    response = conexao.json()
    if str(response['sessionToken']) != f"{token}":
        return redirect('login')
    elif response['empresa_confirmacao'] == False:
        return redirect('login')
    else:
        pass
    key = [{'id': token, 'user': response['username']}]
    empresa_id = response['id_empresa']['objectId']

    req_cargo = requests.api.request('GET', f"https://parseapi.back4app.com/classes/Cargo?where=%7B%22id_empresa%22%3A%20%7B%20%22__type%22%3A%20%22Pointer%22%2C%20%22className%22%3A%20%22Empresa%22%2C%20%22objectId%22%3A%20%22{empresa_id}%22%20%7D%20%7D",
                                    headers={
                                        "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                                        "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9"})
    res_cargo = req_cargo.json()
    cargo = [x for x in res_cargo['results']]

    return render(request, 'list_cargo.html', {'lista': key, 'cargos': cargo})


def cadastro_cargo(request, token):
    conexao = requests.api.request('GET', 'https://parseapi.back4app.com/users/me',
                                    headers={"X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                                        "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
                                        "X-Parse-Session-Token": f"{token}"})
    response = conexao.json()
    if str(response['sessionToken']) != f"{token}":
        return redirect('login')
    elif response['empresa_confirmacao'] == False:
        return redirect('login')
    else:
        pass
    key = [{'id': token, 'user': response['username']}]
    empresa_id = response['id_empresa']['objectId']

    if request.method == 'POST':
        nome = request.POST['nome_cargo']

        req_cargo = requests.api.request('POST', f"https://parseapi.back4app.com/classes/Cargo",
                                        headers={
                                            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                                            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
                                            "Content-Type": "application/json"},
                                        json={
                                            "nome": f"{nome}",
                                            "id_empresa": {
                                                '__type': "Pointer",
                                                "className": "Empresa",
                                                "objectId": empresa_id
                                            }})
        status = str(req_cargo.status_code)
        if status == '201':
            return redirect('list_cargo', token=token)
        else:
            return redirect('fail_default', token=token)

    return render(request, 'cadastro_cargo.html', {'lista': key})


def edit_cargo(request, token, id):
    conexao = requests.api.request('GET', 'https://parseapi.back4app.com/users/me',
                                    headers={"X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                                        "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
                                        "X-Parse-Session-Token": f"{token}"})
    response = conexao.json()
    if str(response['sessionToken']) != f"{token}":
        return redirect('login')
    elif response['empresa_confirmacao'] == False:
        return redirect('login')
    else:
        pass
    key = [{'id': token, 'user': response['username']}]
    empresa_id = response['id_empresa']['objectId']

    req_carg = requests.api.request('GET', f"https://parseapi.back4app.com/classes/Cargo/{id}",
                                    headers={
                                        "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                                        "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9"})
    carg = req_carg.json()

    if request.method == 'POST':
        nome = request.POST['nome_cargo']

        req_dep = requests.api.request('PUT', f"https://parseapi.back4app.com/classes/Cargo/{id}",
                                        headers={
                                            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                                            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
                                            "Content-Type": "application/json"},
                                        json={
                                            "nome": f"{nome}",
                                            "id_empresa": {
                                                '__type': "Pointer",
                                                "className": "Empresa",
                                                "objectId": empresa_id
                                            }})
        status = str(req_dep.status_code)
        if status == '200':
            return redirect('list_cargo', token=token)
        else:
            return redirect('fail_default', token=token)

    return render(request, 'edit_cargo.html', {'lista': key, 'cargo': carg})


def list_colaborador(request, token):
    conexao = requests.api.request('GET', 'https://parseapi.back4app.com/users/me',
                                    headers={"X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                                        "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
                                        "X-Parse-Session-Token": f"{token}"})
    response = conexao.json()
    if str(response['sessionToken']) != f"{token}":
        return redirect('login')
    elif response['empresa_confirmacao'] == False:
        return redirect('login')
    else:
        pass
    key = [{'id': token, 'user': response['username']}]
    empresa_id = response['id_empresa']['objectId']
    
    req_user = requests.api.request('GET', f"https://parseapi.back4app.com/classes/_User",
                                    headers={
                                        "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                                        "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9"})
    res_user = req_user.json()
    colaborador = [x for x in res_user['results']]
    total_colaborador = len(colaborador)
    [colaborador[x].update({'cod': token}) for x in range(total_colaborador)]
    
    return render(request, 'list_colaborador.html', {'lista': key, 'order': colaborador, 'id_emp': empresa_id})


def cadastro_colaborador(request, token):
    conexao = requests.api.request('GET', 'https://parseapi.back4app.com/users/me',
                                    headers={
                                        "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                                        "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
                                        "X-Parse-Session-Token": f"{token}"})

    response = conexao.json()
    if str(response['sessionToken']) != f"{token}":
        return redirect('login')
    elif response['empresa_confirmacao'] == False:
        return redirect('login')
    else:
        pass

    key = [{'id': token, 'user': response['username']}]
    empresa_id = response['id_empresa']['objectId']

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

        req_user = requests.api.request('POST', f"https://parseapi.back4app.com/users",
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
                                            "nome_empresa": response['nome_empresa'],
                                            "admin": bool(False),
                                            "id_empresa": {
                                                '__type': "Pointer",
                                                "className": "Empresa",
                                                "objectId": empresa_id}
                                        })

        req_user.json()
        status = str(req_user.status_code)
        if status != '201':
            return redirect('dashboard')
        else:
            return redirect('cadastro_colaborador_success', token=token)

    return render(request, 'cadastro_colaborador.html', {'lista': key})


def cadastro_colaborador_success(request, token):
    conexao = requests.api.request('GET', 'https://parseapi.back4app.com/users/me',
                                    headers={"X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                                            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
                                            "X-Parse-Session-Token": f"{token}"})

    response = conexao.json()
    if str(response['sessionToken']) != f"{token}":
        return redirect('login')
    elif response['empresa_confirmacao'] == False:
        return redirect('login')
    else:
        pass
    key = [{'id': token, 'user': response['username']}]
    return render(request, 'cadastro_colaborador_success.html', {'lista': key})


def list_demitidos(request, token):
    conexao = requests.api.request('GET', 'https://parseapi.back4app.com/users/me',
                                    headers={"X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                                        "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
                                        "X-Parse-Session-Token": f"{token}"})
    response = conexao.json()
    if str(response['sessionToken']) != f"{token}":
        return redirect('login')
    elif response['empresa_confirmacao'] == False:
        return redirect('login')
    else:
        pass
    key = [{'id': token, 'user': response['username']}]

    return render(request, 'list_demitidos.html', {'lista': key})


def pontos_colaborador(request, token, id_user):
    conexao = requests.api.request('GET', 'https://parseapi.back4app.com/users/me',
                                    headers={"X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                                        "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
                                        "X-Parse-Session-Token": f"{token}"})
    response = conexao.json()
    if str(response['sessionToken']) != f"{token}":
        return redirect('login')
    elif response['empresa_confirmacao'] == False:
        return redirect('login')
    else:
        pass
    key = [{'id': token, 'user': response['username']}]
    empresa_id = response['id_empresa']['objectId']

    req_user = requests.api.request('GET', f"https://parseapi.back4app.com/classes/_User",
                                    headers={
                                        "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                                        "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9"})
    res_user = req_user.json()
    colaborador = [x for x in res_user['results']]

    req_ponto = requests.api.request('GET', f"https://parseapi.back4app.com/classes/Ponto",
                                    headers={
                                        "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                                        "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9"})
    res_ponto = req_ponto.json()
    ponto = [x for x in res_ponto['results']]

    for x in ponto:
        data = x['createdAt']
        data = data[:10]
        date = datetime.strptime(data, '%Y-%m-%d').date()
        date = date.strftime('%d/%m/%Y')
        x['createdAt'] = date

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    if start_date and end_date:
        start = datetime.strptime(start_date, '%Y-%m-%d').date()
        end = datetime.strptime(end_date, '%Y-%m-%d').date()
        start_data = start.strftime('%d/%m/%Y')
        end_data = end.strftime('%d/%m/%Y')
        dia_start = start_data.day
        mes_start = start_data.month
        ano_start = start_data.year
        dia_end = end_data.day
        mes_end = end_data.month
        ano_end = end_data.year

        if mes_start == mes_end:
            if mes_start < 10:
                mes_start = f"0{mes_start}"

            lista = list(range(dia_start, dia_end + 1))
            a = len(lista)
            
            datas = tuple([f"0{lista[x]}" + '/' + f"{mes_start}" + '/' + f"{ano_start}" if lista[x] < 10 else f"{lista[x]}" + '/' + f"{mes_start}" + '/' + f"{ano_start}" for x in range(a)])
        elif mes_start < mes_end:
            if mes_start < 10:
                mes_start = f"0{mes_start}"
            if mes_end < 10:
                mes_end = f"0{mes_end}"

            lista = list(range(dia_start, 32))
            lista2 = list(range(1, dia_end + 1))
            a = len(lista)
            a2 = len(lista2)

            datas = tuple([f"0{lista[x]}" + '/' + f"{mes_start}" + '/' + f"{ano_start}" if lista[x] < 10 else f"{lista[x]}" + '/' + f"{mes_start}" + '/' + f"{ano_start}" for x in range(a)])
            datas2 = tuple([f"0{lista2[x]}" + '/' + f"{mes_end}" + '/' + f"{ano_end}" if lista2[x] < 10 else f"{lista2[x]}" + '/' + f"{mes_end}" + '/' + f"{ano_end}" for x in range(a2)])
            datas += datas2
        
        ponto_date = [{'createdAt': x['createdAt'], 'id_funcionario': {'objectId': x['id_funcionario']['objectId']}, 'horario': x['horario'], 'registro': x['registro'], 'local_registro': x['local_registro']} if str(x['createdAt']) in datas else {'createdAt': 'sem registro', 'id_funcionario': {'objectId': 'sem registro'}, 'horario': 'sem registro', 'registro': 'sem registro', 'local_registro': 'sem registro'} for x in ponto]
    else:
        ponto_date = ponto
        start = "0"
        end = "0"
    
    return render(request, 'pontos_colaborador.html', {'lista': key, 'colaboradores': colaborador, 'id_emp': empresa_id, 'Id_user': id_user, 'pontos': ponto_date, 'start_data': start, 'end_data': end})


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
    empresa_id = abc['id_empresa']['objectId']
    conexao1 = requests.api.request('GET',
                                    f"https://parseapi.back4app.com/classes/_User",
                                    headers={
                                        "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                                        "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9"})
    f = conexao1.json()
    funcionario = [x for x in f['results']]

    conexao2 = requests.api.request('GET', f"https://parseapi.back4app.com/classes/Empresa?where=%7B%22objectId%22%3A%20%22{empresa_id}%22%7D",
                                    headers={
                                        "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                                        "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
                                        "accept": "application/json"})
    e = conexao2.json()
    emp = [x for x in e['results']]

    return rendering.render_to_pdf_response(request=request,
                                            context={'funcionarios': funcionario, 'empresa': emp, 'id_emp': empresa_id},
                                            template='relatorio-funcionarios.html',
                                            encoding='utf-8')


def gerar_relatorio_ponto(request, token, id_user, start_date, end_date):
    conexao = requests.api.request('GET', 'https://parseapi.back4app.com/users/me', headers={
        "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
        "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
        "X-Parse-Session-Token": f"{token}"})
    abc = conexao.json()
    if str(abc['sessionToken']) != f"{token}":
        return redirect('login')
    elif abc['empresa_confirmacao'] == False:
        return redirect('login')
    empresa_id = abc['id_empresa']['objectId']
    conexao1 = requests.api.request('GET', 
                                    f"https://parseapi.back4app.com/classes/_User",
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
        data = data[:10]
        date = datetime.strptime(data, '%Y-%m-%d').date()
        date = date.strftime('%d/%m/%Y')
        x['createdAt'] = date

    if start_date != "0" and end_date != "0":
        start = datetime.strptime(start_date, '%Y-%m-%d').date()
        end = datetime.strptime(end_date, '%Y-%m-%d').date()
        start_data = start.strftime('%d/%m/%Y')
        end_data = end.strftime('%d/%m/%Y')
        dia_start = start.day
        mes_start = start.month
        ano_start = start.year
        dia_end = end.day
        mes_end = end.month
        ano_end = end.year

        if mes_start == mes_end:
            if mes_start < 10:
                mes_start = f"0{mes_start}"

            lista = list(range(dia_start, dia_end + 1))
            a = len(lista)
            
            datas = tuple([f"0{lista[x]}" + '/' + f"{mes_start}" + '/' + f"{ano_start}" if lista[x] < 10 else f"{lista[x]}" + '/' + f"{mes_start}" + '/' + f"{ano_start}" for x in range(a)])
        elif mes_start < mes_end:
            if mes_start < 10:
                mes_start = f"0{mes_start}"
            if mes_end < 10:
                mes_end = f"0{mes_end}"

            lista = list(range(dia_start, 32))
            lista2 = list(range(1, dia_end + 1))
            a = len(lista)
            a2 = len(lista2)

            datas = tuple([f"0{lista[x]}" + '/' + f"{mes_start}" + '/' + f"{ano_start}" if lista[x] < 10 else f"{lista[x]}" + '/' + f"{mes_start}" + '/' + f"{ano_start}" for x in range(a)])
            datas2 = tuple([f"0{lista2[x]}" + '/' + f"{mes_end}" + '/' + f"{ano_end}" if lista2[x] < 10 else f"{lista2[x]}" + '/' + f"{mes_end}" + '/' + f"{ano_end}" for x in range(a2)])
            datas += datas2
        
        ponto_date = [{'createdAt': x['createdAt'], 'id_funcionario': {'objectId': x['id_funcionario']['objectId']}, 'horario': x['horario'], 'registro': x['registro'], 'local_registro': x['local_registro']} if str(x['createdAt']) in datas else {'createdAt': 'sem registro', 'id_funcionario': {'objectId': 'sem registro'}, 'horario': 'sem registro', 'registro': 'sem registro', 'local_registro': 'sem registro'} for x in ponto]
    else:
        ponto_date = ponto
        

    return rendering.render_to_pdf_response(request=request,
                                            context={'funcionarios': funcionario, 'Id_user': id_user, 'id_emp': empresa_id, 'pontos': ponto_date},
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
    user = conexao1.json()
    usuario = [x for x in user['results']]
    num_usuario = [{'numero_usuario': len(usuario) - 1}]
    conexao2 = requests.api.request('GET', f"https://parseapi.back4app.com/classes/Empresa",
                                    headers={
                                        "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                                        "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
                                        "accept": "application/json"})

    emp = conexao2.json()
    empresa = [x for x in emp['results']]
    num_empresa = [{'numero_empresa': len(empresa)}]
    key = [{'id': token, 'user': abc['username']}]

    return render(request, 'admin_base.html', {'lista': key, 'usuarios': num_usuario, 'empresas': num_empresa})


def dashboard_admin(request, token):
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
    return render(request, 'admin_dashboard.html', {'lista': key})


def list_empresa(request, token):
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
    return render(request, 'list_empresa.html', {'lista': key, 'lista2': dap})


def detail_empresa(request, token, id):
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
    return render(request, 'detail_empresa.html', {'lista': key, 'lista2': dap})