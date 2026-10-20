# 🏭 Fábrica Inteligente: Manutenção Preditiva & Visão Computacional
**MetalTech Soluções Industriais S.A. — Protótipo Indústria 4.0**

![Status do Projeto](https://img.shields.io/badge/Status-Concluído-10b981?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.14+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-Visão_Computacional-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-API_RESTful-000000?style=for-the-badge&logo=flask&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Machine_Learning-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)

---

## 📋 Sobre o Projeto

Este repositório contém a solução completa desenvolvida para a **MetalTech Soluções Industriais S.A.**, cujo objetivo é eliminar paradas não planejadas de maquinário e falhas humanas na inspeção visual de linhas de produção. 

O ecossistema integra **Ciência de Dados**, **Machine Learning Preditivo**, **Visão Computacional (OpenCV)**, **Arquitetura MLOps** e um **Dashboard Industrial Interativo** para monitoramento em tempo real pelos operadores e Controladores Lógicos Programáveis (CLPs).

---

## 🏗️ Arquitetura e Estrutura do Repositório

```text
Machine_Learning/
│
├── ML/
│   ├── Code/
│   │   ├── Tratamento.ipynb          # Etapa 1: Limpeza de ruídos IoT, imputação e EDA
│   │   └── Machine_Leaning.ipynb     # Etapa 2: Treinamento de modelos, métricas e exportação
│   │
│   ├── Database_csv/
│   │   ├── dados_sensores_metaltech.csv  # Dataset bruto com ruídos e valores nulos (10.000 registros)
│   │   └── dados_limpos.csv              # Dataset higienizado pronto para treino
│   │
│   └── Ficheiro_IA/
│       ├── MLOP_Plan.md              # Plano completo de governança e operação de MLOps
│       └── Register_IA.joblib        # Modelo preditivo serializado
│
├── Visao_Computacional/
│   ├── assets/                       # Imagens gabarito (peças boas), amostras de teste e laudos gerados
│   ├── analise.py                    # Motor OpenCV de inspeção por subtração de gabarito
│   ├── api.py                        # Servidor Flask RESTful com endpoint /predict
│   └── parecer_tecnico.md            # Parecer técnico, cibersegurança (ISA/IEC 62443) e LGPD
│
├── Dashboard_Industrial/
│   └── index.html                    # Interface Web 4.0 (Visão Computacional + Simulador CLP)
│
├── LICENSE
└── README.md                         # Documentação geral do projeto
```

---

## 🚀 As 3 Etapas da Solução

### 1️⃣ Etapa 1: Diagnóstico e Tratamento de Dados Industriais (`Tratamento.ipynb`)
* **Problema:** Interferências eletromagnéticas nos sensores IoT geraram valores extremos (*outliers* como temperaturas de $999.9\text{ }^\circ\text{C}$ e vibrações de $-50.0\text{ mm/s}$) e perdas de pacotes (`NaN`).
* **Solução:** Pipeline com `pandas` e `seaborn` para saneamento estatístico baseado nas faixas físicas operacionais:
  * Temperatura: $50.0\text{ }^\circ\text{C} \le T \le 80.0\text{ }^\circ\text{C}$
  * Vibração: $2.0\text{ mm/s} \le V \le 5.0\text{ mm/s}$
  * Pressão: $26.0\text{ bar} \le P \le 45.0\text{ bar}$

### 2️⃣ Etapa 2: Inteligência Preditiva e Plano de MLOps (`Machine_Leaning.ipynb` & `MLOP_Plan.md`)
* **Treinamento:** Comparação entre algoritmos supervisionados utilizando `Temperatura_C`, `Vibracao_mms` e `Pressao_bar` para prever a variável alvo `Falha_motor`.
* **Avaliação:** Uso de Matriz de Confusão, Acurácia, Precisão, **Recall** e F1-Score, priorizando o Recall para impedir que quebras reais passem despercebidas.
* **Serialização:** Exportação do modelo em binário (`Register_IA.joblib`) para consumo em tempo real.
* **Governança MLOps:** Planejamento de pipeline contínuo contemplando validação com *Great Expectations*, rastreamento via *MLflow* e detecção de *Data/Concept Drift*.

### 3️⃣ Etapa 3: Visão Computacional, API RESTful e Parecer Socioético
* **Inspeção Óptica (`analise.py`):** Algoritmo de comparação diferencial (*Golden Template Matching*). Subtrai pixel a pixel a peça em teste da peça padrão íntegra, aplica filtros morfológicos e gera:
  1. **Máscara Granular (`_granulado_mascara.png`):** Mapa binário destacando exclusivamente as fissuras, ferrugens ou desgastes.
  2. **Diagnóstico em Overlay (`_analise_dano.png`):** Projeção em vermelho sobre as falhas da peça com cálculo percentual da área danificada e status (**APROVADO** / **REPROVADO**).
* **API de Chão de Fábrica (`api.py`):** Serviço em Flask expondo a rota `POST /predict` na porta `5000`.
* **Parecer Técnico e Ético (`parecer_tecnico.md`):** Estudo sobre requalificação de inspetores (*upskilling* e *Human-in-the-Loop*), blindagem de rede industrial (DMZ) e privacidade de imagem segundo a LGPD.

---

## 🛠️ Pré-requisitos e Instalação

Certifique-se de ter o **Python 3.10+** instalado. No terminal, na raiz do projeto, instale as dependências necessárias:

```bash
pip install pandas numpy scikit-learn matplotlib seaborn opencv-python flask joblib
```

---

## 💻 Como Utilizar o Projeto

### A. Executar a Inspeção por Visão Computacional via Script (`analise.py`)
1. Coloque a imagem da peça perfeita em `Visao_Computacional/assets/tampa_boa.jpg` (ou altere o nome da referência no script).
2. Coloque quantas imagens de peças com defeito desejar na pasta `Visao_Computacional/assets/` (ex.: `tampa_ruim.jpg`, `engrenagem_ruim.jpg`).
3. Execute o script:
   ```bash
   cd Visao_Computacional
   python analise.py
   ```
4. Os laudos visuais (`_granulado_mascara.png` e `_analise_dano.png`) serão gerados automaticamente na pasta `assets/` e o relatório percentual será exibido no console.

---

### B. Iniciar a API Preditiva para CLPs (`api.py`)
1. No terminal, inicie o servidor Flask:
   ```bash
   cd Visao_Computacional
   python api.py
   ```
   *O servidor ficará ativo em `http://127.0.0.1:5000`.*

2. Em outro terminal (ou via Postman / Insomnia), envie leituras de sensores para a rota `/predict`:

   **Exemplo 1 — Condição Normal de Operação:**
   ```bash
   curl -X POST http://127.0.0.1:5000/predict -H "Content-Type: application/json" -d "{\"Temperatura_C\": 65.0, \"Vibracao_mms\": 2.5, \"Pressao_bar\": 38.0}"
   ```
   **Resposta:**
   ```json
   {
     "alerta": false,
     "risco_de_falha": "Não",
     "score_falha": 0.037,
     "status_operacional": "Normal"
   }
   ```

   **Exemplo 2 — Condição Crítica (Alerta de Falha):**
   ```bash
   curl -X POST http://127.0.0.1:5000/predict -H "Content-Type: application/json" -d "{\"Temperatura_C\": 160.0, \"Vibracao_mms\": 2.0, \"Pressao_bar\": 130.0}"
   ```
   **Resposta:**
   ```json
   {
     "alerta": true,
     "risco_de_falha": "Sim",
     "score_falha": 0.5282,
     "status_operacional": "Crítico"
   }
   ```

---

### C. Utilizar o Dashboard Web Industrial (`Dashboard_Industrial/index.html`)
Para operar tudo visualmente através do navegador:

1. Abra o arquivo `Dashboard_Industrial/index.html` em qualquer navegador moderno (Chrome, Edge, Brave, Firefox).
2. **No Painel de Visão Computacional:**
   * Clique em **"Carregar Amostras Demo"** para testar instantaneamente ou envie qualquer par de imagens nos botões **1. Imagem Padrão (Boa)** e **2. Imagem em Teste (Inspecionada)** (como chapas, tampas ou engrenagens).
   * Ajuste em tempo real a **Sensibilidade (Corte)** e a **Tolerância Máxima (%)** nas barras deslizantes e clique em **"Executar Análise de Danos"**.
   * Baixe os laudos gerados clicando no botão **Baixar** no topo dos quadrantes 3 e 4.
3. **No Simulador de Telemetria Preditiva:**
   * Insira os valores de Temperatura, Vibração e Pressão (ou use os botões de cenários rápidos) e clique em **"Disparar Requisição /predict"**.
   * O painel consultará sua API Flask na porta `5000` (ou usará automaticamente o motor matemático de *fallback* integrado caso a API esteja desligada).

---

## 📄 Licença e Autoria
Projeto acadêmico e experimental desenvolvido para o **Projeto Integrador: Fábrica Inteligente MetalTech Soluções Industriais S.A.** Distribuído sob a licença constante no arquivo `LICENSE`.