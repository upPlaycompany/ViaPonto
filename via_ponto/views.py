from django.shortcuts import render
from django.contrib import auth as autent
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
import datetime
from datetime import datetime
from easy_pdf import rendering
from django.utils.six import BytesIO
import requests
import urllib3


def home(request):
    return render(request, "home.html")


def login_tipo(request):
    return render(request, "login_tipo.html")


def login_fail(request):
    return render(request, "fail_login.html")


def deslogar(request, token):
    requests.api.request(
        "GET",
        "https://parseapi.back4app.com/logout",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
            "X-Parse-Session-Token": f"{token}",
        },
    )
    logout(request)
    return redirect("home")


def redefinir_senha(request):
    if request.method == "POST":
        email = request.POST["email"]

        conexao = requests.api.request(
            "POST",
            f"https://parseapi.back4app.com/requestPasswordReset",
            headers={
                "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
                "Content-Type": "application/json",
            },
            json={
                "email": f"{email}",
            },
        )
        conexao.json()
        status = str(conexao.status_code)

        if status == "200":
            return redirect("redefinir_senha_success")
        else:
            return redirect("redefinir_senha_fail")

    return render(request, "redefinir_senha.html")


def redefinir_senha_success(request):
    return render(request, "success_redefinir_senha.html")


def redefinir_senha_fail(request):
    return render(request, "fail_redefinir_senha.html")


def register(request):
    if request.method == "POST":
        # Dados do Usuário
        username = request.POST["username"]
        password = request.POST["password"]
        cpf = request.POST["cpf"]
        # Dados da Empresa
        cnpj = request.POST["cnpj"]
        razaosocial = request.POST["razaosocial"]
        # Endereço da Empresa
        cep = request.POST["cep"]
        uf = request.POST["uf"]
        cidade = request.POST["cidade"]
        logradouro = request.POST["logradouro"]
        bairro = request.POST["bairro"]
        numero = request.POST["numero"]

        req_emp = requests.api.request(
            "POST",
            f"https://parseapi.back4app.com/classes/Empresa",
            headers={
                "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
                "Context-Type": "application/json",
            },
            json={
                "cnpj": f"{cnpj}",
                "razaosocial": f"{razaosocial}",
                "cep": f"{cep}",
                "uf": f"{uf}",
                "logradouro": f"{logradouro}",
                "numero": f"{numero}",
                "cidade": f"{cidade}",
                "bairro": f"{bairro}",
            },
        )
        status_emp = str(req_emp.status_code)
        empresa = req_emp.json()

        if status_emp != "201":
            return redirect("login_gestor")

        req_user = requests.api.request(
            "POST",
            f"https://parseapi.back4app.com/users",
            headers={
                "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
                "X-Parse-Revocable-Session": "1",
                "Content-Type": "application/json",
            },
            json={
                "username": f"{username}",
                "password": f"{password}",
                "cpf": f"{cpf}",
                "gestor": bool(True),
                "admin": bool(False),
                "id_empresa": {
                    "__type": "Pointer",
                    "className": "Empresa",
                    "objectId": empresa["objectId"],
                },
            },
        )
        user = req_user.json()
        status_user = str(req_user.status_code)

        if status_user == "201":
            req_role = requests.api.request(
                "PUT",
                f"https://parseapi.back4app.com/roles/yBVatyTWv8",
                headers={
                    "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                    "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
                    "Content-Type": "application/json",
                },
                json={
                    "users": {
                        "__op": "AddRelation",
                        "objects": [
                            {
                                "__type": "Pointer",
                                "className": "_User",
                                "objectId": f"{user['objectId']}",
                            }
                        ],
                    }
                },
            )

            status_role = str(req_role.status_code)

            if status_role == "200":
                return redirect("register_success")
            else:
                return redirect("login_gestor")

    return render(request, "register.html")


def register_success(request):
    return render(request, "success_register.html")


def fail_default(request, token):
    conexao = requests.api.request(
        "GET",
        "https://parseapi.back4app.com/users/me",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
            "X-Parse-Session-Token": f"{token}",
        },
    )
    usuario = conexao.json()
    if str(usuario["sessionToken"]) != f"{token}":
        return redirect("login")
    elif usuario["gestor"] == False:
        return redirect("login")
    elif usuario["admin"] == True:
        return redirect("login")
    else:
        pass
    key = [{"id": token, "user": usuario["username"]}]

    return render(request, "fail_default.html", {"lista": key})


# COLABORADOR DASHBOARD
def login_colaborador(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        conexao = requests.api.request(
            "GET",
            f"https://parseapi.back4app.com/login?username={username}&password={password}",
            headers={
                "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
                "X-Parse-Revocable-Session": "1",
            },
        )
        response = conexao.json()
        status = str(conexao.status_code)

        if status == "200" and response["admin"] == True:
            return redirect("base_admin", token=response["sessionToken"])
        elif status == "200" and response["gestor"] == False:
            return redirect("dashboard_colaborador", token=response["sessionToken"])
        else:
            return redirect("login_fail")

    return render(request, "login_colaborador.html")


def dashboard_colaborador(request, token):
    conexao = requests.api.request(
        "GET",
        "https://parseapi.back4app.com/users/me",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
            "X-Parse-Session-Token": f"{token}",
        },
    )
    usuario = conexao.json()
    if str(usuario["sessionToken"]) != f"{token}":
        return redirect("login")
    elif usuario["gestor"] == True:
        return redirect("login")
    elif usuario["admin"] == True:
        return redirect("login")
    else:
        pass
    key = [{"id": token, "user": usuario["username"]}]

    return render(request, "dashboard_colaborador.html", {"lista": key})


def registro_ponto(request, token):
    conexao = requests.api.request(
        "GET",
        "https://parseapi.back4app.com/users/me",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
            "X-Parse-Session-Token": f"{token}",
        },
    )
    usuario = conexao.json()
    if str(usuario["sessionToken"]) != f"{token}":
        return redirect("login")
    elif usuario["gestor"] == True:
        return redirect("login")
    elif usuario["admin"] == True:
        return redirect("login")
    else:
        pass
    key = [{"id": token, "user": usuario["username"]}]

    return render(request, "registro_ponto.html", {"lista": key})


def registrar_ponto(request, token):
    conexao = requests.api.request(
        "GET",
        "https://parseapi.back4app.com/users/me",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
            "X-Parse-Session-Token": f"{token}",
        },
    )
    usuario = conexao.json()
    if str(usuario["sessionToken"]) != f"{token}":
        return redirect("login")
    elif usuario["gestor"] == True:
        return redirect("login")
    elif usuario["admin"] == True:
        return redirect("login")
    else:
        pass
    key = [{"id": token, "user": usuario["username"]}]
    departamento_id = usuario["id_departamento"]["objectId"]
    DAYS = ["segunda", "terca", "quarta", "quinta", "sexta", "sabado", "domingo"]

    data_hora = datetime.now()
    indice_week = data_hora.weekday()
    data = data_hora.strftime("%d/%m/%Y")
    hora = data_hora.strftime("%H:%M")
    weekday = DAYS[indice_week]

    # req_turno = requests.api.request('GET', f"https://parseapi.back4app.com/classes/Turno?where=%7B%22id_empresa%22%3A%20%7B%20%22__type%22%3A%20%22Pointer%22%2C%20%22className%22%3A%20%22Empresa%22%2C%20%22objectId%22%3A%20%22{departamento_id}%22%20%7D%20%7D",
    #                                 headers={
    #                                     "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
    #                                     "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9"})
    # res_turno = req_turno.json()
    # turnos = [x for x in res_turno['results']]

    for turno in turnos:
        if turno["dia_da_semana"] == weekday:
            if hora >= turno["primeira_entrada"] and hora <= turno["primeira_saida"]:
                print("Primeira Entrada: ", hora)
            if hora >= turno["primeira_saida"] and hora <= turno["segunda_entrada"]:
                print("Primeira Saída: ", hora)
            if hora >= turno["segunda_entrada"] and hora <= turno["segunda_saida"]:
                print("Segunda Entrada")
            if (
                hora >= turno["segunda_saida"]
                and hora <= turno["segunda_saida"] + "00:30"
            ):
                print("Segunda Saída")

    return render(request, "registro_ponto.html", {"lista": key})


