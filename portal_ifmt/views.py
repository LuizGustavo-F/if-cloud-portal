from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Maquina
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .motor_ia import MotorInferenciaOpenStack 
from .motor_preditivo import MotorPreditivo # <-- IMPORTAMOS A NOVA IA AQUI
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
import requests
import base64
import re 
from .zabbix_service import ZabbixAPI

def is_admin(user):
    return user.is_staff or user.is_superuser

def landing_page(request):
    if request.user.is_authenticated:
        return redirect('painel_maquinas')
    return render(request, 'landing.html')

def cadastrar_usuario(request):
    if request.user.is_authenticated:
        return redirect('painel_maquinas')
        
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect('painel_maquinas')
    else:
        form = UserCreationForm()
        
    return render(request, 'cadastrar.html', {'form': form})

@login_required
def pagina_inicial(request):
    minhas_maquinas = Maquina.objects.filter(dono=request.user).order_by('-data_criacao')
    
    total_vms = minhas_maquinas.count()
    vms_online = minhas_maquinas.filter(status='Online').count()
    vms_construindo = minhas_maquinas.filter(status='Construindo...').count()
    
    contexto = {
        'maquinas': minhas_maquinas,
        'total_vms': total_vms,
        'vms_online': vms_online,
        'vms_construindo': vms_construindo,
    }
    
    return render(request, 'inicio.html', contexto)

@login_required
def pagina_criacao(request):
    contexto = {} 
    if request.method == 'POST':
        aplicacao = request.POST.get('aplicacao')
        carga = request.POST.get('carga')
        
        ia = MotorInferenciaOpenStack()
        recomendacao = ia.avaliar_necessidade(aplicacao, carga)
        
        contexto['recomendacao'] = recomendacao
        contexto['aplicacao_escolhida'] = aplicacao
        contexto['carga_escolhida'] = carga

    return render(request, 'criar.html', contexto)

@login_required
def pagina_sucesso(request):
    nome_vm = request.GET.get('vm', 'sua máquina')
    return render(request, 'sucesso.html', {'nome_maquina': nome_vm})

@login_required
def processar_pedido(request):
    if request.method != 'POST':
        return redirect('/')
        
    nome_vm = request.POST.get('nome_vm', '').strip().replace(' ', '_')
    tamanho_vm = request.POST.get('tamanho_vm', 'if.small')
    chave_ssh_bruta = request.POST.get('chave_ssh', '').strip()
    
    partes = chave_ssh_bruta.split()
    if len(partes) >= 2:
        chave_ssh = f"{partes[0]} {partes[1]}"
    else:
        chave_ssh = chave_ssh_bruta

    URL_GITEA = "http://10.1.141.15:3000" 
    TOKEN = "0c814deffee69cbdf1f1e1f6801bdedc7221dc67" 
    DONO_REPO = "cti"
    NOME_REPO = "if-cloud-infra"
    CAMINHO_ARQUIVO = "terraform/servidores.auto.tfvars"
    
    url_arquivo = f"{URL_GITEA}/api/v1/repos/{DONO_REPO}/{NOME_REPO}/contents/{CAMINHO_ARQUIVO}"
    cabecalhos = {"Authorization": f"token {TOKEN}", "Accept": "application/json"}
    
    resposta_get = requests.get(url_arquivo, headers=cabecalhos)
    if resposta_get.status_code != 200:
        return render(request, 'criar.html', {'mensagem_erro': f"Erro ao acessar Gitea: {resposta_get.text}"})
        
    dados_atuais = resposta_get.json()
    conteudo_texto = base64.b64decode(dados_atuais['content']).decode('utf-8')
    
    if f'"{nome_vm}"' in conteudo_texto:
        return render(request, 'criar.html', {'mensagem_erro': f"A máquina {nome_vm} já existe na nuvem."})
        
    nova_vm = f'  "{nome_vm}" = {{\n    tamanho   = "{tamanho_vm}"\n    chave_pub = "{chave_ssh}"\n  }}'
    
    posicao_ultima_chave = conteudo_texto.rfind('}')
    novo_conteudo_texto = conteudo_texto[:posicao_ultima_chave] + f'\n{nova_vm}\n' + '}'
    novo_conteudo_base64 = base64.b64encode(novo_conteudo_texto.encode('utf-8')).decode('utf-8')
    
    dados_commit = {
        "branch": "main",
        "content": novo_conteudo_base64,
        "message": f"🤖 Portal: Construindo VM {nome_vm} com chave customizada",
        "sha": dados_atuais['sha']
    }
    
    resposta_put = requests.put(url_arquivo, headers=cabecalhos, json=dados_commit)
    
    if resposta_put.status_code == 200:
        Maquina.objects.create(
            dono=request.user,
            nome=nome_vm,
            tamanho=tamanho_vm,
            chave_ssh=chave_ssh,
            status="Construindo..."
        )
        return redirect(f'/sucesso/?vm={nome_vm}')
    else:
        return render(request, 'criar.html', {'mensagem_erro': f"Erro no Commit: {resposta_put.text}"})

