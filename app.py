import pandas as pd
import streamlit as st
import datetime
import pytz

# Função para carregar os dados do arquivo Excel
def carregar_checkins():
    return pd.read_excel('dados_checkin_checkout.xlsx')

# Função para atualizar um check-out no arquivo
def atualizar_checkout(checkin_atualizado):
    df = carregar_checkins()
    for index, row in df.iterrows():
        if (row['carro'] == checkin_atualizado['carro'] and
            row['usuario'] == checkin_atualizado['usuario'] and
            pd.isna(row['km_final'])):
            df.at[index, 'km_final'] = checkin_atualizado['km_final']
            df.at[index, 'data_hora_checkout'] = checkin_atualizado['data_hora_checkout']
    df.to_excel('dados_checkin_checkout.xlsx', index=False)

# Função para exibir o formulário de check-out de veículo
def exibir_formulario_checkout(usuario):
    st.title("CONTROLE DE VEÍCULOS - CHECK-OUT")
    
    df = carregar_checkins()
    checkins_abertos = df[(df['usuario'] == usuario) & (df['km_final'].isna())]

    if not checkins_abertos.empty:
        carro = st.selectbox("ESCOLHA O VEÍCULO PARA CHECK-OUT", checkins_abertos['carro'].unique())
        
        # Obter o km_inicial do veículo selecionado
        km_inicial = checkins_abertos[checkins_abertos['carro'] == carro]['km_inicial'].iloc[0]
        
        # Exibir o campo para o KM final, com um valor mínimo sendo o km_inicial
        km_final = st.number_input("KM FINAL", min_value=km_inicial, value=km_inicial)

        # Definir o fuso horário do Amazonas (UTC-4)
        fuso_amazonas = pytz.timezone('America/Manaus')
        
        # Obter a data e hora atual (horário local) ajustado para UTC-4
        data_hora_checkout = datetime.datetime.now() - datetime.timedelta(hours=4)

        if st.button("REGISTRAR CHECK-OUT"):
            # Verificar se o km_final não é menor que o km_inicial
            if km_final >= km_inicial:
                checkin_atualizado = {
                    "carro": carro,
                    "km_final": km_final,
                    "usuario": usuario,
                    "data_hora_checkout": data_hora_checkout,
                }
                atualizar_checkout(checkin_atualizado)
                st.success(f"CHECK-OUT REALIZADO COM SUCESSO PARA O CARRO {carro}!")
            else:
                st.error("O KM FINAL não pode ser menor que o KM INICIAL.")
    else:
        st.info("Nenhum check-in pendente para este usuário.")

# Função principal
def main():
    st.sidebar.title("Menu")
    usuario = st.sidebar.text_input("Digite seu nome de usuário:")

    if usuario:
        exibir_formulario_checkout(usuario)

if __name__ == "__main__":
    app()