# GESTOR DASHBOARD
def login_gestor(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        conexao = requests.api.request(
            "GET",
            f"https://parseapi.back4app.com/login?username={username}&password={password}",
            headers={
                "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
                "X-Parse-Revocable-Session": "1",
            },
        )
        response = conexao.json()
        status = str(conexao.status_code)

        if status == "200" and response["admin"] == True:
            return redirect("base_admin", token=response["sessionToken"])
        elif status == "200" and response["gestor"] == True:
            return redirect("dashboard", token=response["sessionToken"])
        else:
            return redirect("login_fail")

    return render(request, "login_gestor.html")


def dashboard(request, token):
    conexao = requests.api.request(
        "GET",
        "https://parseapi.back4app.com/users/me",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
            "X-Parse-Session-Token": f"{token}",
        },
    )
    usuario = conexao.json()
    if str(usuario["sessionToken"]) != f"{token}":
        return redirect("login")
    elif usuario["gestor"] == False:
        return redirect("login")
    elif usuario["admin"] == True:
        return redirect("login")
    else:
        pass
    key = [{"id": token, "user": usuario["username"]}]

    return render(request, "dashboard.html", {"lista": key})


# EMPREGADOR
def edit_empresa(request, token):
    conexao = requests.api.request(
        "GET",
        "https://parseapi.back4app.com/users/me",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
            "X-Parse-Session-Token": f"{token}",
        },
    )
    response = conexao.json()
    if str(response["sessionToken"]) != f"{token}":
        return redirect("login")
    elif response["gestor"] == False:
        return redirect("login")
    else:
        pass
    key = [{"id": token, "user": response["username"]}]
    empresa_id = response["id_empresa"]["objectId"]

    req_emp = requests.api.request(
        "GET",
        f"https://parseapi.back4app.com/classes/Empresa/{empresa_id}",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
        },
    )
    emp = req_emp.json()

    if request.method == "POST":
        # Dados da Empresa
        nome_empresa = request.POST["nome_empresa"]
        cnpj = request.POST["cnpj"]
        ie = request.POST["ie"]
        razaosocial = request.POST["razaosocial"]
        atividade = request.POST["atividade"]
        tel_comercial = request.POST["tel_comercial"]
        celular_empresa = request.POST["celular_empresa"]
        email_empresa = request.POST["email_empresa"]
        # Endereço da Empresa
        cep = request.POST["cep"]
        uf = request.POST["uf"]
        cidade = request.POST["cidade"]
        logradouro = request.POST["logradouro"]
        bairro = request.POST["bairro"]
        numero = request.POST["numero"]

        req_emp = requests.api.request(
            "PUT",
            f"https://parseapi.back4app.com/classes/Empresa/{empresa_id}",
            headers={
                "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
                "Content-Type": "application/json",
            },
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
            },
        )

        status = str(req_emp.status_code)
        if status == "200":
            return redirect("edit_empresa_success", token=token)
        else:
            return redirect("edit_empresa_fail", token=token)

    return render(request, "edit_empresa.html", {"lista": key, "empresa": emp})


def edit_empresa_success(request, token):
    conexao = requests.api.request(
        "GET",
        "https://parseapi.back4app.com/users/me",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
            "X-Parse-Session-Token": f"{token}",
        },
    )
    response = conexao.json()
    if str(response["sessionToken"]) != f"{token}":
        return redirect("login")
    elif response["gestor"] == False:
        return redirect("login")
    else:
        pass
    key = [{"id": token, "user": response["username"]}]

    return render(request, "success_edit_empresa.html", {"lista": key})


def edit_empresa_fail(request, token):
    conexao = requests.api.request(
        "GET",
        "https://parseapi.back4app.com/users/me",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
            "X-Parse-Session-Token": f"{token}",
        },
    )
    response = conexao.json()
    if str(response["sessionToken"]) != f"{token}":
        return redirect("login")
    elif response["gestor"] == False:
        return redirect("login")
    else:
        pass
    key = [{"id": token, "user": response["username"]}]

    return render(request, "fail_edit_empresa.html", {"lista": key})


def list_departamento(request, token):
    conexao = requests.api.request(
        "GET",
        "https://parseapi.back4app.com/users/me",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
            "X-Parse-Session-Token": f"{token}",
        },
    )
    response = conexao.json()
    if str(response["sessionToken"]) != f"{token}":
        return redirect("login")
    elif response["gestor"] == False:
        return redirect("login")
    else:
        pass
    key = [{"id": token, "user": response["username"]}]
    empresa_id = response["id_empresa"]["objectId"]

    req_dep = requests.api.request(
        "GET",
        f"https://parseapi.back4app.com/classes/Departamento?where=%7B%22id_empresa%22%3A%20%7B%20%22__type%22%3A%20%22Pointer%22%2C%20%22className%22%3A%20%22Empresa%22%2C%20%22objectId%22%3A%20%22{empresa_id}%22%20%7D%20%7D",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
        },
    )
    res_dep = req_dep.json()
    departamento = [x for x in res_dep["results"]]

    return render(
        request, "list_departamento.html", {"lista": key, "departamentos": departamento}
    )


def cadastro_departamento(request, token):
    conexao = requests.api.request(
        "GET",
        "https://parseapi.back4app.com/users/me",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
            "X-Parse-Session-Token": f"{token}",
        },
    )
    response = conexao.json()
    if str(response["sessionToken"]) != f"{token}":
        return redirect("login")
    elif response["gestor"] == False:
        return redirect("login")
    else:
        pass
    key = [{"id": token, "user": response["username"]}]
    empresa_id = response["id_empresa"]["objectId"]

    if request.method == "POST":
        nome = request.POST["nome_departamento"]

        req_dep = requests.api.request(
            "POST",
            f"https://parseapi.back4app.com/classes/Departamento",
            headers={
                "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
                "Content-Type": "application/json",
            },
            json={
                "nome": f"{nome}",
                "id_empresa": {
                    "__type": "Pointer",
                    "className": "Empresa",
                    "objectId": empresa_id,
                },
            },
        )
        status = str(req_dep.status_code)
        if status == "201":
            return redirect("list_departamento", token=token)
        else:
            return redirect("fail_default", token=token)

    return render(request, "cadastro_departamento.html", {"lista": key})


def edit_departamento(request, token, id):
    conexao = requests.api.request(
        "GET",
        "https://parseapi.back4app.com/users/me",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
            "X-Parse-Session-Token": f"{token}",
        },
    )
    response = conexao.json()
    if str(response["sessionToken"]) != f"{token}":
        return redirect("login")
    elif response["gestor"] == False:
        return redirect("login")
    else:
        pass
    key = [{"id": token, "user": response["username"]}]
    empresa_id = response["id_empresa"]["objectId"]

    req_dep = requests.api.request(
        "GET",
        f"https://parseapi.back4app.com/classes/Departamento/{id}",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
        },
    )
    dep = req_dep.json()

    if request.method == "POST":
        nome = request.POST["nome_departamento"]

        req_dep = requests.api.request(
            "PUT",
            f"https://parseapi.back4app.com/classes/Departamento/{id}",
            headers={
                "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
                "Content-Type": "application/json",
            },
            json={
                "nome": f"{nome}",
                "id_empresa": {
                    "__type": "Pointer",
                    "className": "Empresa",
                    "objectId": empresa_id,
                },
            },
        )
        status = str(req_dep.status_code)
        if status == "200":
            return redirect("list_departamento", token=token)
        else:
            return redirect("fail_default", token=token)

    return render(
        request, "edit_departamento.html", {"lista": key, "departamento": dep}
    )


