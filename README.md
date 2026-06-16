#  IF Cloud - Portal de Gestão de Nuvem com Inteligência Artificial

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Django](https://img.shields.io/badge/Django-092E20?style=flat&logo=django&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat&logo=scikit-learn&logoColor=white)
![OpenStack](https://img.shields.io/badge/OpenStack-ED1944?style=flat&logo=OpenStack&logoColor=white)
![Zabbix](https://img.shields.io/badge/Zabbix-D40000?style=flat&logo=Zabbix&logoColor=white)

Este projeto é um portal de provisionamento e monitoramento de infraestrutura em nuvem, desenvolvido para o ambiente acadêmico do Instituto Federal de Mato Grosso (IFMT). O sistema atua como uma camada de abstração sobre o OpenStack (MicroStack), permitindo que alunos e professores criem e gerenciem Máquinas Virtuais (VMs) de forma simplificada e inteligente.

O grande diferencial do IF Cloud é a sua **Arquitetura Híbrida de Inteligência Artificial**, que atua tanto na recomendação de hardware na criação da VM, quanto na prevenção de falhas durante a sua operação.

---

## Arquitetura de Inteligência Artificial

O sistema é sustentado por dois motores distintos, cobrindo os paradigmas clássicos da disciplina de Sistemas Inteligentes:

### 1. Tutor de Infraestrutura (IA Simbólica / GOFAI)

Um Sistema Especialista Baseado em Regras (*Rule-Based Expert System*) que atua como um arquiteto de nuvem virtual.

* **Paradigma:** Determinístico (Lógica Proposicional).
* **Mecanismo:** Utiliza Encadeamento para Frente (*Forward Chaining*) em uma Árvore de Decisão para cruzar a aplicação desejada pelo usuário com a carga estimada.
* **Explainable AI (XAI):** O motor não apenas recomenda o hardware ideal (ex: `if.small`, `if.medium`, `if.large`), mas gera uma justificativa semântica explicando ao aluno o motivo arquitetural daquela escolha, evitando o desperdício de recursos do cluster.

### 2. Motor Preditivo de Gargalos (IA Estatística / Machine Learning)

Um algoritmo de monitoramento contínuo que consome a telemetria via API do Zabbix para prever o esgotamento de recursos (CPU e RAM).

* **Algoritmo:** Regressão Linear Simples (`y = mx + b`) aplicada a Séries Temporais.
* **Mecanismo:** O motor calcula o coeficiente angular (`m`) do histórico de consumo. Sendo uma tendência de alta contínua, a equação é invertida para prever em **quantos minutos** o servidor atingirá o limite crítico (95%), alertando os administradores antes que a queda ocorra.
* **Métricas Oficiais de Validação (Dataset de Estresse):**
  *  **Acurácia:** 95.0%
  *  **Precisão:** 87.5% (Baixo índice de falsos alarmes)
  *  **Recall (Sensibilidade):** 100.0% (Zero falhas silenciosas omitidas)

---

## Tecnologias Utilizadas

* **Backend:** Python, Django
* **Frontend:** HTML5, CSS3 (Custom Dark Theme), Jinja/Django Templates
* **Infraestrutura e Virtualização:** OpenStack (MicroStack)
* **Monitoramento:** Zabbix API
* **Data Science & IA:** `scikit-learn`, `matplotlib`, `csv` (para validação do modelo preditivo)

---

## Como Executar o Projeto Localmente

### 1. Clone o repositório

```bash
git clone https://github.com/SEU_USUARIO/NOME_DO_REPO.git
cd NOME_DO_REPO
```

### 2. Crie e ative o ambiente virtual

```bash
python -m venv venv

# No Windows
venv\Scripts\activate

# No Linux/Mac
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install django requests scikit-learn matplotlib
```

### 4. Execute as migrações do banco de dados

```bash
python manage.py migrate
```

### 5. Inicie o servidor Django

```bash
python manage.py runserver
```

O portal estará disponível em:

```text
http://127.0.0.1:8000/
```

---

## Como Rodar a Avaliação da IA (Métricas)

Para conferir a eficácia matemática do Motor Preditivo, execute o script isolado de avaliação que utiliza o dataset simulado do Zabbix:

```bash
cd portal_ifmt
python avaliar_ia.py
```

---

## Objetivo Acadêmico

O IF Cloud foi desenvolvido com o objetivo de integrar conceitos de:

* Computação em Nuvem
* Virtualização
* Monitoramento de Infraestrutura
* Sistemas Inteligentes
* Machine Learning
* Sistemas Especialistas
* Explainable AI (XAI)
* Desenvolvimento Web com Django

O projeto demonstra a aplicação prática de Inteligência Artificial na gestão de ambientes de nuvem privada, auxiliando usuários na tomada de decisão e permitindo a antecipação de problemas operacionais por meio de análise preditiva.