@login_required
def deletar_maquina(request, nome_vm):
    if request.method != 'POST':
        return redirect('/')

    URL_GITEA = "http://10.1.141.15:3000" 
    TOKEN = "0c814deffee69cbdf1f1e1f6801bdedc7221dc67" 
    DONO_REPO = "cti"
    NOME_REPO = "if-cloud-infra"
    CAMINHO_ARQUIVO = "terraform/servidores.auto.tfvars"
    
    url_arquivo = f"{URL_GITEA}/api/v1/repos/{DONO_REPO}/{NOME_REPO}/contents/{CAMINHO_ARQUIVO}"
    cabecalhos = {"Authorization": f"token {TOKEN}", "Accept": "application/json"}
    
    resposta_get = requests.get(url_arquivo, headers=cabecalhos)
    if resposta_get.status_code != 200:
        minhas_maquinas = Maquina.objects.filter(dono=request.user).order_by('-data_criacao')
        return render(request, 'inicio.html', {'maquinas': minhas_maquinas, 'mensagem_erro': "Erro ao ler a infraestrutura atual no repositório."})
        
    dados_atuais = resposta_get.json()
    conteudo_texto = base64.b64decode(dados_atuais['content']).decode('utf-8')
    
    padrao_bloco_vm = r'\s*"' + re.escape(nome_vm) + r'"\s*=\s*\{[\s\S]*?\}'
    novo_conteudo_texto = re.sub(padrao_bloco_vm, '', conteudo_texto)
    
    novo_conteudo_base64 = base64.b64encode(novo_conteudo_texto.encode('utf-8')).decode('utf-8')
    
    dados_commit = {
        "branch": "main",
        "content": novo_conteudo_base64,
        "message": f"🗑️ Portal: Removendo código da VM {nome_vm} para destruição",
        "sha": dados_atuais['sha']
    }
    
    resposta_put = requests.put(url_arquivo, headers=cabecalhos, json=dados_commit)
    
    if resposta_put.status_code == 200:
        Maquina.objects.filter(nome=nome_vm, dono=request.user).delete()
        return redirect('/')
    else:
        minhas_maquinas = Maquina.objects.filter(dono=request.user).order_by('-data_criacao')
        return render(request, 'inicio.html', {'maquinas': minhas_maquinas, 'mensagem_erro': "Erro ao processar a remoção no servidor de automação."})

@csrf_exempt
def webhook_ansible(request):
    if request.method == 'POST':
        nome_vm = request.POST.get('nome')
        ip_vm = request.POST.get('ip')
        
        try:
            maquina = Maquina.objects.get(nome=nome_vm)
            maquina.ip_flutuante = ip_vm
            maquina.status = "Online"
            maquina.save()
            return JsonResponse({"status": "sucesso", "mensagem": f"IP da {nome_vm} updated!"})
            
        except Maquina.DoesNotExist:
            return JsonResponse({"erro": "Máquina não encontrada no banco de dados."}, status=404)
            
    return JsonResponse({"erro": "Método não permitido. Use POST."}, status=405)


@login_required
def gerenciar_maquina(request, nome_vm):
    try:
        if is_admin(request.user):
            maquina = Maquina.objects.get(nome=nome_vm)
        else:
            maquina = Maquina.objects.get(nome=nome_vm, dono=request.user)
    except Maquina.DoesNotExist:
        return redirect('/')
        
    return render(request, 'gerenciar.html', {'maquina': maquina})


@login_required
def metricas_maquina_api(request, nome_vm):
    try:
        if is_admin(request.user):
            maquina = Maquina.objects.get(nome=nome_vm)
        else:
            maquina = Maquina.objects.get(nome=nome_vm, dono=request.user)
    except Maquina.DoesNotExist:
        return JsonResponse({"erro": "Acesso negado ou máquina inexistente."}, status=403)
    
    if maquina.status != "Online":
        return JsonResponse({"cpu": 0, "ram": 0, "status": maquina.status})
    
    try:
        zabbix = ZabbixAPI()
        metricas = zabbix.get_vm_metrics_full(nome_vm)
        
        
        if "historico" in metricas:
            ia_preditiva = MotorPreditivo(limite_critico=95.0)
            
            analise_ia = ia_preditiva.avaliar_maquina(
                historico_cpu=metricas["historico"]["cpu"],
                historico_ram=metricas["historico"]["ram"]
            )
            
            metricas["inteligencia_artificial"] = analise_ia

        return JsonResponse(metricas)
    
    except Exception as e:
        return JsonResponse({"erro": f"Erro ao conectar ao monitoramento: {str(e)}"}, status=500)


@login_required
@user_passes_test(is_admin, login_url='/') 
def visao_global(request):
    """
    Painel administrativo que busca TODAS as máquinas de TODOS os usuários.
    """
    todas_maquinas = Maquina.objects.all().order_by('-data_criacao')
    
    total_vms = todas_maquinas.count()
    vms_online = todas_maquinas.filter(status='Online').count()
    
    contexto = {
        'maquinas': todas_maquinas,
        'total_vms': total_vms,
        'vms_online': vms_online,
    }
    
    return render(request, 'visao_global.html', contexto)