def delete_departamento(request, token, id):
    conexao = requests.api.request(
        "GET",
        "https://parseapi.back4app.com/users/me",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
            "X-Parse-Session-Token": f"{token}",
        },
    )
    response = conexao.json()
    if str(response["sessionToken"]) != f"{token}":
        return redirect("login")
    elif response["gestor"] == False:
        return redirect("login")
    else:
        pass

    req_dep = requests.api.request(
        "DELETE",
        f"https://parseapi.back4app.com/classes/Departamento/{id}",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
        },
    )

    status = str(req_dep.status_code)
    if status == "200":
        return redirect("list_departamento", token=token)
    else:
        return redirect("fail_default", token=token)


def list_feriado(request, token):
    conexao = requests.api.request(
        "GET",
        "https://parseapi.back4app.com/users/me",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
            "X-Parse-Session-Token": f"{token}",
        },
    )
    response = conexao.json()
    if str(response["sessionToken"]) != f"{token}":
        return redirect("login")
    elif response["gestor"] == False:
        return redirect("login")
    else:
        pass
    key = [{"id": token, "user": response["username"]}]

    return render(request, "list_feriado.html", {"lista": key})


# HORÁRIOS
def list_horario(request, token):
    conexao = requests.api.request(
        "GET",
        "https://parseapi.back4app.com/users/me",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
            "X-Parse-Session-Token": f"{token}",
        },
    )
    response = conexao.json()
    if str(response["sessionToken"]) != f"{token}":
        return redirect("login")
    elif response["gestor"] == False:
        return redirect("login")
    else:
        pass
    key = [{"id": token, "user": response["username"]}]
    empresa_id = response["id_empresa"]["objectId"]

    req_dep = requests.api.request(
        "GET",
        f"https://parseapi.back4app.com/classes/Departamento?where=%7B%22id_empresa%22%3A%20%7B%20%22__type%22%3A%20%22Pointer%22%2C%20%22className%22%3A%20%22Empresa%22%2C%20%22objectId%22%3A%20%22{empresa_id}%22%20%7D%20%7D",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
        },
    )
    res_dep = req_dep.json()
    departamento = [x for x in res_dep["results"]]

    req_turno = requests.api.request(
        "GET",
        f"https://parseapi.back4app.com/classes/Turno?where=%7B%20%22id_empresa%22%3A%20%7B%20%22__type%22%3A%20%22Pointer%22%2C%20%22className%22%3A%20%22Empresa%22%2C%20%22objectId%22%3A%20%22{empresa_id}%22%20%7D%20%7D",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
        },
    )
    res_turno = req_turno.json()
    turno = [x for x in res_turno["results"]]

    return render(request, "list_horario.html", {"lista": key, "turnos": turno, "departamentos": departamento})


