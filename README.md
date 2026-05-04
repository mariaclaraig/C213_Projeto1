# C213 — Projeto PID — Grupo 06
Projeto 1 da disciplina de Sistemas Embarcados (C213): Projeto de Identificação de Sistemas e Controle PID

## Como Rodar o Projeto

### Instalar dependêcias na raíz do projeto

python -m pip install -r backend/requirements.txt

### Rodar testes (tests)

pytest -q

### Iniciar servidor

python -m uvicorn backend.main:app --host 127.0.0.1 --port 8001

### Acessar no seu navegador

http://127.0.0.1:8001

