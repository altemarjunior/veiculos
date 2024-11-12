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
    
    # Verificar se o usuário existe no dicionário e se a senha bate
    return usuario in usuarios_validos and usuarios_validos[usuario] == senha

# Função para carregar check-ins do arquivo
def carregar_checkins():
    try:
        df = pd.read_excel('dados_checkin_checkout.xlsx')
    except FileNotFoundError:
        df = pd.DataFrame(columns=['carro', 'km_inicial', 'km_final', 'origem', 'destino', 'usuario', 'data_hora_checkin', 'data_hora_checkout'])
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
            
    df.to_excel('dados_checkin_checkout.xlsx', index=False)

# Função para exibir o formulário de check-in de veículo
def exibir_formulario_checkin(usuario):
    st.title("CONTROLE DE VEÍCULOS - CHECK-IN")

    carros_disponiveis = ['HILLUX PRATA - JKE-2B37 ', 'HILLUX PRATA - NUJ-4B69', 'HILLUX PRATA- OHP-4744',
                           'HILLUX PRATA - OVT-9G29', 'HILLUX PRATA - PAB-4F32', 'ONIX - QRA-4B06', 'ONIX - QTG-5C61',
                            'SAVEIRO BRANCA - QTF-2G13', 'STRADA BRANCA - QTG-4D21', 'STRADA CINZA - THJ-2D86']
    carro = st.selectbox("ESCOLHA O VEÍCULO", carros_disponiveis)
    km_inicial = st.number_input("KM INICIAL", min_value=0, key="km_inicial")
    
    locais = ['ESCRITÓRIO', 'UNIDADE LOCAL - HUMAITÁ', 'MANAUS', 'BR-319/AM - SENTIDO MANAUS', 'BR-319/AM - SENTIDO PORTO VELHO-RO', 'BR-230/AM - SENTIDO LÁBREA','BR-230/AM - SENTIDO APUÍ',
              'BR-317/AM', 'LABORATÓRIO', 'ALOJAMENTO', 'POSTO DE COMBUSTÍVEL', 'PORTO VELHO-RO']
    origem = st.selectbox("LOCAL DE ORIGEM", locais + ['Outro...'], key="origem")
    if origem == 'Outro...':
        origem = st.text_input("ESCREVA O LOCAL DE ORIGEM", "")
    destino = st.selectbox("LOCAL DE DESTINO", locais + ['Outro...'], key="destino")
    if destino == 'Outro...':
        destino = st.text_input("ESCREVA O LOCAL DE DESTINO", "")


    # Definir o fuso horário do Amazonas (UTC-4)
    fuso_amazonas = pytz.timezone('America/Manaus')

        # Obter a data e hora atual (horário local)
    data_hora_local = datetime.datetime.now()

    # Ajustar para o fuso horário do Amazonas (UTC-4), subtraindo 4 horas
    data_hora_checkin= data_hora_local - datetime.timedelta(hours=4)
    data_hora_checkout= data_hora_local - datetime.timedelta(hours=4)
    # Exemplo de DataFrame com a hora ajustada
    df = pd.DataFrame({
        'Data': [data_hora_checkin, data_hora_checkout]
    })

    if st.button("REGISTRAR CHECK-IN"):
        if carro and km_inicial and origem and destino:
            checkin = {
                "carro": carro,
                "km_inicial": km_inicial,
                "km_final": None,  
                "origem": origem,
                "destino": destino,
                "usuario": usuario,
                "data_hora_checkin": data_hora_checkin,                 
            }
            salvar_checkin(checkin)
            st.success(f"CHECK-IN REALIZADO COM SUCESSO PARA O CARRO {carro}! USE O CINTO DE SEGURANÇA E RESPEITE OS LIMITES DE VELOCIDADE. BOA VIAGEM")
        else:
            st.error("POR FAVOR, PREENCHA TODOS OS CAMPOS.")

# Função para exibir o formulário de check-out de veículo
def exibir_formulario_checkout(usuario):
    st.title("CONTROLE DE VEÍCULOS - CHECK-OUT")

    df = carregar_checkins()
    checkins_abertos = df[(df['usuario'] == usuario) & (df['km_final'].isna())]

    if not checkins_abertos.empty:
        checkin_selecionado = st.selectbox("Escolha o Check-in em Aberto", checkins_abertos.index, format_func=lambda idx: f"{checkins_abertos.loc[idx, 'carro']} - {checkins_abertos.loc[idx, 'origem']} para {checkins_abertos.loc[idx, 'destino']}")
        km_final = st.number_input("KM FINAL", min_value=0)

        if st.button("REGISTRAR CHECK-OUT"):
            if km_final:
                checkin_atualizado = checkins_abertos.loc[checkin_selecionado].to_dict()
                checkin_atualizado['km_final'] = km_final
                checkin_atualizado['data_hora_checkout'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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


# Função para limpar a planilha
#def limpar_planilha():
    # Cria um DataFrame vazio com as colunas da planilha
    #df_vazio = pd.DataFrame(columns=['carro', 'km_inicial', 'km_final', 'origem', 'destino', 'usuario', 'data_hora_checkin', 'data_hora_checkout'])
    
    # Sobrescreve o arquivo Excel com o DataFrame vazio
    #df_vazio.to_excel('dados_checkin_checkout.xlsx', index=False)
#limpar_planilha()

if __name__ == "__main__":
    app()