def cadastro_horario(request, token):
    conexao = requests.api.request(
        "GET",
        "https://parseapi.back4app.com/users/me",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
            "X-Parse-Session-Token": f"{token}",
        },
    )
    response = conexao.json()
    if str(response["sessionToken"]) != f"{token}":
        return redirect("login")
    elif response["gestor"] == False:
        return redirect("login")
    else:
        pass
    key = [{"id": token, "user": response["username"]}]
    empresa_id = response["id_empresa"]["objectId"]

    req_dep = requests.api.request(
        "GET",
        f"https://parseapi.back4app.com/classes/Departamento?where=%7B%22id_empresa%22%3A%20%7B%20%22__type%22%3A%20%22Pointer%22%2C%20%22className%22%3A%20%22Empresa%22%2C%20%22objectId%22%3A%20%22{empresa_id}%22%20%7D%20%7D",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
        },
    )
    res_dep = req_dep.json()
    departamento = [x for x in res_dep["results"]]

    if request.method == "POST":
        nome = request.POST["nome_turno"]
        departamento_id = request.POST["departamento"]

        seg_primeira_entrada = request.POST["seg_primeira_entrada"]
        if seg_primeira_entrada == "":
            seg_primeira_entrada = "nao definido"

        seg_primeira_saida = request.POST["seg_primeira_saida"]
        if seg_primeira_saida == "":
            seg_primeira_saida = "nao definido"

        seg_segunda_entrada = request.POST["seg_segunda_entrada"]
        if seg_segunda_entrada == "":
            seg_segunda_entrada = "nao definido"

        seg_segunda_saida = request.POST["seg_segunda_saida"]
        if seg_segunda_saida == "":
            seg_segunda_saida = "nao definido"

        ter_primeira_entrada = request.POST["ter_primeira_entrada"]
        if ter_primeira_entrada == "":
            ter_primeira_entrada = "nao definido"

        ter_primeira_saida = request.POST["ter_primeira_saida"]
        if ter_primeira_saida == "":
            ter_primeira_saida = "nao definido"

        ter_segunda_entrada = request.POST["ter_segunda_entrada"]
        if ter_segunda_entrada == "":
            ter_segunda_entrada = "nao definido"

        ter_segunda_saida = request.POST["ter_segunda_saida"]
        if ter_segunda_saida == "":
            ter_segunda_saida = "nao definido"

        qua_primeira_entrada = request.POST["qua_primeira_entrada"]
        if qua_primeira_entrada == "":
            qua_primeira_entrada = "nao definido"

        qua_primeira_saida = request.POST["qua_primeira_saida"]
        if qua_primeira_saida == "":
            qua_primeira_saida = "nao definido"

        qua_segunda_entrada = request.POST["qua_segunda_entrada"]
        if qua_segunda_entrada == "":
            qua_segunda_entrada = "nao definido"

        qua_segunda_saida = request.POST["qua_segunda_saida"]
        if qua_segunda_saida == "":
            qua_segunda_saida = "nao definido"

        qui_primeira_entrada = request.POST["qui_primeira_entrada"]
        if qui_primeira_entrada == "":
            qui_primeira_entrada = "nao definido"

        qui_primeira_saida = request.POST["qui_primeira_saida"]
        if qui_primeira_saida == "":
            qui_primeira_saida = "nao definido"

        qui_segunda_entrada = request.POST["qui_segunda_entrada"]
        if qui_segunda_entrada == "":
            qui_segunda_entrada = "nao definido"

        qui_segunda_saida = request.POST["qui_segunda_saida"]
        if qui_segunda_saida == "":
            qui_segunda_saida = "nao definido"

        sex_primeira_entrada = request.POST["sex_primeira_entrada"]
        if sex_primeira_entrada == "":
            sex_primeira_entrada = "nao definido"

        sex_primeira_saida = request.POST["sex_primeira_saida"]
        if sex_primeira_saida == "":
            sex_primeira_saida = "nao definido"

        sex_segunda_entrada = request.POST["sex_segunda_entrada"]
        if sex_segunda_entrada == "":
            sex_segunda_entrada = "nao definido"

        sex_segunda_saida = request.POST["sex_segunda_saida"]
        if sex_segunda_saida == "":
            sex_segunda_saida = "nao definido"

        sab_primeira_entrada = request.POST["sab_primeira_entrada"]
        if sab_primeira_entrada == "":
            sab_primeira_entrada = "nao definido"

        sab_primeira_saida = request.POST["sab_primeira_saida"]
        if sab_primeira_saida == "":
            sab_primeira_saida = "nao definido"

        sab_segunda_entrada = request.POST["sab_segunda_entrada"]
        if sab_segunda_entrada == "":
            sab_segunda_entrada = "nao definido"

        sab_segunda_saida = request.POST["sab_segunda_saida"]
        if sab_segunda_saida == "":
            sab_segunda_saida = "nao definido"

        dom_primeira_entrada = request.POST["dom_primeira_entrada"]
        if dom_primeira_entrada == "":
            dom_primeira_entrada = "nao definido"

        dom_primeira_saida = request.POST["dom_primeira_saida"]
        if dom_primeira_saida == "":
            dom_primeira_saida = "nao definido"

        dom_segunda_entrada = request.POST["dom_segunda_entrada"]
        if dom_segunda_entrada == "":
            dom_segunda_entrada = "nao definido"

        dom_segunda_saida = request.POST["dom_segunda_saida"]
        if dom_segunda_saida == "":
            dom_segunda_saida = "nao definido"

        requests.api.request(
            "POST",
            f"https://parseapi.back4app.com/classes/Turno",
            headers={
                "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
                "Content-Type": "application/json",
            },
            json={
                "nome": f"{nome}",
                "dia_da_semana": "segunda",
                "primeira_entrada": f"{seg_primeira_entrada}",
                "primeira_saida": f"{seg_primeira_saida}",
                "segunda_entrada": f"{seg_segunda_entrada}",
                "segunda_saida": f"{seg_segunda_saida}",
                "id_empresa": {
                    "__type": "Pointer",
                    "className": "Empresa",
                    "objectId": empresa_id,
                },
                "id_departamento": {
                    "__type": "Pointer",
                    "className": "Departamento",
                    "objectId": departamento_id,
                },
            },
        )

        requests.api.request(
            "POST",
            f"https://parseapi.back4app.com/classes/Turno",
            headers={
                "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
                "Content-Type": "application/json",
            },
            json={
                "nome": f"{nome}",
                "dia_da_semana": "terca",
                "primeira_entrada": f"{ter_primeira_entrada}",
                "primeira_saida": f"{ter_primeira_saida}",
                "segunda_entrada": f"{ter_segunda_entrada}",
                "segunda_saida": f"{ter_segunda_saida}",
                "id_empresa": {
                    "__type": "Pointer",
                    "className": "Empresa",
                    "objectId": empresa_id,
                },
                "id_departamento": {
                    "__type": "Pointer",
                    "className": "Departamento",
                    "objectId": departamento_id,
                },
            },
        )

        requests.api.request(
            "POST",
            f"https://parseapi.back4app.com/classes/Turno",
            headers={
                "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
                "Content-Type": "application/json",
            },
            json={
                "nome": f"{nome}",
                "dia_da_semana": "quarta",
                "primeira_entrada": f"{qua_primeira_entrada}",
                "primeira_saida": f"{qua_primeira_saida}",
                "segunda_entrada": f"{qua_segunda_entrada}",
                "segunda_saida": f"{qua_segunda_saida}",
                "id_empresa": {
                    "__type": "Pointer",
                    "className": "Empresa",
                    "objectId": empresa_id,
                },
                "id_departamento": {
                    "__type": "Pointer",
                    "className": "Departamento",
                    "objectId": departamento_id,
                },
            },
        )

        requests.api.request(
            "POST",
            f"https://parseapi.back4app.com/classes/Turno",
            headers={
                "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
                "Content-Type": "application/json",
            },
            json={
                "nome": f"{nome}",
                "dia_da_semana": "quinta",
                "primeira_entrada": f"{qui_primeira_entrada}",
                "primeira_saida": f"{qui_primeira_saida}",
                "segunda_entrada": f"{qui_segunda_entrada}",
                "segunda_saida": f"{qui_segunda_saida}",
                "id_empresa": {
                    "__type": "Pointer",
                    "className": "Empresa",
                    "objectId": empresa_id,
                },
                "id_departamento": {
                    "__type": "Pointer",
                    "className": "Departamento",
                    "objectId": departamento_id,
                },
            },
        )

        requests.api.request(
            "POST",
            f"https://parseapi.back4app.com/classes/Turno",
            headers={
                "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
                "Content-Type": "application/json",
            },
            json={
                "nome": f"{nome}",
                "dia_da_semana": "sexta",
                "primeira_entrada": f"{sex_primeira_entrada}",
                "primeira_saida": f"{sex_primeira_saida}",
                "segunda_entrada": f"{sex_segunda_entrada}",
                "segunda_saida": f"{sex_segunda_saida}",
                "id_empresa": {
                    "__type": "Pointer",
                    "className": "Empresa",
                    "objectId": empresa_id,
                },
                "id_departamento": {
                    "__type": "Pointer",
                    "className": "Departamento",
                    "objectId": departamento_id,
                },
            },
        )

        requests.api.request(
            "POST",
            f"https://parseapi.back4app.com/classes/Turno",
            headers={
                "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
                "Content-Type": "application/json",
            },
            json={
                "nome": f"{nome}",
                "dia_da_semana": "sabado",
                "primeira_entrada": f"{sab_primeira_entrada}",
                "primeira_saida": f"{sab_primeira_saida}",
                "segunda_entrada": f"{sab_segunda_entrada}",
                "segunda_saida": f"{sab_segunda_saida}",
                "id_empresa": {
                    "__type": "Pointer",
                    "className": "Empresa",
                    "objectId": empresa_id,
                },
                "id_departamento": {
                    "__type": "Pointer",
                    "className": "Departamento",
                    "objectId": departamento_id,
                },
            },
        )

        requests.api.request(
            "POST",
            f"https://parseapi.back4app.com/classes/Turno",
            headers={
                "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
                "Content-Type": "application/json",
            },
            json={
                "nome": f"{nome}",
                "dia_da_semana": "domingo",
                "primeira_entrada": f"{dom_primeira_entrada}",
                "primeira_saida": f"{dom_primeira_saida}",
                "segunda_entrada": f"{dom_segunda_entrada}",
                "segunda_saida": f"{dom_segunda_saida}",
                "id_empresa": {
                    "__type": "Pointer",
                    "className": "Empresa",
                    "objectId": empresa_id,
                },
                "id_departamento": {
                    "__type": "Pointer",
                    "className": "Departamento",
                    "objectId": departamento_id,
                },
            },
        )

        return redirect("list_horario", token=token)

    return render(
        request, "cadastro_horario.html", {"lista": key, "departamentos": departamento}
    )


def edit_horario(request, token, id):
    conexao = requests.api.request(
        "GET",
        "https://parseapi.back4app.com/users/me",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
            "X-Parse-Session-Token": f"{token}",
        },
    )
    response = conexao.json()
    if str(response["sessionToken"]) != f"{token}":
        return redirect("login")
    elif response["gestor"] == False:
        return redirect("login")
    else:
        pass
    key = [{"id": token, "user": response["username"]}]
    empresa_id = response["id_empresa"]["objectId"]

    req_dep = requests.api.request(
        "GET",
        f"https://parseapi.back4app.com/classes/Departamento?where=%7B%22id_empresa%22%3A%20%7B%20%22__type%22%3A%20%22Pointer%22%2C%20%22className%22%3A%20%22Empresa%22%2C%20%22objectId%22%3A%20%22{empresa_id}%22%20%7D%20%7D",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
        },
    )
    res_dep = req_dep.json()
    departamento = [x for x in res_dep["results"]]

    req_turno = requests.api.request(
        "GET",
        f"https://parseapi.back4app.com/classes/Turno/{id}",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
        },
    )
    tur = req_turno.json()

    if request.method == "POST":
        nome = request.POST["nome_turno"]
        departamento_id = request.POST["departamento"]
        primeira_entrada = request.POST["primeira_entrada"]
        primeira_saida = request.POST["primeira_saida"]
        segunda_entrada = request.POST["segunda_entrada"]
        segunda_saida = request.POST["segunda_saida"]

        req_turn = requests.api.request(
            "PUT",
            f"https://parseapi.back4app.com/classes/Turno/{id}",
            headers={
                "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
                "Content-Type": "application/json",
            },
            json={
                "nome": f"{nome}",
                "primeira_entrada": f"{primeira_entrada}",
                "primeira_saida": f"{primeira_saida}",
                "segunda_entrada": f"{segunda_entrada}",
                "segunda_saida": f"{segunda_saida}",
                "id_empresa": {
                    "__type": "Pointer",
                    "className": "Empresa",
                    "objectId": empresa_id,
                },
                "id_departamento": {
                    "__type": "Pointer",
                    "className": "Departamento",
                    "objectId": departamento_id,
                },
            },
        )
        status = str(req_turn.status_code)
        if status == "200":
            return redirect("list_horario", token=token)
        else:
            return redirect("fail_default", token=token)

    return render(
        request,
        "edit_horario.html",
        {"lista": key, "horario": tur, "departamentos": departamento},
    )


