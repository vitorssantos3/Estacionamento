# Sistema de Gestao de Estacionamento

Projeto desenvolvido para as Atividades Continuas (ACs) da faculdade, utilizando Python, Streamlit e SQLite.

## Estrutura do Projeto

- `app.py`: Interface grafica desenvolvida em Streamlit (Front-end).
- `database.py`: Camada de persistencia de dados com SQLite (Back-end).
- `estacionamento.db`: Banco de dados local gerado automaticamente.

## Funcionalidades Implementadas

### AC1
- Cadastro de entrada de veiculos com validacao rigida de placa (padroes Tradicional e Mercosul).
- Listagem em tempo real dos veiculos estacionados no patio.
- Persistencia dos dados em banco SQLite.

### AC2
- Interface em abas (`st.tabs`) para separacao de modulos.
- Aba de consulta de permanencia por placa.
- Calculo dinamico do tempo estacionado (horas e minutos).
- Calculo de tarifacao parcial:
  - Ate 15 minutos: Gratis (Tolerancia)
  - De 16 a 30 minutos: R$ 5,00
  - De 31 a 60 minutos: R$ 10,00
  - Acima de 60 minutos: R$ 10,00 + R$ 2,00 por hora extra (ou fracao)

## Como Executar o Projeto

1. Instale as dependencias:
   ```bash
   pip install streamlit

2. Rode o sistema:
   ```bash
    streamlit run app.py
