from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, FileResponse, HttpResponse
from .forms import *
from django.contrib import messages
from .consultas import *
from django.contrib.auth.decorators import login_required , user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django, logout 
from reportlab.pdfgen import canvas
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.platypus import Spacer
from django.views import View


def is_admin(user):
    return user.is_superuser


def home(request):
   
    if request.method == "POST":
        useraux = UsuarioForm(request.POST)
        
        if useraux.is_valid():
            nome = useraux.cleaned_data['nome']
            username = useraux.cleaned_data['usuario']
            emailuse = useraux.cleaned_data['email']
            senha = useraux.cleaned_data['senha']
            confsenha = useraux.cleaned_data['conf_senha']
            user = User.objects.filter(username = username ).first()

            if  user:
                messages.error(request, 'Usuário ja existe!.', extra_tags='error-message')
                return render(request, 'home/cadastro.html', {"form": useraux })
            else:
                email = User.objects.filter(email = emailuse ).first()

                if email:
                    messages.error(request, 'Email já cadastrado!.', extra_tags='error-message')
                    return render(request, 'home/cadastro.html', {"form": useraux })
                else:
                    if senha != confsenha:
                        messages.error(request, 'Senhas não coincidem.', extra_tags='error-message')
                        return render(request, 'home/cadastro.html', {"form": useraux})
                    else:
                        user2 = User.objects.create_user(username=username,email=emailuse,password=senha, first_name = nome)
                        user2.save()
                        messages.success(request, 'Cadastro realizado com sucesso! Realize Login.', extra_tags='success-message')
                        return render(request, 'home/cadastro.html', {"form": UsuarioForm})

           
       
               
    return render(request, 'home/cadastro.html', {"form": UsuarioForm})


def login(request):
    if request.method == "GET":
        return render(request, 'registration/login.html', {"form": LoginForm})
    else:
        login = LoginForm(request.POST)
        if login.is_valid():
            username = login.cleaned_data['usuario']
            senha = login.cleaned_data['senha']

            user = authenticate(username=username, password = senha)

            if user:
                login_django(request,user)
            else:
                messages.error(request, 'Usuario ou senha Invalidos.', extra_tags='error-message')
                return render(request, 'accounts/login.html', {"form": LoginForm})
        



@login_required
def inicial(request):
    message = request.GET.get('message', '')
    return render(request, 'home/inicial.html', {'message': message})



@login_required
def cadastrarMotorista(request):
    if request.method == "GET":

        return render(request, 'home/motorista/cadastrarMotorista.html', {"form": MotoristaForm})
    else:
        motaux = MotoristaForm(request.POST)
        if motaux.is_valid():
            mot = Motorista()
            mot.nome = motaux.cleaned_data['nome']
            mot.endereco =  motaux.cleaned_data['endereco']
            mot.cnh = motaux.cleaned_data['cnh']
            mot.save()
            messages.success(request, 'Cadastro salvo.', extra_tags='sucess-message')
            return redirect('cadastrarMotorista')
            
     
    return render(request, 'home/motorista/cadastrarMotorista.html', {"form": MotoristaForm})



@login_required
def cadastroManutencao(request):
    if request.method == "GET":
        return render(request ,'home/manutencao/cadastroManutencao.html', {"form": TipoManutencoesForms})
    else:
        manutAux = TipoManutencoesForms(request.POST)
        if manutAux.is_valid():
            manut = TipoManutencao()
            manut.produto = manutAux.cleaned_data['produto']
            manut.tempoTroca = manutAux.cleaned_data['tempoTroca']
            manut.kmTroca = manutAux.cleaned_data['kmTroca']
            manut.valor = manutAux.cleaned_data['valor']
            manut.save()
            messages.success(request, 'Manutenção salva.', extra_tags='sucess-message')
            return redirect('cadastroManutencao')
        else:
            messages.error(request, 'Confira os dados e tente novamente', extra_tags='error-message')
            return render(request ,'home/manutencao/cadastroManutencao.html', {"form": TipoManutencoesForms})


@login_required
def cadastroVeiculo(request):
    if request.method == "GET":
        return render(request ,'home/veiculo/cadastroVeiculo.html', {"form": VeiculoForms})
    else:
        veicAux = VeiculoForms(request.POST)
        if veicAux.is_valid():
            veiculo = Veiculo()
            veiculo.placa = veicAux.cleaned_data['placa']
            veiculo.chassi = veicAux.cleaned_data['chassi']
            veiculo.marca = veicAux.cleaned_data['marca']
            veiculo.modelo = veicAux.cleaned_data['modelo']
            veiculo.tara = veicAux.cleaned_data['tara']
            veiculo.tamanho = veicAux.cleaned_data['tamanho']
            veiculo.save()
            messages.success(request, 'Veiculo salvo.', extra_tags='sucess-message')
            return redirect('cadastroVeiculo')
        else:
            messages.error(request, 'Confira os dados e tente novamente', extra_tags='error-message')
            return render(request ,'home/manutencao/cadastroManutencao.html', {"form": VeiculoForms})
        