def delete_horario(request, token, id):
    conexao = requests.api.request(
        "GET",
        "https://parseapi.back4app.com/users/me",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
            "X-Parse-Session-Token": f"{token}",
        },
    )
    response = conexao.json()
    if str(response["sessionToken"]) != f"{token}":
        return redirect("login")
    elif response["gestor"] == False:
        return redirect("login")
    else:
        pass

    req_turno = requests.api.request(
        "DELETE",
        f"https://parseapi.back4app.com/classes/Turno/{id}",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
        },
    )

    status = str(req_turno.status_code)
    if status == "200":
        return redirect("list_horario", token=token)
    else:
        return redirect("fail_default", token=token)


# LOCAIS
def list_local(request, token):
    conexao = requests.api.request(
        "GET",
        "https://parseapi.back4app.com/users/me",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
            "X-Parse-Session-Token": f"{token}",
        },
    )
    response = conexao.json()
    if str(response["sessionToken"]) != f"{token}":
        return redirect("login")
    elif response["gestor"] == False:
        return redirect("login")
    else:
        pass
    key = [{"id": token, "user": response["username"]}]

    return render(request, "list_local.html", {"lista": key})


def cadastro_local(request, token):
    conexao = requests.api.request(
        "GET",
        "https://parseapi.back4app.com/users/me",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
            "X-Parse-Session-Token": f"{token}",
        },
    )
    response = conexao.json()
    if str(response["sessionToken"]) != f"{token}":
        return redirect("login")
    elif response["gestor"] == False:
        return redirect("login")
    else:
        pass
    key = [{"id": token, "user": response["username"]}]

    return render(request, "cadastro_local.html", {"lista": key})


# COLABORADORES
def list_cargo(request, token):
    conexao = requests.api.request(
        "GET",
        "https://parseapi.back4app.com/users/me",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
            "X-Parse-Session-Token": f"{token}",
        },
    )
    response = conexao.json()
    if str(response["sessionToken"]) != f"{token}":
        return redirect("login")
    elif response["gestor"] == False:
        return redirect("login")
    else:
        pass
    key = [{"id": token, "user": response["username"]}]
    empresa_id = response["id_empresa"]["objectId"]

    req_cargo = requests.api.request(
        "GET",
        f"https://parseapi.back4app.com/classes/Cargo?where=%7B%22id_empresa%22%3A%20%7B%20%22__type%22%3A%20%22Pointer%22%2C%20%22className%22%3A%20%22Empresa%22%2C%20%22objectId%22%3A%20%22{empresa_id}%22%20%7D%20%7D",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
        },
    )
    res_cargo = req_cargo.json()
    cargo = [x for x in res_cargo["results"]]

    return render(request, "list_cargo.html", {"lista": key, "cargos": cargo})


def cadastro_cargo(request, token):
    conexao = requests.api.request(
        "GET",
        "https://parseapi.back4app.com/users/me",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
            "X-Parse-Session-Token": f"{token}",
        },
    )
    response = conexao.json()
    if str(response["sessionToken"]) != f"{token}":
        return redirect("login")
    elif response["gestor"] == False:
        return redirect("login")
    else:
        pass
    key = [{"id": token, "user": response["username"]}]
    empresa_id = response["id_empresa"]["objectId"]

    if request.method == "POST":
        nome = request.POST["nome_cargo"]

        req_cargo = requests.api.request(
            "POST",
            f"https://parseapi.back4app.com/classes/Cargo",
            headers={
                "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
                "Content-Type": "application/json",
            },
            json={
                "nome": f"{nome}",
                "id_empresa": {
                    "__type": "Pointer",
                    "className": "Empresa",
                    "objectId": empresa_id,
                },
            },
        )
        status = str(req_cargo.status_code)
        if status == "201":
            return redirect("list_cargo", token=token)
        else:
            return redirect("fail_default", token=token)

    return render(request, "cadastro_cargo.html", {"lista": key})


def edit_cargo(request, token, id):
    conexao = requests.api.request(
        "GET",
        "https://parseapi.back4app.com/users/me",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
            "X-Parse-Session-Token": f"{token}",
        },
    )
    response = conexao.json()
    if str(response["sessionToken"]) != f"{token}":
        return redirect("login")
    elif response["gestor"] == False:
        return redirect("login")
    else:
        pass
    key = [{"id": token, "user": response["username"]}]
    empresa_id = response["id_empresa"]["objectId"]

    req_carg = requests.api.request(
        "GET",
        f"https://parseapi.back4app.com/classes/Cargo/{id}",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
        },
    )
    carg = req_carg.json()

    if request.method == "POST":
        nome = request.POST["nome_cargo"]

        req_dep = requests.api.request(
            "PUT",
            f"https://parseapi.back4app.com/classes/Cargo/{id}",
            headers={
                "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
                "Content-Type": "application/json",
            },
            json={
                "nome": f"{nome}",
                "id_empresa": {
                    "__type": "Pointer",
                    "className": "Empresa",
                    "objectId": empresa_id,
                },
            },
        )
        status = str(req_dep.status_code)
        if status == "200":
            return redirect("list_cargo", token=token)
        else:
            return redirect("fail_default", token=token)

    return render(request, "edit_cargo.html", {"lista": key, "cargo": carg})


def delete_cargo(request, token, id):
    conexao = requests.api.request(
        "GET",
        "https://parseapi.back4app.com/users/me",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
            "X-Parse-Session-Token": f"{token}",
        },
    )
    response = conexao.json()
    if str(response["sessionToken"]) != f"{token}":
        return redirect("login")
    elif response["gestor"] == False:
        return redirect("login")
    else:
        pass

    req_carg = requests.api.request(
        "DELETE",
        f"https://parseapi.back4app.com/classes/Cargo/{id}",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
        },
    )

    status = str(req_carg.status_code)
    if status == "200":
        return redirect("list_cargo", token=token)
    else:
        return redirect("fail_default", token=token)


def list_colaborador(request, token):
    conexao = requests.api.request(
        "GET",
        "https://parseapi.back4app.com/users/me",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
            "X-Parse-Session-Token": f"{token}",
        },
    )
    response = conexao.json()
    if str(response["sessionToken"]) != f"{token}":
        return redirect("login")
    elif response["gestor"] == False:
        return redirect("login")
    else:
        pass
    key = [{"id": token, "user": response["username"]}]
    empresa_id = response["id_empresa"]["objectId"]

    req_user = requests.api.request(
        "GET",
        f"https://parseapi.back4app.com/classes/_User?where=%7B%22id_empresa%22%3A%20%7B%20%22__type%22%3A%20%22Pointer%22%2C%20%22className%22%3A%20%22Empresa%22%2C%20%22objectId%22%3A%20%22{empresa_id}%22%20%7D%20%7D",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
        },
    )
    res_user = req_user.json()
    colaborador = [x for x in res_user["results"]]

    req_cargo = requests.api.request(
        "GET",
        f"https://parseapi.back4app.com/classes/Cargo?where=%7B%22id_empresa%22%3A%20%7B%20%22__type%22%3A%20%22Pointer%22%2C%20%22className%22%3A%20%22Empresa%22%2C%20%22objectId%22%3A%20%22{empresa_id}%22%20%7D%20%7D",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
        },
    )
    res_cargo = req_cargo.json()
    cargo = [x for x in res_cargo["results"]]

    req_dep = requests.api.request(
        "GET",
        f"https://parseapi.back4app.com/classes/Departamento?where=%7B%22id_empresa%22%3A%20%7B%20%22__type%22%3A%20%22Pointer%22%2C%20%22className%22%3A%20%22Empresa%22%2C%20%22objectId%22%3A%20%22{empresa_id}%22%20%7D%20%7D",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
        },
    )
    res_dep = req_dep.json()
    departamento = [x for x in res_dep["results"]]

    return render(
        request,
        "list_colaborador.html",
        {
            "lista": key,
            "colaboradores": colaborador,
            "id_emp": empresa_id,
            "cargos": cargo,
            "departamentos": departamento,
        },
    )


