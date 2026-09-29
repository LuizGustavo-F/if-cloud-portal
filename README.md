# IF Cloud - Portal de Autosserviço e Gestão de Nuvem Privada

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Django](https://img.shields.io/badge/Django-092E20?style=flat&logo=django&logoColor=white)
![OpenStack](https://img.shields.io/badge/OpenStack-ED1944?style=flat&logo=OpenStack&logoColor=white)
![Terraform](https://img.shields.io/badge/Terraform-7B42BC?style=flat&logo=terraform&logoColor=white)
![Ansible](https://img.shields.io/badge/Ansible-EE0000?style=flat&logo=ansible&logoColor=white)
![Zabbix](https://img.shields.io/badge/Zabbix-D40000?style=flat&logo=Zabbix&logoColor=white)

Este projeto é o portal de interface de usuário (frontend/backend) do ecossistema **IF Cloud**, uma infraestrutura de nuvem privada (IaaS) desenvolvida para a Coordenação de Tecnologia da Informação (CTI) do Instituto Federal de Mato Grosso (IFMT).

O portal atua como a principal camada de abstração do projeto, permitindo que alunos e professores solicitem, provisionem e gerenciem Máquinas Virtuais (VMs) de forma autônoma, sem precisarem interagir diretamente com a complexidade do OpenStack (MicroStack) ou com as esteiras de Infraestrutura como Código.

## 🚀 Principais Funcionalidades

* **Autosserviço de Instâncias:** Interface simplificada para criação de VMs padronizadas (*flavors* como `if.small`, `if.medium`) alinhadas aos recursos físicos legados do laboratório.
* **Integração GitOps & IaC:** O portal atua como o gatilho amigável para as automações de provisionamento infraestrutural (Terraform) e gerência de configuração (Ansible) executadas nos bastidores.
* **Acesso Direto (Provider Network):** Gestão simplificada para que as instâncias recebam IPs diretamente da sub-rede física da instituição, eliminando a necessidade de roteamento NAT complexo pelo usuário final.
* **Observabilidade Unificada:** Integração visual baseada na telemetria coletada pelo Zabbix e estruturada via Grafana para acompanhamento do consumo de recursos.
* **Assistência Inteligente (Módulo IA):** Sistema de suporte embarcado que cruza a aplicação desejada pelo usuário com a carga estimada para recomendar o hardware ideal (evitando desperdício no cluster), aliado a um algoritmo preditivo que consome dados da API do Zabbix para alertar sobre o esgotamento iminente de recursos na nuvem.

## 🛠️ Tecnologias e Arquitetura

O portal foi construído para atuar como o maestro da stack de nuvem privada:

* **Backend:** Python e Django (gestão de requisições, regras de negócio e integração via APIs).
* **Frontend:** HTML5, CSS3 (Custom Dark Theme) e Django Templates.
* **Orquestração Subjacente:** OpenStack (distribuição MicroStack).
* **Automação (Integrações):** Chamadas e engatilhos para Gitea, Terraform e Ansible.
* **Monitoramento e Inteligência:** Integração com a API do Zabbix, utilizando `scikit-learn` para os modelos preditivos de saturação de infraestrutura.

## ⚙️ Como Executar o Projeto Localmente

### 1. Clone o repositório
```bash
git clone [https://github.com/SEU_USUARIO/NOME_DO_REPO.git](https://github.com/SEU_USUARIO/NOME_DO_REPO.git)
cd NOME_DO_REPO
````
### 2. Crie e ative o ambiente virtual
```
python -m venv venv
```
# No Windows
```
venv\Scripts\activate
```
# No Linux/Mac
```
source venv/bin/activate
```
### 3. Instale as dependências
```
pip install -r requirements.txt
```
### 4. Execute as migrações do banco de dados
```
python manage.py migrate
```
### 5. Inicie o serviço Django
```
python manage.py runserver
```
# O portal será acessado em: ```http://127.0.0.1:8000/```

## Este repositório é parte integrante do projeto IF cloud, desenvolvido no IFMT Octayde Jorge da Silva. A equipe CTI, busca projetar uma plataforma de provisionamento autônoma, para realizar testes internos e possível uso de alunos em laboratório.