@login_required
def informarManutencao(request):
    if request.method == "GET":
        return render(request ,'home/manutencao/informarManutencao.html', {"form": InformarManutencaoForm})
    else:
        manutAux = InformarManutencaoForm(request.POST)
        if manutAux.is_valid():
            manut = Manutencao()
            manut.manutencao = manutAux.cleaned_data['manutencao']
            manut.veiculo = manutAux.cleaned_data['veiculo']
            manut.dataAtual = manutAux.cleaned_data['dataAtual']
            manut.kmAtual = manutAux.cleaned_data['kmAtual']
            manut.save()

            messages.success(request, 'Manutenção Salva.', extra_tags='sucess-message')
            return redirect('informarManutencao')
        else:
            messages.error(request, 'Confira os dados e tente novamente', extra_tags='error-message')
            return render(request ,'home/manutencao/informarManutencao.html', {"form": VeiculoForms})



@login_required
def informarAbastecimento(request):
    if request.method == "GET":
        return render(request ,'home/abastecimento/informarAbastecimento.html', {"form": InformarAbastecimentoForms})
    else:
        abast = InformarAbastecimentoForms(request.POST)
        if abast.is_valid():
            abastecimento = Abastecimentos()
            abastecimento.veiculo = abast.cleaned_data['veiculo']
            abastecimento.data = abast.cleaned_data['data']
            abastecimento.litros = abast.cleaned_data['litros']
            abastecimento.kmatual = abast.cleaned_data['kmatual']
            abastecimento.save()

            messages.success(request, 'Abatecimento Salvo.', extra_tags='sucess-message')
            return redirect('informarAbastecimento')
        else:
            messages.error(request, 'Confira os dados e tente novamente', extra_tags='error-message')
            return render(request ,'home/abastecimento/informarAbastecimento.html', {"form": InformarAbastecimentoForms})

@login_required
def gerarRelatorio(request):
    if request.method == "GET":
        veic = RelatorioForms(request.GET)
        if veic.is_valid():
            placa = veic.cleaned_data['veiculo']
            veiculo = Veiculo.objects.get(placa=placa)
            dados_de_abastecimentos = Abastecimentos.objects.filter(veiculo=veiculo)
            dados_de_manutencao = Manutencao.objects.filter(veiculo=veiculo)

            response = FileResponse(generate_abastecimentos_pdf(dados_de_abastecimentos,dados_de_manutencao))
            response['Content-Type'] = 'application/pdf'
            response['Content-Disposition'] = 'inline; filename="relatorio_abastecimentos.pdf"'
            return response
    return render(request ,'home/relatorios/gerarRelatorio.html', {"form" : RelatorioForms})





@login_required
@user_passes_test(is_admin, login_url='/inicial/?message=PAGINA SOLICITADA SO PODE SER ACESSADA POR ADMIN.' ) # teste para saber se é administrador 
def acessarVeiculo(request):
    veiculos = Veiculo.objects.all()
    return render(request ,'home/veiculo/acessarVeiculo.html',{"veiculos":veiculos})


def relatorioVeiculo(request):
    veiculo = Veiculo.objects.get()
    dados_de_abastecimentos = Abastecimentos.objects.filter(veiculo=veiculo)
    dados_de_manutencao = Manutencao.objects.filter(veiculo=veiculo)

    response = HttpResponse(generate_abastecimentos_pdf(dados_de_abastecimentos, dados_de_manutencao), content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="relatorio_abastecimentos.pdf"'
    return response


def generate_abastecimentos_pdf(dados_de_abastecimentos, dados_de_manutencao):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)

    elements = []
    title1 = Table([['ABASTECIMENTOS']])
    title2 = Table([['MANUTENÇÕES']])
    # Adicione os dados à tabela
    abast = [['Veículo', 'Data', 'Litros', 'KM Atual', 'Media Calculada']]
    for abastecimento in dados_de_abastecimentos:
        abast.append([abastecimento.veiculo, abastecimento.data, abastecimento.litros, abastecimento.kmatual, abastecimento.mediaVeiculo])
    # Crie a tabela
        table = Table(abast)

    # Crie a tabela
    table = Table(abast)


    manut = [['Veículo', 'Data', 'Data Proxima', 'Km Manutenção', 'KM Proxima ']]
    for manutencao in dados_de_manutencao:
        manut.append([manutencao.veiculo, manutencao.dataAtual, manutencao.dataProximaMan, manutencao.kmAtual, manutencao.kmProximaMan ])

    table2 = Table(manut)

    # Estilize a tabela
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    table.setStyle(style)
    table2.setStyle(style)
    title1.setStyle(style)
    title2.setStyle(style)
    elements.append(Spacer(1, 12))
    elements.append(title1)
    elements.append(table)
    elements.append(Spacer(1, 12))
    elements.append(title2)
    elements.append(table2)
    doc.build(elements)

    buffer.seek(0)
    return buffer



