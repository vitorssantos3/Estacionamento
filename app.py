import streamlit as st
import database as db

st.set_page_config(page_title="Gestao de Estacionamento", layout="centered")

db.init_db()

st.title("Sistema de Gestao de Estacionamento")

st.subheader("Registro de Entrada")

with st.form(key="form_registro_entrada"):
    placa_raw = st.text_input("Placa do veiculo:", max_chars=8).upper().strip()
    btn_submeter = st.form_submit_button("Registrar Entrada")

    if btn_submeter:
        # Remove hifen digitado para isolar os 7 caracteres
        placa_limpa = placa_raw.replace("-", "")

        if not placa_limpa:
            st.warning("Informe a placa do veiculo.")
            
        elif len(placa_limpa) != 7:
            st.error("A placa deve conter exatamente 7 caracteres.")
            
        # 1, 2 e 3 caracteres: Obrigatoriamente Letras
        elif not placa_limpa[:3].isalpha():
            st.error("Os 3 primeiros caracteres devem ser letras.")
            
        # 4 caractere: Obrigatoriamente Numero
        elif not placa_limpa[3].isdigit():
            st.error("O 4º caractere deve ser um numero.")
            
        # 5 caractere: Pode ser Letra ou Numero (Mercosul ou Tradicional)
        elif not placa_limpa[4].isalnum():
            st.error("O 5º caractere deve ser uma letra ou numero.")
            
        # 6 e 7 caracteres: Obrigatoriamente Numeros
        elif not placa_limpa[5:7].isdigit():
            st.error("Os 2 ultimos caracteres devem ser numeros.")
            
        else:
            # Formata no padrao AAA-1234 ou AAA-1D23 para salvar no banco
            placa_formatada = f"{placa_limpa[:3]}-{placa_limpa[3:]}"

            if db.verificar_placa_ja_estacionada(placa_formatada):
                st.error("Veiculo ja esta registrado no patio.")
            else:
                db.registrar_entrada_veiculo(placa_formatada)
                st.success(f"Entrada registrada para a placa: {placa_formatada}")

st.subheader("Veiculos no Patio")

dados_veiculos = db.buscar_veiculos_estacionados()

if dados_veiculos:
    lista_formatada = []
    for item in dados_veiculos:
        lista_formatada.append({
            "ID": item["id"],
            "Placa": item["placa"],
            "Entrada": item["data_entrada"],
            "Status": item["status"]
        })
    
    st.table(lista_formatada)
else:
    st.info("Nenhum veiculo no patio.")