import streamlit as st
import pandas as pd
import datetime
import pytz

# Função para verificar o login
def verificar_login(usuario, senha):
    usuarios_validos = {
        'COORDENAÇÃO': '67321', 'TÉC. LUIZ ANDRÉ': '12345', 'TÉC. RAFAEL PORTO': '12345', 'TÉC. ANDERSON ALVES': '12345',
        'TÉC. AILSON SILVA': '12345', 'ENG. PAULO VICTOR': '12345', 'ENG. JOSÉ UILIAN': '12345', 'ENG. LUIZ NEVES': '12345',
        'ADM. VÍTALLO RAONY': '12345', 'TÉC. EVELYN FERNANDEZ': '12345', 'COORD. GENILSON MEDEIROS': '12345', 'TÉC. MARCELO BRITO': '12345',
        'ENG. ALTEMAR JÚNIOR': '12345', 'ENG. LUAN DEMARCO': '12345', 'TÉC. JOSÉ BRAZ': '12345'
    }
    
    return usuario in usuarios_validos and usuarios_validos[usuario] == senha

# Função para carregar check-ins do arquivo
def carregar_checkins():
    try:
        df = pd.read_excel('dados_checkin_checkout.xlsx')
    except FileNotFoundError:
        df = pd.DataFrame(columns=['carro', 'km_inicial', 'km_final', 'origem', 'destino', 'usuario', 
                                   'data_hora_checkin', 'data_hora_checkout', 'litros_abastecidos', 
                                   'valor_nota', 'preco_por_litro'])
    return df

# Função para salvar check-in no arquivo
def salvar_checkin(checkin):
    df = carregar_checkins()
    df = pd.concat([df, pd.DataFrame([checkin])], ignore_index=True)
    df.to_excel('dados_checkin_checkout.xlsx', index=False)

# Função para atualizar um check-out no arquivo
def atualizar_checkout(checkin_atualizado):
    df = carregar_checkins()
    for index, row in df.iterrows():
        if (row['carro'] == checkin_atualizado['carro'] and
            row['usuario'] == checkin_atualizado['usuario'] and
            pd.isna(row['km_final'])):
            df.at[index, 'km_final'] = checkin_atualizado['km_final']
            df.at[index, 'data_hora_checkout'] = checkin_atualizado['data_hora_checkout']
            df.at[index, 'litros_abastecidos'] = checkin_atualizado['litros_abastecidos']
            df.at[index, 'valor_nota'] = checkin_atualizado['valor_nota']
            df.at[index, 'preco_por_litro'] = checkin_atualizado['preco_por_litro']
            
    df.to_excel('dados_checkin_checkout.xlsx', index=False)

# Função para exibir o formulário de check-out de veículo
def exibir_formulario_checkout(usuario):
    st.title("CONTROLE DE VEÍCULOS - CHECK-OUT")

    df = carregar_checkins()
    checkins_abertos = df[(df['usuario'] == usuario) & (df['km_final'].isna())]

    if not checkins_abertos.empty:
        checkin_selecionado = st.selectbox("Escolha o Check-in em Aberto", checkins_abertos.index, format_func=lambda idx: f"{checkins_abertos.loc[idx, 'carro']} - {checkins_abertos.loc[idx, 'origem']} para {checkins_abertos.loc[idx, 'destino']}")
        km_final = st.number_input("KM FINAL", min_value=0)

        # Adicionar campos para registro de abastecimento
        st.subheader("REGISTRO DE ABASTECIMENTO (Opcional)")
        abasteceu = st.radio("HOUVE ABASTECIMENTO DURANTE A VIAGEM?", ("Não", "Sim"))

        if abasteceu == "Sim":
            litros_abastecidos = st.number_input("QUANTIDADE DE LITROS ABASTECIDOS", min_value=0.0, step=0.1, format="%.2f")
            valor_nota = st.number_input("VALOR TOTAL DA NOTA (R$)", min_value=0.0, step=0.1, format="%.2f")

            if litros_abastecidos > 0 and valor_nota > 0:
                preco_por_litro = valor_nota / litros_abastecidos
                st.write(f"PREÇO POR LITRO: R$ {preco_por_litro:.2f}")
            else:
                preco_por_litro = None
                st.warning("INSIRA OS VALORES DE LITROS E DA NOTA PARA CALCULAR O PREÇO POR LITRO.")
        else:
            litros_abastecidos = None
            valor_nota = None
            preco_por_litro = None

        if st.button("REGISTRAR CHECK-OUT"):
            if km_final:
                checkin_atualizado = checkins_abertos.loc[checkin_selecionado].to_dict()
                checkin_atualizado['km_final'] = km_final
                checkin_atualizado['data_hora_checkout'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                checkin_atualizado['litros_abastecidos'] = litros_abastecidos
                checkin_atualizado['valor_nota'] = valor_nota
                checkin_atualizado['preco_por_litro'] = preco_por_litro
                atualizar_checkout(checkin_atualizado)
                st.success(f"CHECK-OUT REALIZADO COM SUCESSO PARA O CARRO {checkin_atualizado['carro']}!")
            else:
                st.error("POR FAVOR, PREENCHA O KM FINAL.")
    else:
        st.warning("NÃO HÁ CHECK-IN EM ABERTO PARA ESTE USUÁRIO.")

# Função para exibir apenas a visualização de registros para a coordenação
def exibir_visualizacao_coordenação():
    st.title("Visualização de Registros de Check-in e Check-out")
    df = carregar_checkins()
    st.write(df)

# Função principal do aplicativo
def app():
    if 'login' not in st.session_state or not st.session_state.login:
        st.title("BEM-VINDO! FAÇA SEU LOGIN")
        
        usuarios = [
            'COORDENAÇÃO', 'TÉC. LUIZ ANDRÉ', 'TÉC. RAFAEL PORTO', 'TÉC. MARCELO BRITO', 'TÉC. JOSÉ BRAZ',
            'TÉC. ANDERSON ALVES', 'TÉC. AILSON SILVA', 'ADM. VÍTALLO RAONY', 'TÉC. EVELYN FERNANDEZ', 
            'ENG. PAULO VICTOR', 'ENG. JOSÉ UILIAN', 'ENG. ALTEMAR JÚNIOR', 'ENG. LUAN DEMARCO', 
            'ENG. LUIZ NEVES', 'COORD. GENILSON MEDEIROS'
        ]
        
        # Ordenar a lista de usuários de forma crescente
        usuarios.sort()

        usuario_selecionado = st.selectbox("ESCOLHA O USUÁRIO", [''] + usuarios)
        
        senha = st.text_input("SENHA", type="password")
        
        if st.button("Entrar"):
            if usuario_selecionado and verificar_login(usuario_selecionado, senha):
                st.session_state.login = True
                st.session_state.usuario = usuario_selecionado
                st.success("LOGIN BEM-SUCEDIDO!")
            else:
                st.error("USUÁRIO OU SENHA INCORRETOS.")
    else:
        if st.session_state.usuario == 'COORDENAÇÃO':
            exibir_visualizacao_coordenação()
        else:
            escolha = st.radio("ESCOLHA UMA OPÇÃO", ('Check-in', 'Check-out'))
            if escolha == 'Check-in':
                exibir_formulario_checkin(st.session_state.usuario)
            elif escolha == 'Check-out':
                exibir_formulario_checkout(st.session_state.usuario)


if __name__ == "__main__":
    app()