# EDITAR MOTORISTAS
@login_required
@user_passes_test(is_admin, login_url='/inicial/?message=PAGINA SOLICITADA SO PODE SER ACESSADA POR ADMIN.' ) # teste para saber se é administrador 
def visualizarMotoristas(request):
    motoristas = Motorista.objects.all().order_by('nome')
    return render(request, "home/motorista/visualizarMotorista.html", {"motoristas":motoristas} )


@login_required
@user_passes_test(is_admin, login_url='/inicial/?message=PAGINA SOLICITADA SO PODE SER ACESSADA POR ADMIN.' ) # teste para saber se é administrador 
def editarMotorista(request, id):
    motorista = Motorista.objects.get(id=id)
    form = MotoristaFormCustom(motorista)
    return render(request, "home/motorista/editarMotorista.html", {"form":form,"motorista": motorista} )


@login_required
@user_passes_test(is_admin, login_url='/inicial/?message=PAGINA SOLICITADA SO PODE SER ACESSADA POR ADMIN.' ) # teste para saber se é administrador 
def buscar_motoristas(request):
    nome = request.GET.get('nome')
    if nome:
        motoristas = Motorista.objects.filter(nome__icontains=nome)
        if not motoristas:
            messages.error(request, 'NAO ENCONTRADO NENHUM VALOR', extra_tags='error-message')
            motoristas = Motorista.objects.all()
    else:
        messages.error(request, 'DIGITE ALGUM VALOR', extra_tags='error-message')
        motoristas = Motorista.objects.all()
    return render(request, 'home/motorista/visualizarMotorista.html', {'motoristas': motoristas})

@login_required
@user_passes_test(is_admin, login_url='/inicial/?message=PAGINA SOLICITADA SO PODE SER ACESSADA POR ADMIN.' ) # teste para saber se é administrador 
def updateMotorista(request, id):
    motorista = Motorista.objects.get(id=id)
    if request.method == "POST":
        novoNome = request.POST.get("nome")
        novoEndereco = request.POST.get("endereco")
        novaCnh = request.POST.get("cnh")
        motorista.nome = novoNome
        motorista.endereco = novoEndereco
        motorista.cnh = novaCnh
        motorista.save()

    messages.success(request, 'Salvo.', extra_tags='sucess-message')
    return redirect('visualizarMotoristas')


# EDITAR VEICULOS
@user_passes_test(is_admin, login_url='/inicial/?message=PAGINA SOLICITADA SO PODE SER ACESSADA POR ADMIN.' ) # teste para saber se é administrador 
def visualizarVeiculo(request):
    veiculos = Veiculo.objects.all()
    return render(request, 'home/veiculo/visualizarVeiculo.html', {"veiculos":veiculos} )


@login_required
@user_passes_test(is_admin, login_url='/inicial/?message=PAGINA SOLICITADA SO PODE SER ACESSADA POR ADMIN.' ) # teste para saber se é administrador 
def editarVeiculo(request, id):
    veiculo = Veiculo.objects.get(id=id)
    form = VeiculoFormCustom(veiculo)
    return render(request, "home/veiculo/editarVeiculo.html", {"form":form,"veiculo": veiculo} )


@login_required
@user_passes_test(is_admin, login_url='/inicial/?message=PAGINA SOLICITADA SO PODE SER ACESSADA POR ADMIN.' ) # teste para saber se é administrador 
def buscarVeiculo(request):
    placa = request.GET.get('placa')
    if placa:
        veiculos = Veiculo.objects.filter(placa__icontains=placa)
        if not veiculos:
            messages.error(request, 'NAO ENCONTRADO NENHUM VEICULO', extra_tags='error-message')
            veiculos = Veiculo.objects.all()
    else:
        messages.error(request, 'DIGITE ALGUM VALOR', extra_tags='error-message')
        veiculos = Veiculo.objects.all()
    return render(request, 'home/veiculo/visualizarVeiculo.html', {'veiculos': veiculos})

