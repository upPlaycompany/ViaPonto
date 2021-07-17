from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
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
    req_logout = requests.api.request(
        "POST",
        "https://parseapi.back4app.com/logout",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
            "X-Parse-Session-Token": f"{token}",
        },
    )
    # logout(request)

    res_logout = req_logout.json()
    print(res_logout)

    if res_logout == {}:
        return redirect("home")
    else:
        return redirect("fail_default")


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
            return redirect("admin_dashboard", token=response["sessionToken"])
        elif status == "200" and response["gestor"] == False:
            return redirect("dashboard_colaborador", token=response["sessionToken"])
        else:
            return redirect("login_fail")

    return render(request, "login_colaborador.html")


def fail_default_colaborador(request, token):
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

    return render(request, "fail_default_colaborador.html", {"lista": key})


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
    usuario_id = usuario["objectId"]
    cargo_id = usuario["id_cargo"]["objectId"]
    departamento_id = usuario["id_departamento"]["objectId"]

    # PEGAR DO SERVIDOR
    data_hora = datetime.now()
    data_do_dia = data_hora.strftime("%d/%m/%Y")

    req_cargo = requests.api.request(
        "GET",
        f"https://parseapi.back4app.com/classes/Cargo/{cargo_id}",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
        },
    )
    carg = req_cargo.json()

    req_dep = requests.api.request(
        "GET",
        f"https://parseapi.back4app.com/classes/Departamento/{departamento_id}",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
        },
    )
    dep = req_dep.json()

    req_turno = requests.api.request(
        "GET",
        f"https://parseapi.back4app.com/classes/Turno?where=%7B%20%22id_departamento%22%3A%20%7B%20%22__type%22%3A%20%22Pointer%22%2C%20%22className%22%3A%20%22Departamento%22%2C%20%22objectId%22%3A%20%22{departamento_id}%22%20%7D%20%7D",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
        },
    )
    res_turno = req_turno.json()
    turno = [x for x in res_turno["results"]]

    req_ponto = requests.api.request(
        "GET",
        f"https://parseapi.back4app.com/classes/Ponto?where=%7B%20%22id_funcionario%22%3A%20%7B%20%22__type%22%3A%20%22Pointer%22%2C%20%22className%22%3A%20%22_User%22%2C%20%22objectId%22%3A%20%22{usuario_id}%22%20%7D%20%7D",
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

    return render(request, "dashboard_colaborador.html", {"lista": key, "user": usuario, "cargo": carg, "departamento": dep, "horarios": turno, "pontos": ponto, "data": data_do_dia})


def edit_perfil(request, token):
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
    usuario_id = usuario["objectId"]

    data = (usuario.get('data_nasc', ""))
    if data != "":
        date = datetime.strptime(data, "%d/%m/%Y").date()
        data = date.strftime("%Y-%m-%d")
        usuario["data_nasc"] = data

    if request.method == "POST":
        username = request.POST["username"]
        nome = request.POST["nome"]
        datanasc = request.POST["datanasc"]
        if datanasc != "":
            date = datetime.strptime(datanasc, "%Y-%m-%d").date()
            data = date.strftime("%d/%m/%Y")
            datanasc = data

        celular = request.POST["celular"]
        email_colab = request.POST["email"]
        # Endereço do Colaborador
        cep = request.POST["cep"]
        uf = request.POST["uf"]
        cidade = request.POST["cidade"]
        logradouro = request.POST["logradouro"]
        bairro = request.POST["bairro"]
        numero = request.POST["numero"]

        req_user = requests.api.request(
            "PUT",
            f"https://parseapi.back4app.com/classes/_User/{usuario_id}",
            headers={
                "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
                "X-Parse-Session-Token": f"{token}",
                "Content-Type": "application/json",
            },
            json={
                "username": f"{username}",
                "nome": f"{nome}",
                "data_nasc": f"{datanasc}",
                "email_colab": f"{email_colab}",
                "email": f"{email_colab}",
                "celular": f"{celular}",
                "cep": f"{cep}",
                "uf": f"{uf}",
                "cidade": f"{cidade}",
                "logradouro": f"{logradouro}",
                "bairro": f"{bairro}",
                "numero": f"{numero}",
            },
        )

        req_user.json()

        status = str(req_user.status_code)

        if status == "200":
            return redirect("dashboard_colaborador", token=token)
        else:
            return redirect("fail_default_colaborador", token=token)

    return render(request, "edit_perfil_colaborador.html", {"lista": key, "user": usuario})


def list_ponto(request, token):
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
    usuario_id = usuario["objectId"]

    req_ponto = requests.api.request(
        "GET",
        f"https://parseapi.back4app.com/classes/Ponto?where=%7B%20%22id_funcionario%22%3A%20%7B%20%22__type%22%3A%20%22Pointer%22%2C%20%22className%22%3A%20%22_User%22%2C%20%22objectId%22%3A%20%22{usuario_id}%22%20%7D%20%7D",
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
                "horario": x["horario"],
                "registro": x["registro"],
                "local_registro": x["local_registro"],
            }
            if str(x["createdAt"]) in datas
            else {
                "createdAt": "sem registro",
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

    return render( request, "list_ponto_colaborador.html",{"lista": key, "pontos": ponto_date, "start_data": start, "end_data": end})


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
    usuario_id = usuario["objectId"]
    empresa_id = usuario["id_empresa"]["objectId"]
    departamento_id = usuario["id_departamento"]["objectId"]
    DAYS = ["segunda", "terca", "quarta", "quinta", "sexta", "sabado", "domingo"]

    if request.method == "POST":
        lat = request.POST["lat"]
        long = request.POST["long"]
        rua = request.POST["rua"]
        bairro = request.POST["bairro"]
        cidade = request.POST["cidade"]
        estado = request.POST["estado"]

        if rua == "" or bairro == "" or cidade or estado == "":
            return redirect("fail_default_colaborador", token=token)
        
        # PEGAR DO SERVIDOR
        data_hora = datetime.now()
        indice_week = data_hora.weekday()

        # DADOS DO PONTO
        data_do_dia = data_hora.strftime("%d/%m/%Y")
        hora = data_hora.strftime("%H:%M")
        weekday = DAYS[indice_week]
        local_registro = f"{rua}" + ", " + f"{bairro}" + " - " + f"{cidade}" + " / " + f"{estado}"
        registro = ""

        req_ponto = requests.api.request(
            "GET",
            f"https://parseapi.back4app.com/classes/Ponto?where=%7B%20%22id_funcionario%22%3A%20%7B%20%22__type%22%3A%20%22Pointer%22%2C%20%22className%22%3A%20%22_User%22%2C%20%22objectId%22%3A%20%22{usuario_id}%22%20%7D%20%7D",
            headers={
                "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
            },
        )
        res_ponto = req_ponto.json()
        pontos = [x for x in res_ponto["results"]]

        for x in pontos:
            data = x["createdAt"]
            data = data[:10]
            date = datetime.strptime(data, "%Y-%m-%d").date()
            date = date.strftime("%d/%m/%Y")
            x["createdAt"] = date

        total_pontos = 0
        primeira_entrada = False
        primeira_saida = False
        segunda_entrada = False
        segunda_saida = False

        for ponto in pontos:
            if ponto["createdAt"] == data_do_dia:
                total_pontos += 1
                if ponto["registro"] == "1ª Entrada":
                    primeira_entrada = True
                if ponto["registro"] == "1ª Saída":
                    primeira_saida = True
                if ponto["registro"] == "2ª Entrada":
                    segunda_entrada = True
                if ponto["registro"] == "2ª Saída":
                    segunda_saida = True

        req_turno = requests.api.request('GET', f"https://parseapi.back4app.com/classes/Turno?where=%7B%22id_departamento%22%3A%20%7B%20%22__type%22%3A%20%22Pointer%22%2C%20%22className%22%3A%20%22Departamento%22%2C%20%22objectId%22%3A%20%22{departamento_id}%22%20%7D%20%7D",
                                        headers={
                                            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                                            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9"})
        res_turno = req_turno.json()
        turnos = [x for x in res_turno['results']]

        for turno in turnos:
            if turno["dia_da_semana"] == weekday:
                if turno["primeira_entrada"] != "nao definido":
                    if total_pontos == 0:
                        if hora >= turno["primeira_entrada"] and hora <= turno["primeira_saida"]:
                            print("Primeira Entrada: ", hora)
                            registro = "1ª Entrada"

                if turno["primeira_saida"] != "nao definido":
                    if total_pontos == 1 and primeira_entrada == True:
                        if hora <= turno["segunda_entrada"]:
                            print("Primeira Saída: ", hora)
                            registro = "1ª Saída"

                if turno["segunda_entrada"] != "nao definido":
                    if total_pontos == 2 and primeira_saida == True or total_pontos == 0:
                        if hora >= turno["segunda_entrada"] and hora <= turno["segunda_saida"]:
                            print("Segunda Entrada", hora)
                            registro = "2ª Entrada"

                if turno["segunda_saida"] != "nao definido":
                    if total_pontos == 3 and segunda_entrada == True or total_pontos == 1 and segunda_entrada == True:
                        if hora <= turno["segunda_saida"] or hora >= turno["segunda_saida"]:
                            print("Segunda Saída", hora)
                            registro = "2ª Saída"

        print("Data", data_do_dia)
        print("Dia", weekday)
        print("Registro", registro)
        print("Horario", hora)
        print("Total pontos", total_pontos)

        if total_pontos == 4:
            return redirect("fail_registro_ponto", token=token)

        # SALVAR O REGISTRO DO PONTO NO BANCO
        if registro != "":
            req_ponto = requests.api.request(
                "POST",
                f"https://parseapi.back4app.com/classes/Ponto",
                headers={
                    "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                    "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
                    "Content-Type": "application/json",
                },
                json={
                    "registro": f"{registro}",
                    "data": f"{data_do_dia}",
                    "dia_da_semana": f"{weekday}",
                    "horario": f"{hora}",
                    "local_registro": f"{local_registro}",
                    "id_empresa": {
                        "__type": "Pointer",
                        "className": "Empresa",
                        "objectId": empresa_id,
                    },
                    "id_funcionario": {
                        "__type": "Pointer",
                        "className": "_User",
                        "objectId": usuario_id,
                    },
                },
            )
            status = str(req_ponto.status_code)
            if status == "201":
                return redirect("dashboard_colaborador", token=token)
            else:
                return redirect("fail_default_colaborador", token=token)

        return redirect("fail_default_colaborador", token=token)

    return render(request, "registro_ponto.html", {"lista": key})


def fail_registro_ponto(request, token):
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

    return render(request, "fail_registro_ponto.html", {"lista": key})


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
            return redirect("admin_dashboard", token=response["sessionToken"])
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
    empresa_id = usuario["id_empresa"]["objectId"]
    data_atual = datetime.today()
    data_do_dia = data_atual.strftime("%d/%m/%Y")

    req_user = requests.api.request(
        "GET",
        f"https://parseapi.back4app.com/classes/_User?where=%7B%20%22id_empresa%22%3A%20%7B%20%22__type%22%3A%20%22Pointer%22%2C%20%22className%22%3A%20%22Empresa%22%2C%20%22objectId%22%3A%20%22{empresa_id}%22%20%7D%20%7D",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
        },
    )
    res_user = req_user.json()
    colab = [x for x in res_user["results"]]

    total_demitidos = 0
    for col in colab:
        if col["demitido"] == True or col["gestor"] == True:
            total_demitidos += 1

    num_colab = len(colab) - total_demitidos

    req_ponto = requests.api.request(
        "GET",
        f"https://parseapi.back4app.com/classes/Ponto?where=%7B%20%22id_empresa%22%3A%20%7B%20%22__type%22%3A%20%22Pointer%22%2C%20%22className%22%3A%20%22Empresa%22%2C%20%22objectId%22%3A%20%22{empresa_id}%22%20%7D%20%7D",
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

    data_atual = datetime.today()
    data_do_dia = data_atual.strftime("%d/%m/%Y")

    ponto_dia = [{"createdAt": x["createdAt"], "id_funcionario": {"objectId": x["id_funcionario"]["objectId"]}, "dia_da_semana": x["dia_da_semana"], "horario": x["horario"], "registro": x["registro"], "local_registro": x["local_registro"] } if str(x["createdAt"]) in data_do_dia else {"createdAt": "sem registro", "id_funcionario": {"objectId": "sem registro"}, "dia_da_semana": "sem registro", "horario": "sem registro", "registro": "sem registro", "local_registro": "sem registro" } for x in ponto]

    total_prim_entrada = 0
    total_prim_saida = 0
    total_seg_entrada = 0
    total_seg_saida = 0

    for p in ponto_dia:
        if p["createdAt"] != "sem registro":
            if p["registro"] == "1ª Entrada":
                total_prim_entrada += 1
            if p["registro"] == "1ª Saída":
                total_prim_saida += 1
            if p["registro"] == "2ª Entrada":
                total_seg_entrada += 1
            if p["registro"] == "2ª Saída":
                total_seg_saida += 1

    total_pend_1 = num_colab - total_prim_entrada
    total_pend_2 = num_colab - total_prim_saida
    total_pend_3 = num_colab - total_seg_entrada
    total_pend_4 = num_colab - total_seg_saida

    return render(request, "dashboard.html", {"lista": key, "total_colab": num_colab, "data": data_do_dia, "total_ent1": total_prim_entrada, "total_sai1": total_prim_saida, "total_ent2": total_seg_entrada, "total_sai2": total_seg_saida, "total_pend1": total_pend_1, "total_pend2": total_pend_2, "total_pend3": total_pend_3, "total_pend4": total_pend_4})


def total_registrados(request, token):
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
        f"https://parseapi.back4app.com/classes/_User?where=%7B%20%22id_empresa%22%3A%20%7B%20%22__type%22%3A%20%22Pointer%22%2C%20%22className%22%3A%20%22Empresa%22%2C%20%22objectId%22%3A%20%22{empresa_id}%22%20%7D%20%7D",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
        },
    )
    res_user = req_user.json()
    colab = [x for x in res_user["results"]]

    req_ponto = requests.api.request(
        "GET",
        f"https://parseapi.back4app.com/classes/Ponto?where=%7B%20%22id_empresa%22%3A%20%7B%20%22__type%22%3A%20%22Pointer%22%2C%20%22className%22%3A%20%22Empresa%22%2C%20%22objectId%22%3A%20%22{empresa_id}%22%20%7D%20%7D",
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

    data_atual = datetime.today()
    data_do_dia = data_atual.strftime("%d/%m/%Y")

    ponto_dia = [{"createdAt": x["createdAt"], "id_funcionario": {"objectId": x["id_funcionario"]["objectId"]}, "dia_da_semana": x["dia_da_semana"], "horario": x["horario"], "registro": x["registro"], "local_registro": x["local_registro"] } if str(x["createdAt"]) in data_do_dia else {"createdAt": "sem registro", "id_funcionario": {"objectId": "sem registro"}, "dia_da_semana": "sem registro", "horario": "sem registro", "registro": "sem registro", "local_registro": "sem registro" } for x in ponto]

    return render(request, "total_registrados.html", {"lista": key, "pontos": ponto_dia, "colaboradores": colab})


def total_pendentes(request, token):
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
        f"https://parseapi.back4app.com/classes/_User?where=%7B%20%22id_empresa%22%3A%20%7B%20%22__type%22%3A%20%22Pointer%22%2C%20%22className%22%3A%20%22Empresa%22%2C%20%22objectId%22%3A%20%22{empresa_id}%22%20%7D%20%7D",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
        },
    )
    res_user = req_user.json()
    colab = [x for x in res_user["results"]]

    req_ponto = requests.api.request(
        "GET",
        f"https://parseapi.back4app.com/classes/Ponto?where=%7B%20%22id_empresa%22%3A%20%7B%20%22__type%22%3A%20%22Pointer%22%2C%20%22className%22%3A%20%22Empresa%22%2C%20%22objectId%22%3A%20%22{empresa_id}%22%20%7D%20%7D",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
        },
    )
    res_ponto = req_ponto.json()
    ponto = [x for x in res_ponto["results"]]

    for p in ponto:
        data = p["createdAt"]
        data = data[:10]
        date = datetime.strptime(data, "%Y-%m-%d").date()
        date = date.strftime("%d/%m/%Y")
        p["createdAt"] = date

    # PEGAR DO SERVIDOR
    data_hora = datetime.now()
    data_do_dia = data_hora.strftime("%d/%m/%Y")

    ponto_dia = [{"createdAt": x["createdAt"], "id_funcionario": {"objectId": x["id_funcionario"]["objectId"]}, "dia_da_semana": x["dia_da_semana"], "horario": x["horario"], "registro": x["registro"], "local_registro": x["local_registro"] } if str(x["createdAt"]) in data_do_dia else {"createdAt": "sem registro", "id_funcionario": {"objectId": "sem registro"}, "dia_da_semana": "sem registro", "horario": "sem registro", "registro": "sem registro", "local_registro": "sem registro" } for x in ponto]

    pendentes_prim_entrada = []
    pendentes_prim_saida = []
    pendentes_seg_entrada = []
    pendentes_seg_saida = []

    for colaborador in colab:
        if colaborador["demitido"] != True and colaborador["gestor"] != True:
            primeira_entrada = False
            primeira_saida = False
            segunda_entrada = False
            total_pontos = 0
            for ponto in ponto_dia:
                if ponto["id_funcionario"]["objectId"] == colaborador["objectId"]:
                    total_pontos += 1
                    if ponto["registro"] == "1ª Entrada":
                        primeira_entrada = True
                    if ponto["registro"] == "1ª Saída":
                        primeira_saida = True
                    if ponto["registro"] == "2ª Entrada":
                        segunda_entrada = True
            if total_pontos == 0:
                colabId = colaborador["objectId"]
                pendentes_prim_entrada.append(colabId)
            
            elif total_pontos == 1 and primeira_entrada == True:
                colabId2 = colaborador["objectId"]
                pendentes_prim_saida.append(colabId2)
            
            elif total_pontos == 2 and primeira_saida == True:
                colabId3 = colaborador["objectId"]
                pendentes_seg_entrada.append(colabId3)
            
            elif total_pontos == 3 and segunda_entrada == True:
                colabId4 = colaborador["objectId"]
                pendentes_seg_saida.append(colabId4)

    total_p1 = len(pendentes_prim_entrada)
    total_p2 = len(pendentes_prim_saida)
    total_p3 = len(pendentes_seg_entrada)
    total_p4 = len(pendentes_seg_saida)
    if total_p1 == 0:
        pendentes_prim_entrada = ""
    if total_p2 == 0:
        pendentes_prim_saida = ""
    if total_p3 == 0:
        pendentes_seg_entrada = ""
    if total_p4 == 0:
        pendentes_seg_saida = ""

    return render(request, "total_pendentes.html", {"lista": key, "pontos": ponto_dia,"colaboradores": colab, "pendentes1": pendentes_prim_entrada, "pendentes2": pendentes_prim_saida, "pendentes3": pendentes_seg_entrada, "pendentes4": pendentes_seg_saida})


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

    req_fer = requests.api.request(
        "GET",
        f"https://parseapi.back4app.com/classes/Feriado?where=%7B%22id_empresa%22%3A%20%7B%20%22__type%22%3A%20%22Pointer%22%2C%20%22className%22%3A%20%22Empresa%22%2C%20%22objectId%22%3A%20%22{empresa_id}%22%20%7D%20%7D",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
        },
    )
    res_fer = req_fer.json()
    feriado = [x for x in res_fer["results"]]

    return render(request, "list_feriado.html", {"lista": key, "feriados": feriado, "departamentos": departamento})