def cadastro_colaborador(request, token):
    conexao = requests.api.request(
        "GET",
        "https://parseapi.back4app.com/users/me",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
            "X-Parse-Session-Token": f"{token}",
        },
    )

    response = conexao.json()
    if str(response["sessionToken"]) != f"{token}":
        return redirect("login")
    elif response["gestor"] == False:
        return redirect("login")
    else:
        pass
    key = [{"id": token, "user": response["username"]}]
    empresa_id = response["id_empresa"]["objectId"]

    req_cargo = requests.api.request(
        "GET",
        f"https://parseapi.back4app.com/classes/Cargo?where=%7B%22id_empresa%22%3A%20%7B%20%22__type%22%3A%20%22Pointer%22%2C%20%22className%22%3A%20%22Empresa%22%2C%20%22objectId%22%3A%20%22{empresa_id}%22%20%7D%20%7D",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
        },
    )
    res_cargo = req_cargo.json()
    cargo = [x for x in res_cargo["results"]]

    req_dep = requests.api.request(
        "GET",
        f"https://parseapi.back4app.com/classes/Departamento?where=%7B%22id_empresa%22%3A%20%7B%20%22__type%22%3A%20%22Pointer%22%2C%20%22className%22%3A%20%22Empresa%22%2C%20%22objectId%22%3A%20%22{empresa_id}%22%20%7D%20%7D",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
        },
    )
    res_dep = req_dep.json()
    departamento = [x for x in res_dep["results"]]

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        nome = request.POST["nome"]
        cpf = request.POST["cpf"]
        datanasc = request.POST["datanasc"]
        celular = request.POST["celular"]
        email = request.POST["email"]
        admissao = request.POST["admissao"]
        pis = request.POST["pis"]
        cargo_id = request.POST["cargo"]
        departamento_id = request.POST["departamento"]
        # Endereço do Colaborador
        cep = request.POST["cep"]
        uf = request.POST["uf"]
        cidade = request.POST["cidade"]
        logradouro = request.POST["logradouro"]
        bairro = request.POST["bairro"]
        numero = request.POST["numero"]

        req_user = requests.api.request(
            "POST",
            f"https://parseapi.back4app.com/users",
            headers={
                "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
                "X-Parse-Revocable-Session": "1",
                "Content-Type": "application/json",
            },
            json={
                "ACL": {
                    "role:admins": {
                        "write": True,
                    },
                    "*": {
                        "read": True,
                    },
                },
                "username": f"{username}",
                "password": f"{password}",
                "nome": f"{nome}",
                "cpf": f"{cpf}",
                "data_nasc": f"{datanasc}",
                "email": f"{email}",
                "email_colab": f"{email}",
                "celular": f"{celular}",
                "admissao": f"{admissao}",
                "pis": f"{pis}",
                "cep": f"{cep}",
                "uf": f"{uf}",
                "cidade": f"{cidade}",
                "logradouro": f"{logradouro}",
                "bairro": f"{bairro}",
                "numero": f"{numero}",
                "gestor": bool(False),
                "admin": bool(False),
                "id_cargo": {
                    "__type": "Pointer",
                    "className": "Cargo",
                    "objectId": cargo_id,
                },
                "id_departamento": {
                    "__type": "Pointer",
                    "className": "Departamento",
                    "objectId": departamento_id,
                },
                "id_empresa": {
                    "__type": "Pointer",
                    "className": "Empresa",
                    "objectId": empresa_id,
                },
            },
        )

        req_user.json()
        status = str(req_user.status_code)
        if status == "201":
            return redirect("cadastro_colaborador_success", token=token)
        else:
            return redirect("fail_default", token=token)

    return render(
        request,
        "cadastro_colaborador.html",
        {"lista": key, "cargos": cargo, "departamentos": departamento},
    )


def cadastro_colaborador_success(request, token):
    conexao = requests.api.request(
        "GET",
        "https://parseapi.back4app.com/users/me",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
            "X-Parse-Session-Token": f"{token}",
        },
    )

    response = conexao.json()
    if str(response["sessionToken"]) != f"{token}":
        return redirect("login")
    elif response["gestor"] == False:
        return redirect("login")
    else:
        pass
    key = [{"id": token, "user": response["username"]}]
    return render(request, "success_cadastro_colaborador.html", {"lista": key})


def demitir_colaborador(request, token, id):
    conexao = requests.api.request(
        "GET",
        "https://parseapi.back4app.com/users/me",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
            "X-Parse-Session-Token": f"{token}",
        },
    )
    response = conexao.json()
    if str(response["sessionToken"]) != f"{token}":
        return redirect("login")
    elif response["gestor"] == False:
        return redirect("login")
    else:
        pass

    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date = date[:10]
    data = datetime.strptime(date, "%Y-%m-%d").date()
    data_demissao = data.strftime("%d/%m/%Y")

    req_user = requests.api.request(
        "PUT",
        f"https://parseapi.back4app.com/classes/_User/{id}",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
            "X-Parse-Session-Token": f"{token}",
            "Content-Type": "application/json",
        },
        json={
            "demitido": bool(True),
            "demissao": f"{data_demissao}",
        },
    )

    status = str(req_user.status_code)

    if status == "200":
        return redirect("list_demitidos", token=token)
    else:
        return redirect("fail_default", token=token)


def edit_colaborador(request, token, id):
    conexao = requests.api.request(
        "GET",
        "https://parseapi.back4app.com/users/me",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
            "X-Parse-Session-Token": f"{token}",
        },
    )
    response = conexao.json()
    if str(response["sessionToken"]) != f"{token}":
        return redirect("login")
    elif response["gestor"] == False:
        return redirect("login")
    else:
        pass
    key = [{"id": token, "user": response["username"]}]
    empresa_id = response["id_empresa"]["objectId"]

    req_cargo = requests.api.request(
        "GET",
        f"https://parseapi.back4app.com/classes/Cargo?where=%7B%22id_empresa%22%3A%20%7B%20%22__type%22%3A%20%22Pointer%22%2C%20%22className%22%3A%20%22Empresa%22%2C%20%22objectId%22%3A%20%22{empresa_id}%22%20%7D%20%7D",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
        },
    )
    res_cargo = req_cargo.json()
    cargo = [x for x in res_cargo["results"]]

    req_dep = requests.api.request(
        "GET",
        f"https://parseapi.back4app.com/classes/Departamento?where=%7B%22id_empresa%22%3A%20%7B%20%22__type%22%3A%20%22Pointer%22%2C%20%22className%22%3A%20%22Empresa%22%2C%20%22objectId%22%3A%20%22{empresa_id}%22%20%7D%20%7D",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
        },
    )
    res_dep = req_dep.json()
    departamento = [x for x in res_dep["results"]]

    req_user_get = requests.api.request(
        "GET",
        f"https://parseapi.back4app.com/classes/_User/{id}",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
        },
    )
    colab = req_user_get.json()

    if request.method == "POST":
        username = request.POST["username"]
        nome = request.POST["nome"]
        cpf = request.POST["cpf"]
        datanasc = request.POST["datanasc"]
        celular = request.POST["celular"]
        email_colab = request.POST["email"]
        admissao = request.POST["admissao"]
        pis = request.POST["pis"]
        cargo_id = request.POST["cargo"]
        departamento_id = request.POST["departamento"]
        # Endereço do Colaborador
        cep = request.POST["cep"]
        uf = request.POST["uf"]
        cidade = request.POST["cidade"]
        logradouro = request.POST["logradouro"]
        bairro = request.POST["bairro"]
        numero = request.POST["numero"]

        req_user = requests.api.request(
            "PUT",
            f"https://parseapi.back4app.com/classes/_User/{id}",
            headers={
                "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
                "X-Parse-Session-Token": f"{token}",
                "Content-Type": "application/json",
            },
            json={
                "username": f"{username}",
                "nome": f"{nome}",
                "cpf": f"{cpf}",
                "data_nasc": f"{datanasc}",
                "email_colab": f"{email_colab}",
                "email": f"{email_colab}",
                "celular": f"{celular}",
                "admissao": f"{admissao}",
                "pis": f"{pis}",
                "cep": f"{cep}",
                "uf": f"{uf}",
                "cidade": f"{cidade}",
                "logradouro": f"{logradouro}",
                "bairro": f"{bairro}",
                "numero": f"{numero}",
                "id_cargo": {
                    "__type": "Pointer",
                    "className": "Cargo",
                    "objectId": cargo_id,
                },
                "id_departamento": {
                    "__type": "Pointer",
                    "className": "Departamento",
                    "objectId": departamento_id,
                },
            },
        )

        req_user.json()

        status = str(req_user.status_code)

        if status == "200":
            return redirect("list_colaborador", token=token)
        else:
            return redirect("fail_default", token=token)

    return render(
        request,
        "edit_colaborador.html",
        {
            "lista": key,
            "cargos": cargo,
            "departamentos": departamento,
            "colaborador": colab,
        },
    )