@login_required
@user_passes_test(is_admin, login_url='/inicial/?message=PAGINA SOLICITADA SO PODE SER ACESSADA POR ADMIN.' ) # teste para saber se é administrador 
def updateVeiculo(request, id):
    veiculo = Veiculo.objects.get(id=id)
    if request.method == "POST":
        veiculo.placa = request.POST.get("placa")
        veiculo.chassi = request.POST.get("chassi")
        veiculo.marca = request.POST.get("marca")
        veiculo.modelo = request.POST.get("modelo")
        veiculo.tara = request.POST.get("tara")
        veiculo.tamanho = request.POST.get("tamanho")
        veiculo.save()

    messages.success(request, 'Salvo.', extra_tags='sucess-message')
    return redirect('visualizarVeiculo')




# EDITAR TIPO MENUTENÇÃO
@user_passes_test(is_admin, login_url='/inicial/?message=PAGINA SOLICITADA SO PODE SER ACESSADA POR ADMIN.' ) # teste para saber se é administrador 
def visualizarTipoManutencao(request):
    manutencoes = TipoManutencao.objects.all().order_by('produto')
    return render(request, 'home/manutencao/visualizarTipoManutencao.html', {"manutencoes":manutencoes} )


@login_required
@user_passes_test(is_admin, login_url='/inicial/?message=PAGINA SOLICITADA SO PODE SER ACESSADA POR ADMIN.' ) # teste para saber se é administrador 
def editarTipoManutencao(request, id):
    manutencao = TipoManutencao.objects.get(id=id)
    form = ManutencaoFormCustom(manutencao)
    return render(request, "home/manutencao/editarTipoManutencao.html", {"form":form,"manutencao": manutencao} )


@login_required
@user_passes_test(is_admin, login_url='/inicial/?message=PAGINA SOLICITADA SO PODE SER ACESSADA POR ADMIN.' ) # teste para saber se é administrador 
def buscarTipoManutencao(request):
    nome = request.GET.get('nome')
    if nome:
        manutencoes = TipoManutencao.objects.filter(produto__icontains=nome)
        if not manutencoes:
            messages.error(request, 'NAO ENCONTRADO NENHUMA MANUTENÇÃO', extra_tags='error-message')
            manutencoes = TipoManutencao.objects.all()
    else:
        messages.error(request, 'DIGITE ALGUM VALOR', extra_tags='error-message')
        manutencoes = TipoManutencao.objects.all()
    return render(request, 'home/manutencao/visualizarTipoManutencao.html', {'manutencoes': manutencoes})

@login_required
@user_passes_test(is_admin, login_url='/inicial/?message=PAGINA SOLICITADA SO PODE SER ACESSADA POR ADMIN.' ) # teste para saber se é administrador 
def updateTipoManutencao(request, id):
    manutencao = TipoManutencao.objects.get(id=id)
    if request.method == "POST":
        manutencao.produto = request.POST.get("produto")
        manutencao.tempoTroca = request.POST.get("tempoTroca")
        manutencao.kmTroca = request.POST.get("kmTroca")
        manutencao.valor = request.POST.get("valor")
        manutencao.save()

    messages.success(request, 'Salvo.', extra_tags='sucess-message')
    return redirect('visualizarTipoManutencao')


# EDITAR ABASTECIMENTO
@user_passes_test(is_admin, login_url='/inicial/?message=PAGINA SOLICITADA SO PODE SER ACESSADA POR ADMIN.' ) # teste para saber se é administrador 
def visualizarAbastecimento(request):
    abastecimentos = Abastecimentos.objects.all().order_by('veiculo','data')
    return render(request, 'home/abastecimento/visualizarAbastecimento.html', {"abastecimentos":abastecimentos} )


@login_required
@user_passes_test(is_admin, login_url='/inicial/?message=PAGINA SOLICITADA SO PODE SER ACESSADA POR ADMIN.' ) # teste para saber se é administrador 
def editarAbastecimento(request, id):
    abastecimento = Abastecimentos.objects.get(id=id)
    form = AbastecimentoFormCustom(abastecimento)
    datafor = abastecimento.data.strftime('%Y-%m-%d')
    return render(request, "home/abastecimento/editarAbastecimento.html", {"form":form,"abastecimento": abastecimento, "datafor":datafor} )


