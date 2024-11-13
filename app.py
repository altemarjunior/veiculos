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

# Função para exibir o formulário de check-in de veículo com verificação de check-out pendente
def exibir_formulario_checkin(usuario):
    st.title("CONTROLE DE VEÍCULOS - CHECK-IN")

    carros_disponiveis = ['HILLUX PRATA - JKE-2B37 ', 'HILLUX PRATA - NUJ-4B69', 'HILLUX PRATA- OHP-4744',
                          'HILLUX PRATA - OVT-9G29', 'HILLUX PRATA - PAB-4F32', 'ONIX - QRA-4B06', 'ONIX - QTG-5C61',
                          'SAVEIRO BRANCA - QTF-2G13', 'STRADA BRANCA - QTG-4D21', 'STRADA CINZA - THJ-2D86']
    carro = st.selectbox("ESCOLHA O VEÍCULO", carros_disponiveis)
    
    # Obter o último km_final do veículo selecionado
    df = carregar_checkins()
    ultimo_km_final = df[(df['carro'] == carro) & (df['km_final'].notna())].sort_values(by='data_hora_checkout', ascending=False)['km_final'].head(1)
    km_inicial = ultimo_km_final.iloc[0] if not ultimo_km_final.empty else 0  # Km inicial é o último km final registrado

    st.number_input("KM INICIAL", min_value=0, value=km_inicial, key="km_inicial", disabled=True)
    
    locais = ['ESCRITÓRIO', 'UNIDADE LOCAL - HUMAITÁ', 'MANAUS', 'BR-319/AM - SENTIDO MANAUS', 'BR-319/AM - SENTIDO PORTO VELHO-RO', 'BR-230/AM - SENTIDO LÁBREA', 'BR-230/AM - SENTIDO APUÍ',
              'BR-317/AM', 'LABORATÓRIO', 'ALOJAMENTO', 'POSTO DE COMBUSTÍVEL', 'PORTO VELHO-RO']
    origem = st.selectbox("LOCAL DE ORIGEM", locais + ['Outro...'], key="origem")
    if origem == 'Outro...':
        origem = st.text_input("ESCREVA O LOCAL DE ORIGEM", "")
    destino = st.selectbox("LOCAL DE DESTINO", locais + ['Outro...'], key="destino")
    if destino == 'Outro...':
        destino = st.text_input("ESCREVA O LOCAL DE DESTINO", "")

    # Verificar check-out pendente para o carro selecionado
    checkin_aberto = df[(df['carro'] == carro) & (df['km_final'].isna())]

    if not checkin_aberto.empty:
        usuario_pendente = checkin_aberto.iloc[0]['usuario']
        st.warning(f"O usuário {usuario_pendente} não realizou check-out para o veículo {carro}. Consulte-o para liberar o check-in.")
    else:
        # Definir o fuso horário do Amazonas (UTC-4)
        fuso_amazonas = pytz.timezone('America/Manaus')

        # Obter a data e hora atual (horário local)
        data_hora_local = datetime.datetime.now()

        # Ajustar para o fuso horário do Amazonas (UTC-4)
        data_hora_checkin = data_hora_local - datetime.timedelta(hours=4)

       if st.button("REGISTRAR CHECK-IN"):
    # Permitir que `km_inicial` seja zero e continue com o check-in
    if carro and (km_inicial is not None) and origem and destino:
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


# Outras funções permanecem iguais...

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