def list_demitidos(request, token):
    conexao = requests.api.request(
        "GET",
        "https://parseapi.back4app.com/users/me",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
            "X-Parse-Session-Token": f"{token}",
        },
    )
    response = conexao.json()
    if str(response["sessionToken"]) != f"{token}":
        return redirect("login")
    elif response["gestor"] == False:
        return redirect("login")
    else:
        pass
    key = [{"id": token, "user": response["username"]}]
    empresa_id = response["id_empresa"]["objectId"]

    req_user = requests.api.request(
        "GET",
        f"https://parseapi.back4app.com/classes/_User?where=%7B%22id_empresa%22%3A%20%7B%20%22__type%22%3A%20%22Pointer%22%2C%20%22className%22%3A%20%22Empresa%22%2C%20%22objectId%22%3A%20%22{empresa_id}%22%20%7D%20%7D",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
        },
    )
    res_user = req_user.json()
    colaborador = [x for x in res_user["results"]]

    req_dep = requests.api.request(
        "GET",
        f"https://parseapi.back4app.com/classes/Departamento?where=%7B%22id_empresa%22%3A%20%7B%20%22__type%22%3A%20%22Pointer%22%2C%20%22className%22%3A%20%22Empresa%22%2C%20%22objectId%22%3A%20%22{empresa_id}%22%20%7D%20%7D",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
        },
    )
    res_dep = req_dep.json()
    departamento = [x for x in res_dep["results"]]

    return render(
        request,
        "list_demitidos.html",
        {
            "lista": key,
            "colaboradores": colaborador,
            "id_emp": empresa_id,
            "departamentos": departamento,
        },
    )


# RELATÓRIOS
def pontos_colaborador(request, token, id_user):
    conexao = requests.api.request(
        "GET",
        "https://parseapi.back4app.com/users/me",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
            "X-Parse-Session-Token": f"{token}",
        },
    )
    response = conexao.json()
    if str(response["sessionToken"]) != f"{token}":
        return redirect("login")
    elif response["gestor"] == False:
        return redirect("login")
    else:
        pass
    key = [{"id": token, "user": response["username"]}]
    empresa_id = response["id_empresa"]["objectId"]

    req_user = requests.api.request(
        "GET",
        f"https://parseapi.back4app.com/classes/_User",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
        },
    )
    res_user = req_user.json()
    colaborador = [x for x in res_user["results"]]

    req_ponto = requests.api.request(
        "GET",
        f"https://parseapi.back4app.com/classes/Ponto",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
        },
    )
    res_ponto = req_ponto.json()
    ponto = [x for x in res_ponto["results"]]

    for x in ponto:
        data = x["createdAt"]
        data = data[:10]
        date = datetime.strptime(data, "%Y-%m-%d").date()
        date = date.strftime("%d/%m/%Y")
        x["createdAt"] = date

    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    if start_date and end_date:
        start = datetime.strptime(start_date, "%Y-%m-%d").date()
        end = datetime.strptime(end_date, "%Y-%m-%d").date()
        start_data = start.strftime("%d/%m/%Y")
        end_data = end.strftime("%d/%m/%Y")
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

            datas = tuple(
                [
                    f"0{lista[x]}" + "/" + f"{mes_start}" + "/" + f"{ano_start}"
                    if lista[x] < 10
                    else f"{lista[x]}" + "/" + f"{mes_start}" + "/" + f"{ano_start}"
                    for x in range(a)
                ]
            )
        elif mes_start < mes_end:
            if mes_start < 10:
                mes_start = f"0{mes_start}"
            if mes_end < 10:
                mes_end = f"0{mes_end}"

            lista = list(range(dia_start, 32))
            lista2 = list(range(1, dia_end + 1))
            a = len(lista)
            a2 = len(lista2)

            datas = tuple(
                [
                    f"0{lista[x]}" + "/" + f"{mes_start}" + "/" + f"{ano_start}"
                    if lista[x] < 10
                    else f"{lista[x]}" + "/" + f"{mes_start}" + "/" + f"{ano_start}"
                    for x in range(a)
                ]
            )
            datas2 = tuple(
                [
                    f"0{lista2[x]}" + "/" + f"{mes_end}" + "/" + f"{ano_end}"
                    if lista2[x] < 10
                    else f"{lista2[x]}" + "/" + f"{mes_end}" + "/" + f"{ano_end}"
                    for x in range(a2)
                ]
            )
            datas += datas2

        ponto_date = [
            {
                "createdAt": x["createdAt"],
                "id_funcionario": {"objectId": x["id_funcionario"]["objectId"]},
                "horario": x["horario"],
                "registro": x["registro"],
                "local_registro": x["local_registro"],
            }
            if str(x["createdAt"]) in datas
            else {
                "createdAt": "sem registro",
                "id_funcionario": {"objectId": "sem registro"},
                "horario": "sem registro",
                "registro": "sem registro",
                "local_registro": "sem registro",
            }
            for x in ponto
        ]
    else:
        ponto_date = ponto
        start = "0"
        end = "0"

    return render(
        request,
        "pontos_colaborador.html",
        {
            "lista": key,
            "colaboradores": colaborador,
            "id_emp": empresa_id,
            "Id_user": id_user,
            "pontos": ponto_date,
            "start_data": start,
            "end_data": end,
        },
    )


def gerar_relatorio_func(request, token):
    conexao = requests.api.request(
        "GET",
        "https://parseapi.back4app.com/users/me",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
            "X-Parse-Session-Token": f"{token}",
        },
    )
    response = conexao.json()
    if str(response["sessionToken"]) != f"{token}":
        return redirect("login")
    elif response["gestor"] == False:
        return redirect("login")
    else:
        pass
    key = [{"id": token, "user": response["username"]}]
    empresa_id = response["id_empresa"]["objectId"]

    conexao1 = requests.api.request(
        "GET",
        f"https://parseapi.back4app.com/classes/_User",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
        },
    )
    f = conexao1.json()
    funcionario = [x for x in f["results"]]

    conexao2 = requests.api.request(
        "GET",
        f"https://parseapi.back4app.com/classes/Empresa?where=%7B%22objectId%22%3A%20%22{empresa_id}%22%7D",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
            "accept": "application/json",
        },
    )
    e = conexao2.json()
    emp = [x for x in e["results"]]

    return rendering.render_to_pdf_response(
        request=request,
        context={"funcionarios": funcionario, "empresa": emp, "id_emp": empresa_id},
        template="relatorio-funcionarios.html",
        encoding="utf-8",
    )