@login_required
@user_passes_test(is_admin, login_url='/inicial/?message=PAGINA SOLICITADA SO PODE SER ACESSADA POR ADMIN.' ) # teste para saber se é administrador 
def buscarAbastecimento(request):
    veiculo = request.GET.get('placa')
    if veiculo:
        abastecimentos = Abastecimentos.objects.filter(veiculo__placa__icontains=veiculo)
        if not abastecimentos:
            messages.error(request, 'NAO ENCONTRADO NENHUM VEICULO', extra_tags='error-message')
            abastecimentos = Abastecimentos.objects.all()
    else:
        messages.error(request, 'DIGITE ALGUM VALOR', extra_tags='error-message')
        abastecimentos = Abastecimentos.objects.all()
    return render(request, 'home/abastecimento/visualizarAbastecimento.html', {'abastecimentos': abastecimentos})

@login_required
@user_passes_test(is_admin, login_url='/inicial/?message=PAGINA SOLICITADA SO PODE SER ACESSADA POR ADMIN.' ) # teste para saber se é administrador 
def updateAbastecimento(request, id):
    abastecimentoaux = Abastecimentos.objects.get(id=id)
    if request.method == "POST":
        abast = InformarAbastecimentoForms(request.POST)
        if abast.is_valid():
            abastecimento = Abastecimentos()
            abastecimento.veiculo = abast.cleaned_data['veiculo']
            abastecimento.data = abast.cleaned_data['data']
            abastecimento.litros = abast.cleaned_data['litros']
            abastecimento.kmatual = abast.cleaned_data['kmatual']
            abastecimentoaux.delete()
            abastecimento.save()
            

    messages.success(request, 'Salvo.', extra_tags='sucess-message')
    return redirect('visualizarAbastecimento')


# EDITAR MANUTENÇÃO ADICIONADA
@user_passes_test(is_admin, login_url='/inicial/?message=PAGINA SOLICITADA SO PODE SER ACESSADA POR ADMIN.' ) # teste para saber se é administrador 
def visualizarManutencao(request):
    manutencoes = Manutencao.objects.all().order_by('veiculo','dataAtual')
    return render(request, 'home/manutencao/visualizarManutencao.html', {"manutencoes":manutencoes} )


@login_required
@user_passes_test(is_admin, login_url='/inicial/?message=PAGINA SOLICITADA SO PODE SER ACESSADA POR ADMIN.' ) # teste para saber se é administrador 
def editarManutencao(request, id):
    manutencao = Manutencao.objects.get(id=id)
    form = InformarManutencaoFormCustom(manutencao)
    datafor = manutencao.dataAtual.strftime('%Y-%m-%d')
    return render(request, "home/manutencao/editarManutencao.html", {"form":form,"manutencao": manutencao, "datafor":datafor} )


@login_required
@user_passes_test(is_admin, login_url='/inicial/?message=PAGINA SOLICITADA SO PODE SER ACESSADA POR ADMIN.' ) # teste para saber se é administrador 
def buscarManutencao(request):
    veiculo = request.GET.get('placa')
    if veiculo:
        manutencoes = Manutencao.objects.filter(veiculo__placa__icontains=veiculo)
        if not manutencoes:
            messages.error(request, 'NAO ENCONTRADO NENHUM VEICULO', extra_tags='error-message')
            manutencoes = Manutencao.objects.all()
    else:
        messages.error(request, 'DIGITE ALGUM VALOR', extra_tags='error-message')
        manutencoes = Manutencao.objects.all()
    return render(request, 'home/manutencao/visualizarManutencao.html', {'manutencoes': manutencoes})

@login_required
@user_passes_test(is_admin, login_url='/inicial/?message=PAGINA SOLICITADA SO PODE SER ACESSADA POR ADMIN.' ) # teste para saber se é administrador 
def updateManutencao(request, id):
    manutencaoaux = Manutencao.objects.get(id=id)
    if request.method == "POST":
        manutAux = InformarManutencaoForm(request.POST)
        manutencaonova = Manutencao()
        manutencaoaux.delete()
        if manutAux.is_valid():
            manutencaonova.veiculo = manutAux.cleaned_data['veiculo']
            manutencaonova.manutencao = manutAux.cleaned_data['manutencao']
            manutencaonova.dataAtual = manutAux.cleaned_data['dataAtual']
            manutencaonova.kmAtual = manutAux.cleaned_data['kmAtual']
            manutencaonova.save()
                

    messages.success(request, 'Salvo.', extra_tags='sucess-message')
    return redirect('visualizarManutencao')


class GeneratePDF(View):
    def get(self, request, *args, **kwargs):
        # Crie um objeto PDF
        response = HttpResponse(content_type='application/pdf')

        # Use o ReportLab para gerar o conteúdo do PDF
        p = canvas.Canvas(response)
        p.drawString(100, 100, "Hello world.")
        p.showPage()
        p.save()

        return response
    
def teste(request):
    return render(request,'home/teste.html')