from django.core.cache import cache
import secrets
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import JsonResponse
import io
import re
from datetime import datetime
from collections import defaultdict

import segno
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from qrcode.models import Cliente, ClienteQtd


# ====================
# ÁREA RESTRITA - REQUER LOGIN
# ====================

@login_required
def index(request):
    try:
        empresa = ClienteQtd.objects.get(cnpj=request.user.username)
        qtd = empresa.qtd_convites
    except ClienteQtd.DoesNotExist:
        qtd = 0

    return render(request, "index.html", {'convites': qtd})


@login_required
def gerar_pdf_qrcodes(request):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    empresas = defaultdict(list)
    for convidado in Cliente.objects.all().order_by('cnpj'):
        empresas[convidado.cnpj, convidado.razsoc].append(convidado)

    for (cnpj, razsoc), convidados in empresas.items():
        # Cabeçalho com nome da empresa
        c.setFont("Helvetica-Bold", 20)
        c.setFillColorRGB(0, 0, 0)
        c.drawCentredString(width / 2, height - 50, f"{razsoc} ({cnpj})")

        y = height - 100
        x = 30 * mm
        qr_size = 35 * mm
        padding_x = 15 * mm
        padding_y = 50 * mm
        count = 0
        qr_per_row = 4

        for convidado in convidados:
            qr = segno.make(
                f"https://qrcode-festao-dnsf.onrender.com/validar/?codigo={convidado.cpf}")
            qr_buffer = io.BytesIO()
            qr.save(qr_buffer, kind='png', scale=3)
            qr_buffer.seek(0)
            qr_img = ImageReader(qr_buffer)

            c.drawImage(qr_img, x, y - qr_size, width=qr_size, height=qr_size)
            c.setFont("Helvetica", 9)
            c.drawCentredString(x + qr_size / 2, y -
                                qr_size - 10, convidado.nome.upper())

            x += qr_size + padding_x
            count += 1

            if count % qr_per_row == 0:
                x = 30 * mm
                y -= padding_y

            if y < 80 * mm:
                c.setFont("Helvetica-Oblique", 9)
                c.setFillColorRGB(0.3, 0.3, 0.3)
                c.drawRightString(
                    width - 20, 20, f"Página {c.getPageNumber()}")
                c.drawString(
                    20, 20, f"Geração: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
                c.showPage()

                # Recomeça a nova página com título
                c.setFont("Helvetica-Bold", 20)
                c.setFillColorRGB(0, 0, 0)
                c.drawCentredString(width / 2, height - 50,
                                    f"{razsoc} ({cnpj})")
                y = height - 100
                x = 30 * mm
                count = 0

        # Finaliza a última página do grupo
        c.setFont("Helvetica-Oblique", 9)
        c.setFillColorRGB(0.3, 0.3, 0.3)
        c.drawRightString(width - 20, 20, f"Página {c.getPageNumber()}")
        c.drawString(
            20, 20, f"Geração: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        c.showPage()

    c.save()
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')


@login_required
def gerador(request):
    cnpj = cnpj = request.user.username
    convidados = []

    if cnpj:
        convidados = Cliente.objects.filter(cnpj=cnpj)
        return render(request, 'pages/gerador.html', {
            'convidados': convidados,
            'cnpj_consultado': cnpj
        })

    return render(request, 'pages/gerador.html')


@login_required
def cadastro(request):
    if request.method == 'GET':
        cnpj = request.user.username
        try:
            empresa = ClienteQtd.objects.get(cnpj=cnpj)
            qtd = empresa.qtd_convites
            return render(request, 'pages/cadastro.html', {
                'convites': qtd,
                'cnpj': empresa.cnpj,
                'razsoc': empresa.razsoc,
                'cpf_responsavel': '',
                'nome_responsavel': '',
                'total': range(qtd),
            })
        except ClienteQtd.DoesNotExist:
            return render(request, 'pages/cadastro.html', {'erro': 'CNPJ não encontrado na lista de clientes.'})

    elif request.method == 'POST' and 'cnpj_final' in request.POST:
        cnpj = request.POST['cnpj_final']
        razsoc = request.POST.get('razsoc_final', '').strip()
        cpf_responsavel = request.POST.get('cpf_responsavel_final', '').strip()
        nome_responsavel = request.POST.get(
            'nome_responsavel_final', '').strip()
        convidados = []

        cliente_qtd = ClienteQtd.objects.get(cnpj=cnpj)
        qtd = cliente_qtd.qtd_convites

        if qtd == 0:
            return render(request, 'pages/cadastro.html', {
                'erro': 'Você já cadastrou todos os convites disponíveis.',
                'cnpj': cnpj,
                'convites': qtd,
                'mensagem': 'Não há mais convites disponíveis.'
            })

        if Cliente.objects.filter(cpf=cpf_responsavel).exists():
            return render(request, 'pages/cadastro.html', {
                'erro': f'O CPF {cpf_responsavel} já está cadastrado.',
                'convites': qtd,
                'cnpj': cnpj,
                'razsoc': razsoc,
                'total': range(qtd),
            })

        for i in range(qtd):
            cpf_raw = request.POST.get(f'cpf_{i}', '').strip()
            nome = request.POST.get(f'nome_{i}', '').strip()
            cpf = re.sub(r'\D', '', cpf_raw)

            if not cpf or len(cpf) != 11 or not cpf.isdigit():
                return render(request, 'pages/cadastro.html', {
                    'erro': f'CPF inválido no convidado {i+1}.',
                    'convites': qtd,
                    'cnpj': cnpj,
                    'razsoc': razsoc,
                    'total': range(qtd),
                })

            if len(nome.split()) < 2:
                return render(request, 'pages/cadastro.html', {
                    'erro': f'Digite o nome completo do convidado {i+1}.',
                    'convites': qtd,
                    'cnpj': cnpj,
                    'razsoc': razsoc,
                    'total': range(qtd),
                })

            if Cliente.objects.filter(cpf=cpf).exists():
                return render(request, 'pages/cadastro.html', {
                    'erro': f'O CPF {cpf} já está cadastrado.',
                    'convites': qtd,
                    'cnpj': cnpj,
                    'razsoc': razsoc,
                    'total': range(qtd),
                })

            convidados.append((cpf, nome))

        for cpf, nome in convidados:
            Cliente.objects.create(
                cpf=cpf,
                nome=nome,
                cnpj=cnpj,
                razsoc=razsoc,
                checkin='N',
                data_hora=datetime.now()
            )

        cliente_qtd.qtd_convites -= len(convidados)
        cliente_qtd.save()

        return redirect('index')

    return render(request, 'pages/cadastro.html')


# ====================
# ÁREA PÚBLICA
# ====================


def checkin(request):
    return render(request, "checkin.html")


def validador(request):
    return render(request, "pages/validador.html")


def validar(request):
    codigo = request.GET.get('codigo', '').strip()

    if codigo:
        try:
            cliente = Cliente.objects.get(cpf=codigo)

            if cliente.checkin == 'S':
                return render(request, 'resposta/validado.html', {'codigo': codigo})

            cliente.checkin = 'S'
            cliente.data_hora = datetime.now()
            cliente.save(update_fields=['checkin', 'data_hora'])

            return render(request, 'resposta/aprovado.html', {'cliente': cliente})

        except Cliente.DoesNotExist:
            return render(request, 'resposta/negado.html', {'codigo': codigo})

    return redirect('index')


def aprovado(request):
    return render(request, "resposta/aprovado.html")


def negado(request):
    return render(request, "resposta/negado.html")


def validado(request):
    return render(request, "resposta/validado.html")


def buscar_email_por_cnpj(request):
    cnpj = request.GET.get('cnpj')
    try:
        cliente = ClienteQtd.objects.get(cnpj=cnpj)
        return JsonResponse({'email': cliente.email})
    except ClienteQtd.DoesNotExist:
        return JsonResponse({'email': ''})


def mascarar_email(email):
    try:
        usuario, dominio = email.split("@")
        if len(usuario) <= 4:
            # Se muito curto, mostra só o primeiro e o último
            usuario_mascarado = usuario[0] + "*" * \
                (len(usuario) - 2) + usuario[-1]
        else:
            usuario_mascarado = usuario[:3] + \
                "*" * (len(usuario) - 4) + usuario[-1]
        return f"{usuario_mascarado}@{dominio}"
    except Exception:
        return "***@***"


def cadastrar_password(request):
    message = None
    if request.method == 'POST':
        cnpj = request.POST.get('cnpj', '').strip()

        try:
            cliente = ClienteQtd.objects.get(cnpj=cnpj)
            if cliente.email:
                # Gera token seguro
                token = secrets.token_urlsafe(32)
                cache.set(token, cnpj, timeout=3600)  # expira em 1 hora

                # Link com token
                link = f"https://qrcode-festao-dnsf.onrender.com/cadastrar-senha/confirmar/?token={token}"

                # Envia o e-mail
                send_mail(
                    subject='Cadastro de Senha',
                    message=f"Olá, você solicitou um cadastro de senha. Clique no link abaixo para cadastrar sua senha:\n\n{link}",
                    from_email='suporte@agross.com.br',
                    recipient_list=[cliente.email],
                )
                email_mascarado = mascarar_email(cliente.email)
                message = f"Um e-mail com instruções para cadastrar sua senha foi enviado para {email_mascarado}."
            else:
                message = "O CNPJ informado não possui um e-mail cadastrado."

        except ClienteQtd.DoesNotExist:
            message = "CNPJ não encontrado."

    return render(request, 'cadastro/cadastrar_password.html', {'message': message})


def cadastrar_senha(request):
    token = request.GET.get('token')
    cnpj = cache.get(token)
    message = None

    if not cnpj:
        return render(request, 'cadastro/cadastrar_confirm.html', {'erro': 'Token inválido ou expirado.'})

    try:
        cliente = ClienteQtd.objects.get(cnpj=cnpj)
    except ClienteQtd.DoesNotExist:
        return render(request, 'cadastro/cadastrar_confirm.html', {'erro': 'CNPJ inválido.'})

    if request.method == 'POST':
        senha1 = request.POST.get('senha1', '')
        senha2 = request.POST.get('senha2', '')

        if senha1 != senha2:
            message = "As senhas não coincidem."
        else:
            try:
                user = User.objects.get(username=cnpj)
                user.password = make_password(senha1)
                user.save()
                cache.delete(token)  # invalida o token após uso
                return redirect('login')
            except User.DoesNotExist:
                message = "Usuário não encontrado."

    return render(request, 'cadastro/cadastrar_confirm.html', {
        'cnpj': cnpj,
        'message': message
    })