def gerar_relatorio_ponto(request, token, id_user, start_date, end_date):
    conexao = requests.api.request(
        "GET",
        "https://parseapi.back4app.com/users/me",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
            "X-Parse-Session-Token": f"{token}",
        },
    )
    response = conexao.json()
    if str(response["sessionToken"]) != f"{token}":
        return redirect("login")
    elif response["gestor"] == False:
        return redirect("login")
    else:
        pass
    key = [{"id": token, "user": response["username"]}]
    empresa_id = response["id_empresa"]["objectId"]

    conexao1 = requests.api.request(
        "GET",
        f"https://parseapi.back4app.com/classes/_User",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
        },
    )
    f = conexao1.json()
    funcionario = [x for x in f["results"]]

    conexao2 = requests.api.request(
        "GET",
        f"https://parseapi.back4app.com/classes/Ponto",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
        },
    )
    p = conexao2.json()
    ponto = [x for x in p["results"]]

    for x in ponto:
        data = x["createdAt"]
        data = data[:10]
        date = datetime.strptime(data, "%Y-%m-%d").date()
        date = date.strftime("%d/%m/%Y")
        x["createdAt"] = date

    if start_date != "0" and end_date != "0":
        start = datetime.strptime(start_date, "%Y-%m-%d").date()
        end = datetime.strptime(end_date, "%Y-%m-%d").date()
        start_data = start.strftime("%d/%m/%Y")
        end_data = end.strftime("%d/%m/%Y")
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

            datas = tuple(
                [
                    f"0{lista[x]}" + "/" + f"{mes_start}" + "/" + f"{ano_start}"
                    if lista[x] < 10
                    else f"{lista[x]}" + "/" + f"{mes_start}" + "/" + f"{ano_start}"
                    for x in range(a)
                ]
            )
        elif mes_start < mes_end:
            if mes_start < 10:
                mes_start = f"0{mes_start}"
            if mes_end < 10:
                mes_end = f"0{mes_end}"

            lista = list(range(dia_start, 32))
            lista2 = list(range(1, dia_end + 1))
            a = len(lista)
            a2 = len(lista2)

            datas = tuple(
                [
                    f"0{lista[x]}" + "/" + f"{mes_start}" + "/" + f"{ano_start}"
                    if lista[x] < 10
                    else f"{lista[x]}" + "/" + f"{mes_start}" + "/" + f"{ano_start}"
                    for x in range(a)
                ]
            )
            datas2 = tuple(
                [
                    f"0{lista2[x]}" + "/" + f"{mes_end}" + "/" + f"{ano_end}"
                    if lista2[x] < 10
                    else f"{lista2[x]}" + "/" + f"{mes_end}" + "/" + f"{ano_end}"
                    for x in range(a2)
                ]
            )
            datas += datas2

        ponto_date = [
            {
                "createdAt": x["createdAt"],
                "id_funcionario": {"objectId": x["id_funcionario"]["objectId"]},
                "horario": x["horario"],
                "registro": x["registro"],
                "local_registro": x["local_registro"],
            }
            if str(x["createdAt"]) in datas
            else {
                "createdAt": "sem registro",
                "id_funcionario": {"objectId": "sem registro"},
                "horario": "sem registro",
                "registro": "sem registro",
                "local_registro": "sem registro",
            }
            for x in ponto
        ]
    else:
        ponto_date = ponto

    return rendering.render_to_pdf_response(
        request=request,
        context={
            "funcionarios": funcionario,
            "Id_user": id_user,
            "id_emp": empresa_id,
            "pontos": ponto_date,
        },
        template="relatorio-pontos.html",
        encoding="utf-8",
    )


# ÁREA ADMINISTRATIVA #
def base_admin(request, token):
    conexao = requests.api.request(
        "GET",
        "https://parseapi.back4app.com/users/me",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
            "X-Parse-Session-Token": f"{token}",
        },
    )
    response = conexao.json()
    if str(response["sessionToken"]) != f"{token}":
        return redirect("login")
    elif response["gestor"] == False or response["gestor"] == True:
        return redirect("login")
    elif response["admin"] == False:
        return redirect("login")
    else:
        pass
    key = [{"id": token, "user": response["username"]}]

    conexao1 = requests.api.request(
        "GET",
        f"https://parseapi.back4app.com/classes/_User",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
        },
    )
    user = conexao1.json()
    usuario = [x for x in user["results"]]
    num_usuario = [{"numero_usuario": len(usuario) - 1}]
    conexao2 = requests.api.request(
        "GET",
        f"https://parseapi.back4app.com/classes/Empresa",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
            "accept": "application/json",
        },
    )

    emp = conexao2.json()
    empresa = [x for x in emp["results"]]
    num_empresa = [{"numero_empresa": len(empresa)}]
    key = [{"id": token, "user": abc["username"]}]

    return render(
        request,
        "admin_base.html",
        {"lista": key, "usuarios": num_usuario, "empresas": num_empresa},
    )


def dashboard_admin(request, token):
    conexao = requests.api.request(
        "GET",
        "https://parseapi.back4app.com/users/me",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
            "X-Parse-Session-Token": f"{token}",
        },
    )
    response = conexao.json()
    if str(response["sessionToken"]) != f"{token}":
        return redirect("login")
    elif response["gestor"] == False or response["gestor"] == True:
        return redirect("login")
    elif response["admin"] == False:
        return redirect("login")
    else:
        pass
    key = [{"id": token, "user": response["username"]}]

    return render(request, "admin_dashboard.html", {"lista": key})


def list_empresa(request, token):
    conexao = requests.api.request(
        "GET",
        "https://parseapi.back4app.com/users/me",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
            "X-Parse-Session-Token": f"{token}",
        },
    )
    response = conexao.json()
    if str(response["sessionToken"]) != f"{token}":
        return redirect("login")
    elif response["gestor"] == False or response["gestor"] == True:
        return redirect("login")
    elif response["admin"] == False:
        return redirect("login")
    else:
        pass
    key = [{"id": token, "user": response["username"]}]
    conexao1 = requests.api.request(
        "GET",
        f"https://parseapi.back4app.com/classes/Empresa",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
            "accept": "application/json",
        },
    )

    key = [{"id": token, "user": abc["username"]}]
    dop = conexao1.json()
    dap = [x for x in dop["results"]]
    a = len(dap)
    [dap[x].update({"token": token}) for x in range(a)]
    return render(request, "list_empresa.html", {"lista": key, "lista2": dap})


def detail_empresa(request, token, id):
    conexao = requests.api.request(
        "GET",
        "https://parseapi.back4app.com/users/me",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
            "X-Parse-Session-Token": f"{token}",
        },
    )
    response = conexao.json()
    if str(response["sessionToken"]) != f"{token}":
        return redirect("login")
    elif response["gestor"] == False or response["gestor"] == True:
        return redirect("login")
    elif response["admin"] == False:
        return redirect("login")
    else:
        pass
    key = [{"id": token, "user": response["username"]}]
    conexao1 = requests.api.request(
        "GET",
        f"https://parseapi.back4app.com/classes/Empresa?where=%7B%22objectId%22%3A%20%22{id}%22%7D",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
            "accept": "application/json",
        },
    )
    key = [{"id": token, "user": abc["username"]}]
    dop = conexao1.json()
    dap = [x for x in dop["results"]]
    return render(request, "detail_empresa.html", {"lista": key, "lista2": dap})