def cadastro_feriado(request, token):
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
        nome = request.POST["nome_feriado"]
        data = request.POST["data_feriado"]
        departamento_id = request.POST["departamento"]
        date = datetime.strptime(data, "%Y-%m-%d").date()
        date = date.strftime("%d/%m/%Y")

        req_fer = requests.api.request(
            "POST",
            f"https://parseapi.back4app.com/classes/Feriado",
            headers={
                "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
                "Content-Type": "application/json",
            },
            json={
                "nome": f"{nome}",
                "data": f"{date}",
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
        status = str(req_fer.status_code)
        if status == "201":
            return redirect("list_feriado", token=token)
        else:
            return redirect("fail_default", token=token)

    return render(request, "cadastro_feriado.html", {"lista": key, "departamentos": departamento})


def edit_feriado(request, token, id):
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

    req_fer = requests.api.request(
        "GET",
        f"https://parseapi.back4app.com/classes/Feriado/{id}",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
        },
    )
    res_fer = req_fer.json()

    data = res_fer["data"]
    date = datetime.strptime(data, "%d/%m/%Y").date()
    data = date.strftime("%Y-%m-%d")
    res_fer["data"] = data

    if request.method == "POST":
        nome = request.POST["nome_feriado"]
        data = request.POST["data_feriado"]
        departamento_id = request.POST["departamento"]
        date = datetime.strptime(data, "%Y-%m-%d").date()
        date = date.strftime("%d/%m/%Y")

        req_fer = requests.api.request(
            "PUT",
            f"https://parseapi.back4app.com/classes/Feriado/{id}",
            headers={
                "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
                "Content-Type": "application/json",
            },
            json={
                "nome": f"{nome}",
                "data": f"{date}",
                "id_departamento": {
                    "__type": "Pointer",
                    "className": "Departamento",
                    "objectId": departamento_id,
                },
            },
        )
        status = str(req_fer.status_code)
        if status == "200":
            return redirect("list_feriado", token=token)
        else:
            return redirect("fail_default", token=token)

    return render(request, "edit_feriado.html", {"lista": key, "feriado": res_fer, "departamentos": departamento})


def delete_feriado(request, token, id):
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

    req_fer = requests.api.request(
        "DELETE",
        f"https://parseapi.back4app.com/classes/Feriado/{id}",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
        },
    )

    status = str(req_fer.status_code)
    if status == "200":
        return redirect("list_feriado", token=token)
    else:
        return redirect("fail_default", token=token)


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

    req_turno = requests.api.request(
        "GET",
        f"https://parseapi.back4app.com/classes/Turno/{id}",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
        },
    )
    turno = req_turno.json()

    if request.method == "POST":
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
                "primeira_entrada": f"{primeira_entrada}",
                "primeira_saida": f"{primeira_saida}",
                "segunda_entrada": f"{segunda_entrada}",
                "segunda_saida": f"{segunda_saida}",
            },
        )
        status = str(req_turn.status_code)
        if status == "200":
            return redirect("list_horario", token=token)
        else:
            return redirect("fail_default", token=token)

    return render(request, "edit_horario.html", {"lista": key, "horario": turno})


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

    req_local = requests.api.request(
        "GET",
        f"https://parseapi.back4app.com/classes/Local?where=%7B%22id_empresa%22%3A%20%7B%20%22__type%22%3A%20%22Pointer%22%2C%20%22className%22%3A%20%22Empresa%22%2C%20%22objectId%22%3A%20%22{empresa_id}%22%20%7D%20%7D",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
        },
    )
    res_local = req_local.json()
    local = [x for x in res_local["results"]]

    return render(request, "list_local.html", {"lista": key, "locais": local, "departamentos": departamento})


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
        nome = request.POST["nome_local"]
        departamento_id = request.POST["departamento"]
        cep = request.POST["cep"]
        uf = request.POST["uf"]
        cidade = request.POST["cidade"]
        logradouro = request.POST["logradouro"]
        bairro = request.POST["bairro"]
        numero = request.POST["numero"]

        req_cargo = requests.api.request(
            "POST",
            f"https://parseapi.back4app.com/classes/Local",
            headers={
                "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
                "Content-Type": "application/json",
            },
            json={
                "nome": f"{nome}",
                "cep": f"{cep}",
                "uf": f"{uf}",
                "cidade": f"{cidade}",
                "logradouro": f"{logradouro}",
                "bairro": f"{bairro}",
                "numero": f"{numero}",
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
        status = str(req_cargo.status_code)
        if status == "201":
            return redirect("list_local", token=token)
        else:
            return redirect("fail_default", token=token)

    return render(request, "cadastro_local.html", {"lista": key, "departamentos": departamento})


def edit_local(request, token, id):
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

    req_local = requests.api.request(
        "GET",
        f"https://parseapi.back4app.com/classes/Local/{id}",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
        },
    )
    res_local = req_local.json()

    if request.method == "POST":
        nome = request.POST["nome_local"]
        departamento_id = request.POST["departamento"]
        cep = request.POST["cep"]
        uf = request.POST["uf"]
        cidade = request.POST["cidade"]
        logradouro = request.POST["logradouro"]
        bairro = request.POST["bairro"]
        numero = request.POST["numero"]

        req_cargo = requests.api.request(
            "PUT",
            f"https://parseapi.back4app.com/classes/Local/{id}",
            headers={
                "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
                "Content-Type": "application/json",
            },
            json={
                "nome": f"{nome}",
                "cep": f"{cep}",
                "uf": f"{uf}",
                "cidade": f"{cidade}",
                "logradouro": f"{logradouro}",
                "bairro": f"{bairro}",
                "numero": f"{numero}",
                "id_departamento": {
                    "__type": "Pointer",
                    "className": "Departamento",
                    "objectId": departamento_id,
                },
            },
        )
        status = str(req_cargo.status_code)
        if status == "200":
            return redirect("list_local", token=token)
        else:
            return redirect("fail_default", token=token)

    return render(request, "edit_local.html", {"lista": key, "local": res_local, "departamentos": departamento})


def delete_local(request, token, id):
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

    req_local = requests.api.request(
        "DELETE",
        f"https://parseapi.back4app.com/classes/Local/{id}",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
        },
    )

    status = str(req_local.status_code)
    if status == "200":
        return redirect("list_local", token=token)
    else:
        return redirect("fail_default", token=token)


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
def relatorio_pontos(request, token):
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

    if request.method == "POST":
        departamento_id = request.POST["departamento"]

        req_user = requests.api.request(
            "GET",
            f"https://parseapi.back4app.com/classes/_User?where=%7B%22id_departamento%22%3A%20%7B%20%22__type%22%3A%20%22Pointer%22%2C%20%22className%22%3A%20%22Departamento%22%2C%20%22objectId%22%3A%20%22{departamento_id}%22%20%7D%20%7D",
            headers={
                "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
            },
        )
        res_user = req_user.json()
        colaborador = [x for x in res_user["results"]]

        status = str(res_user.status_code)
        if status == "200":
            return redirect("espelho_registros.html", token=token)
        else:
            return redirect("fail_default", token=token)

    return render(request, "relatorio_pontos.html", {"lista": key, "colaboradores": colaborador, "cargos": cargo, "departamentos": departamento})


