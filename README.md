# C213 — Projeto PID — Grupo 06

Projeto 1 da disciplina de Sistemas Embarcados (C213): **Identificação de Sistemas e Controle PID**

Sistema completo para identificação automática de processos industriais (modelo FOPDT) e sintonia de controladores PID usando métodos clássicos de controle.

---

## Visão Geral

Este projeto implementa uma plataforma integrada para:

1. **Identificação de Sistemas**: Extrai parâmetros de processos industriais (ganho, constante de tempo e tempo morto) a partir de dados experimentais de resposta ao degrau
2. **Sintonia de Controladores PID**: Calcula automaticamente os ganhos (Kp, Ti, Td) usando métodos clássicos
3. **Simulação e Análise**: Valida a performance do controlador antes de aplicação em campo
4. **Dashboard Interativo**: Interface web para manipulação de dados e visualização de resultados

### Métodos Implementados

**Identificação:**
- Método de Smith
- Método de Sundaresan

**Sintonia PID:**
- Método CHR (Chien-Hrones-Reswick) sem sobresinal
- Método Cohen-Coon
- Sintonia Manual com análise de estabilidade

---

## Arquitetura

```
├── backend/                    # API e lógica de negócio
│   ├── main.py                 # Aplicação FastAPI
│   ├── requirements.txt         # Dependências Python
│   ├── api/
│   │   └── routes.py           # Endpoints da API
│   ├── controllers/
│   │   └── app_controller.py   # Camada de controle
│   ├── models/
│   │   ├── identificacao.py    # Identificação de sistemas (Smith, Sundaresan)
│   │   └── sintonia.py         # Sintonia PID (CHR, Cohen-Coon, Manual)
│   └── utils/
│       ├── data_loader.py      # Carregamento de datasets (MAT, CSV)
│       └── simulation.py       # Simulação de malha fechada
├── frontend/                   # Interface web
│   ├── index.html              # Página de login
│   ├── dashboard.html          # Dashboard principal
│   ├── css/                    # Estilos (login, dashboard)
│   └── js/                     # Scripts (api, charts, interação)
├── datasets/                   # Dados experimentais
│   └── Dataset_Grupo6_c213.mat # Dataset MATLAB com dados coletados
└── tests/                      # Suite de testes (pytest)
```

---

## Inicialização

### 1. Instalar dependências

```bash
python -m pip install -r backend/requirements.txt
```

### 2. Rodar testes

```bash
pytest -q
```

Testes incluem:
- Identificação de sistemas (Smith e Sundaresan)
- Sintonia PID (todos os métodos)
- Simulação de malha fechada
- Carregamento de datasets

### 3. Iniciar o Servidor

```bash
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8001
```

### 4. Acessar a Aplicação

Abrir navegador em: **http://127.0.0.1:8001**

---

## API REST

### Upload de Dataset

```http
POST /api/upload
Content-Type: multipart/form-data

arquivo: <arquivo.mat>
```

**Resposta:** Retorna dados do experimento (tempo, saída, entrada)

### Identificação de Sistemas

```http
POST /api/identificar
Content-Type: application/json

{
  "t": [0, 0.1, 0.2, ...],
  "y": [0, 1.2, 2.1, ...],
  "u": [0, 1, 1, ...]
}
```

**Resposta:**
```json
{
  "smith": {
    "k": 2.5,
    "tau": 5.0,
    "theta": 0.5,
    "eqm": 0.02,
    "t_modelo": [...],
    "y_modelo": [...]
  },
  "sundaresan": {...},
  "recomendado": "smith"
}
```

### Sintonia PID

```http
POST /api/sintonizar
Content-Type: application/json

{
  "k": 2.5,
  "tau": 5.0,
  "theta": 0.5,
  "metodo": "chr"
}
```

**Resposta:**
```json
{
  "Kp": 0.6,
  "Ti": 5.0,
  "Td": 0.25
}
```

### Simulação de Malha Fechada

```http
POST /api/simular
Content-Type: application/json

{
  "k": 2.5,
  "tau": 5.0,
  "theta": 0.5,
  "Kp": 0.6,
  "Ti": 5.0,
  "Td": 0.25,
  "setpoint": 1.0
}
```

**Resposta:** Dados de tempo, setpoint, saída do processo e erro

---

## Tecnologias

| Componente | Tecnologia |
|-----------|-----------|
| Backend | FastAPI, Python 3.10+ |
| Frontend | HTML5, CSS3, JavaScript |
| Processamento | NumPy, SciPy, Control |
| Testes | Pytest |
| Web Server | Uvicorn |
| Dados | MATLAB (.mat), CSV |

---

## Estrutura de Dados

### Arquivo de Dataset (MAT)

Esperado contém variáveis:
- `t`: vetor de tempo [s]
- `y`: vetor de saída do processo
- `u`: vetor de entrada (degrau aplicado)

### Modelos FOPDT Identificados

```
G(s) = k * e^(-theta*s) / (1 + tau*s)

Onde:
  k     = ganho estático
  tau   = constante de tempo [s]
  theta = tempo morto [s]
```

---

## Testes

Execute a suite completa:

```bash
pytest -v             
```

**Cobertura de testes:**
- `test_identificacao.py`: Validação dos métodos Smith e Sundaresan
- `test_sintonia.py`: Sintonia CHR, Cohen-Coon e Manual
- `test_simulation.py`: Simulação de malha fechada
- `test_dataset.py`: Carregamento e processamento de dados
- `test_app_controller.py`: Integração completa

---

## Fluxo de Uso Típico

1. **Upload de Dados**: Envie arquivo .mat ou .csv com dados experimentais
2. **Identificação**: Sistema identifica automaticamente parâmetros (k, tau, theta)
3. **Sintonia**: Selecione método (CHR/Cohen-Coon) e calcule ganhos PID
4. **Simulação**: Valide o desempenho em malha fechada antes de aplicar
5. **Visualização**: Dashboard mostra gráficos de resposta e performance

---

## Requisitos do Sistema

- Python 3.10+
- 2GB RAM mínimo
- Navegador moderno (Chrome, Firefox, Edge)
- Conexão com localhost (127.0.0.1)

---

## Grupo 06

- Projeto desenvolvido para disciplina C213 - Sistemas Embarcados
- Integrantes: Christian Salles Castilho, Maria Clara Ribeiro Ignácio, Samuel Almeida Ralise

---

