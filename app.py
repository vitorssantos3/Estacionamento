import streamlit as st
import database as db
from datetime import datetime
import math

st.set_page_config(page_title="Gestao de Estacionamento", layout="centered")

db.init_db()

st.title("Sistema de Gestao de Estacionamento")

tab_entrada, tab_consulta = st.tabs(["Registrar Entrada", "Consulta de Permanencia"])

# ==========================================
# ABA 1: REGISTRO DE ENTRADA
# ==========================================
with tab_entrada:
    st.subheader("Registro de Entrada")

    if "mensagem_sucesso" in st.session_state:
        st.success(st.session_state["mensagem_sucesso"])
        del st.session_state["mensagem_sucesso"]

    with st.form(key="form_registro_entrada", clear_on_submit=True):
        placa_raw = st.text_input("Placa do veiculo:", max_chars=8).upper().strip()
        btn_submeter = st.form_submit_button("Registrar Entrada")

        if btn_submeter:
            placa_limpa = placa_raw.replace("-", "")

            if not placa_limpa:
                st.warning("Informe a placa do veiculo.")
                
            elif len(placa_limpa) != 7:
                st.error("A placa deve conter exatamente 7 caracteres.")
                
            elif not placa_limpa[:3].isalpha():
                st.error("Os 3 primeiros caracteres devem ser letras.")
                
            elif not placa_limpa[3].isdigit():
                st.error("O 4º caractere deve ser um numero.")
                
            elif not placa_limpa[4].isalnum():
                st.error("O 5º caractere deve ser uma letra ou numero.")
                
            elif not placa_limpa[5:7].isdigit():
                st.error("Os 2 ultimos caracteres devem ser numeros.")
                
            else:
                placa_formatada = f"{placa_limpa[:3]}-{placa_limpa[3:]}"

                if db.verificar_placa_ja_estacionada(placa_formatada):
                    st.error("Veiculo ja esta registrado no patio.")
                else:
                    db.registrar_entrada_veiculo(placa_formatada)
                    st.session_state["mensagem_sucesso"] = f"Entrada registrada para a placa: {placa_formatada}"
                    st.rerun()

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

# ==========================================
# ABA 2: CONSULTA DE PERMANENCIA
# ==========================================
with tab_consulta:
    st.subheader("Consultar Tempo de Permanencia e Valor")
    
    placa_consulta_raw = st.text_input("Digite a placa para consultar:", max_chars=8, key="input_consulta").upper().strip()
    btn_consultar = st.button("Consultar Veiculo")

    if btn_consultar or placa_consulta_raw:
        placa_limpa = placa_consulta_raw.replace("-", "")
        if len(placa_limpa) == 7:
            placa_formatada = f"{placa_limpa[:3]}-{placa_limpa[3:]}"
            veiculo = db.buscar_veiculo_por_placa(placa_formatada)

            if veiculo:
                # Calculo do tempo decorrido
                data_entrada = datetime.strptime(veiculo["data_entrada"], "%Y-%m-%d %H:%M:%S")
                agora = datetime.now()
                diferenca = agora - data_entrada

                total_segundos = int(diferenca.total_seconds())
                total_minutos = total_segundos // 60
                horas = total_segundos // 3600
                minutos = (total_segundos % 3600) // 60

                # Regra de Tarifa Atualizada:
                # 0 a 15 min: Grátis (Tolerância)
                # 16 a 30 min: R$ 5,00
                # 31 a 60 min: R$ 10,00
                # > 60 min: R$ 10,00 + R$ 2,00 por hora extra (ou fração)
                if total_minutos <= 15:
                    valor_estimado = 0.0
                elif total_minutos <= 30:
                    valor_estimado = 5.0
                elif total_minutos <= 60:
                    valor_estimado = 10.0
                else:
                    TARIFA_PRIMEIRA_HORA = 10.0
                    TARIFA_HORA_ADICIONAL = 2.0
                    horas_totais_cobrada = math.ceil(total_segundos / 3600)
                    horas_adicionais = horas_totais_cobrada - 1
                    valor_estimado = TARIFA_PRIMEIRA_HORA + (horas_adicionais * TARIFA_HORA_ADICIONAL)

                st.success(f"Veiculo localizado no patio. Status: {veiculo['status']}")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Tempo Estacionado", f"{horas}h {minutos}min")
                    st.caption(f"Entrada registrada em: {veiculo['data_entrada']}")
                with col2:
                    st.metric("Valor Acumulado (Parcial)", f"R$ {valor_estimado:.2f}")
                    st.caption("Tarifa: até 15min Grátis | 30min R$ 5 | 1h R$ 10 | +R$ 2/h extra")

            else:
                st.error("Veiculo nao localizado no patio ou ja finalizado.")
        elif placa_consulta_raw:
            st.warning("A placa informada deve ter 7 caracteres.")