def registros_ponto(request, token, id_user):
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
        f"https://parseapi.back4app.com/classes/_User/{id_user}",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
        },
    )
    colab = req_user.json()

    req_ponto = requests.api.request(
        "GET",
        f"https://parseapi.back4app.com/classes/Ponto?where=%7B%20%22id_funcionario%22%3A%20%7B%20%22__type%22%3A%20%22Pointer%22%2C%20%22className%22%3A%20%22_User%22%2C%20%22objectId%22%3A%20%22{id_user}%22%20%7D%20%7D",
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

        start_data = start.strftime("%Y-%m-%d")
        end_data = end.strftime("%Y-%m-%d")

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

        ponto_date = [{"createdAt": x["createdAt"], "id_funcionario": {"objectId": x["id_funcionario"]["objectId"]}, "dia_da_semana": x["dia_da_semana"], "horario": x["horario"], "registro": x["registro"], "local_registro": x["local_registro"] } if str(x["createdAt"]) in datas else {"createdAt": "sem registro", "id_funcionario": {"objectId": "sem registro"}, "dia_da_semana": "sem registro", "horario": "sem registro", "registro": "sem registro", "local_registro": "sem registro" } for x in ponto]
    else:
        ponto_date = ponto
        start = "0"
        end = "0"
        start_data = ""
        end_data = ""
    print(start, end)

    return render(request, "registros_ponto.html", {"lista": key, "colaborador": colab, "Id_user": id_user, "pontos": ponto_date, "start_data": start, "end_data": end, "start_date": start_data, "end_date": end_data})


def espelho_registros(request, token):
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

    if request.method == "POST":
        departamento_id = request.POST["departamento"]

        req_user = requests.api.request(
            "GET",
            f"https://parseapi.back4app.com/classes/_User?where=%7B%22id_departamento%22%3A%20%7B%20%22__type%22%3A%20%22Pointer%22%2C%20%22className%22%3A%20%22Departamento%22%2C%20%22objectId%22%3A%20%22{departamento_id}%22%20%7D%20%7D",
            headers={
                "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
                "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
            },
        )
        res_user = req_user.json()
        colaborador = [x for x in res_user["results"]]

        status = str(res_user.status_code)
        if status == "200":
            return redirect("espelho_registros.html", token=token)
        else:
            return redirect("fail_default", token=token)

    return render(request, "espelho_registros.html", {"lista": key, "colaboradores": colaborador, "cargos": cargo, "departamentos": departamento})


def folha_ponto(request, token, id_user):
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
        f"https://parseapi.back4app.com/classes/_User/{id_user}",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
        },
    )
    colab = req_user.json()

    req_ponto = requests.api.request(
        "GET",
        f"https://parseapi.back4app.com/classes/Ponto?where=%7B%20%22id_funcionario%22%3A%20%7B%20%22__type%22%3A%20%22Pointer%22%2C%20%22className%22%3A%20%22_User%22%2C%20%22objectId%22%3A%20%22{id_user}%22%20%7D%20%7D",
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

    mes_lista = [
        {
            "num": "01",
            "nome": "Janeiro",
        },
        {
            "num": "02",
            "nome": "Fevereiro",
        },
        {
            "num": "03",
            "nome": "Março",
        },
        {
            "num": "04",
            "nome": "Abril",
        },
        {
            "num": "05",
            "nome": "Maio",
        },
        {
            "num": "06",
            "nome": "Junho",
        },
        {
            "num": "07",
            "nome": "Julho",
        },
        {
            "num": "08",
            "nome": "Agosto",
        },
        {
            "num": "09",
            "nome": "Setembro",
        },
        {
            "num": "10",
            "nome": "Outubro",
        },
        {
            "num": "11",
            "nome": "Novembro",
        },
        {
            "num": "12",
            "nome": "Dezembro",
        },
    ]

    mes_select = request.GET.get("mes")

    if mes_select:
        data_atual = datetime.today()
        
        ano = data_atual.year
        dias_mes = ""

        if mes_select == "01" or mes_select == "03" or mes_select == "05" or mes_select == "07" or mes_select == "08" or mes_select == "10" or mes_select == "12":
            dias_mes = 31
        elif mes_select == "02":
            if ano % 100 != 0 and ano % 4 == 0 or ano % 400 == 0:
                # É UM ANO BISSEXTO
                dias_mes = 29
            else:
                # NÃO É UM ANO BISSEXTO
                dias_mes = 28
        elif mes_select == "04" or mes_select == "06" or mes_select == "09" or mes_select == "11":
            dias_mes = 30

        dias = list(range(1, dias_mes + 1))
        total_dias = len(dias)

        datas = tuple(
            [
                f"0{dias[x]}" + "/" + f"{mes_select}" + "/" + f"{ano}"
                if dias[x] < 10
                else f"{dias[x]}" + "/" + f"{mes_select}" + "/" + f"{ano}"
                for x in range(total_dias)
            ]
        )

        ponto_mes = [{"createdAt": x["createdAt"], "id_funcionario": {"objectId": x["id_funcionario"]["objectId"]}, "dia_da_semana": x["dia_da_semana"], "horario": x["horario"], "registro": x["registro"], "local_registro": x["local_registro"] } if str(x["createdAt"]) in datas else {"createdAt": "sem registro", "id_funcionario": {"objectId": "sem registro"}, "dia_da_semana": "sem registro", "horario": "sem registro", "registro": "sem registro", "local_registro": "sem registro" } for x in ponto]
    else:
        ponto_mes = ponto

    return render(request, "folha_ponto.html", {"lista": key, "colaborador": colab, "Id_user": id_user, "pontos": ponto_mes, "mes_sel": mes_select, "meses": mes_lista})


# GERAR PDF
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

    req_user = requests.api.request(
        "GET",
        f"https://parseapi.back4app.com/classes/_User/{id_user}",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
        },
    )
    colab = req_ser.json()

    req_ponto = requests.api.request(
        "GET",
        f"https://parseapi.back4app.com/classes/Ponto?where=%7B%20%22id_funcionario%22%3A%20%7B%20%22__type%22%3A%20%22Pointer%22%2C%20%22className%22%3A%20%22_User%22%2C%20%22objectId%22%3A%20%22{id_user}%22%20%7D%20%7D",
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
        data_str = date.strftime("%d/%m/%Y")
        x["data"] = date.day
        x["createdAt"] = data_str

    if start_date != "0" and end_date != "0":
        start = datetime.strptime(start_date, "%Y-%m-%d").date()
        end = datetime.strptime(end_date, "%Y-%m-%d").date()
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
                "dia": x["data"],
                "mes": x["mes_start"],
                "ano": x["ano_start"],
                "id_funcionario": {"objectId": x["id_funcionario"]["objectId"]},
                "horario": x["horario"],
                "registro": x["registro"]
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


def gerar_folha_ponto(request, token, id_user, mes):
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

    req_user = requests.api.request(
        "GET",
        f"https://parseapi.back4app.com/classes/_User/{id_user}",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
        },
    )
    colab = req_user.json()

    req_ponto = requests.api.request(
        "GET",
        f"https://parseapi.back4app.com/classes/Ponto?where=%7B%20%22id_funcionario%22%3A%20%7B%20%22__type%22%3A%20%22Pointer%22%2C%20%22className%22%3A%20%22_User%22%2C%20%22objectId%22%3A%20%22{id_user}%22%20%7D%20%7D",
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
        dia = data[:2]
        date = datetime.strptime(data, "%Y-%m-%d").date()
        date = date.strftime("%d/%m/%Y")
        x["createdAt"] = date
        x["data"] = dia

    mes_lista = [
        {
            "num": "01",
            "nome": "Janeiro",
        },
        {
            "num": "02",
            "nome": "Fevereiro",
        },
        {
            "num": "03",
            "nome": "Março",
        },
        {
            "num": "04",
            "nome": "Abril",
        },
        {
            "num": "05",
            "nome": "Maio",
        },
        {
            "num": "06",
            "nome": "Junho",
        },
        {
            "num": "07",
            "nome": "Julho",
        },
        {
            "num": "08",
            "nome": "Agosto",
        },
        {
            "num": "09",
            "nome": "Setembro",
        },
        {
            "num": "10",
            "nome": "Outubro",
        },
        {
            "num": "11",
            "nome": "Novembro",
        },
        {
            "num": "12",
            "nome": "Dezembro",
        },
    ]

    if mes != "None":
        for m in mes_lista:
            if m["num"] == mes:
                mes_nome = m["nome"]

        mes_select = mes

        data_atual = datetime.today()
        
        ano_atual = data_atual.year
        dias_mes = ""

        if mes_select == "01" or mes_select == "03" or mes_select == "05" or mes_select == "07" or mes_select == "08" or mes_select == "10" or mes_select == "12":
            dias_mes = 31
        elif mes_select == "02":
            if ano_atual % 100 != 0 and ano_atual % 4 == 0 or ano_atual % 400 == 0:
                # É UM ANO BISSEXTO
                dias_mes = 29
            else:
                # NÃO É UM ANO BISSEXTO
                dias_mes = 28
        elif mes_select == "04" or mes_select == "06" or mes_select == "09" or mes_select == "11":
            dias_mes = 30

        dias = list(range(1, dias_mes + 1))
        total_dias = len(dias)

        datas = tuple(
            [
                f"0{dias[x]}" + "/" + f"{mes_select}" + "/" + f"{ano_atual}"
                if dias[x] < 10
                else f"{dias[x]}" + "/" + f"{mes_select}" + "/" + f"{ano_atual}"
                for x in range(total_dias)
            ]
        )

        ponto_mes = [{"createdAt": x["createdAt"], "id_funcionario": {"objectId": x["id_funcionario"]["objectId"]}, "dia": x["data"], "horario": x["horario"], "registro": x["registro"], "local_registro": x["local_registro"] } if str(x["createdAt"]) in datas else {"createdAt": "sem registro", "id_funcionario": {"objectId": "sem registro"}, "dia": "sem registro", "horario": "sem registro", "registro": "sem registro" } for x in ponto]
    else:
        ponto_mes = ponto
        return redirect("fail_default", token=token)

    return rendering.render_to_pdf_response(
        request=request,
        context={
            "empresa": emp,
            "cargos": cargo,
            "departamentos": departamento,
            "colaborador": colab,
            "pontos": ponto_mes,
            "nome_mes": mes_nome,
            "mes": mes_select,
            "ano": ano_atual,
            "meses": mes_lista,
            "total_days": range(total_dias + 1),
        },
        template="pdf-folha-ponto.html",
        encoding="utf-8",
    )


# ÁREA ADMINISTRATIVA #
def admin_dashboard(request, token):
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
    elif response["admin"] == False:
        return redirect("login")
    else:
        pass
    key = [{"id": token, "user": response["username"]}]

    req_user = requests.api.request(
        "GET",
        f"https://parseapi.back4app.com/classes/_User",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
        },
    )
    res_user = req_user.json()
    usuario = [x for x in res_user["results"]]
    num_usuario = len(usuario) - 1

    req_emp = requests.api.request(
        "GET",
        f"https://parseapi.back4app.com/classes/Empresa",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
            "accept": "application/json",
        },
    )
    res_emp = req_emp.json()
    empresa = [x for x in res_emp["results"]]
    num_empresa = len(empresa)

    return render(
        request,
        "admin_dashboard.html",
        {"lista": key, "usuarios": num_usuario, "empresas": num_empresa},
    )


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
    elif response["admin"] == False:
        return redirect("login")
    else:
        pass
    key = [{"id": token, "user": response["username"]}]

    req_empresa = requests.api.request(
        "GET",
        f"https://parseapi.back4app.com/classes/Empresa",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
            "accept": "application/json",
        },
    )
    res_empresa = req_empresa.json()

    empresa = [x for x in res_empresa["results"]]

    return render(request, "list_empresa.html", {"lista": key, "empresas": empresa})


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
    elif response["admin"] == False:
        return redirect("login")
    else:
        pass
    key = [{"id": token, "user": response["username"]}]

    req_emp = requests.api.request(
        "GET",
        f"https://parseapi.back4app.com/classes/Empresa/{id}",
        headers={
            "X-Parse-Application-Id": "Sgx1E183pBATq8APs006w2ACmAPqpkk33jJwRGC6",
            "X-Parse-REST-API-Key": "lA1fgtFCTA2A5o0ebhuQM8T7DSAErYCPMF4jQtp9",
            "accept": "application/json",
        },
    )
    res_emp = req_emp.json()

    return render(request, "detail_empresa.html", {"lista": key, "empresa": res_emp})
