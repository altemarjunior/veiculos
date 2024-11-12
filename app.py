import streamlit as st
import pandas as pd
import datetime
import pytz

# Função para verificar o login
def verificar_login(usuario, senha):
    usuarios_validos = {
        'COORDENAÇÃO': '67321', 'TÉC. LUIZ ANDRÉ': '12345', 'TÉC. RAFAEL PORTO': '12345', 'TÉC. ANDERSON ALVES': '12345',
        'TÉC. AILSON SILVA': '12345', 'ENG. PAULO VICTOR': '12345', 'ENG. JOSÉ UILIAN': '12345', 'ENG. LUIZ NEVES': '12345',
        'ADM. VÍTALLO RAONY': '12345', 'TÉC. EVELYN FERNANDEZ': '12345', 'COORD. GENILSON MEDEIROS': '12345',
        'TÉC. MARCELO BRITO': '12345', 'ENG. ALTEMAR JÚNIOR': '12345', 'ENG. LUAN DEMARCO': '12345', 'TÉC. JOSÉ BRAZ': '12345'
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

# Função para carregar usuários e senhas do arquivo
def carregar_usuarios():
    try:
        df = pd.read_excel('usuarios_senhas.xlsx')
    except FileNotFoundError:
        # Criar um DataFrame inicial com os usuários
        df = pd.DataFrame({
            'usuario': ['COORDENAÇÃO', 'TÉC. LUIZ ANDRÉ', 'TÉC. RAFAEL PORTO', 'TÉC. MARCELO BRITO', 'TÉC. JOSÉ BRAZ',
                        'TÉC. ANDERSON ALVES', 'TÉC. AILSON SILVA', 'ADM. VÍTALLO RAONY', 'TÉC. EVELYN FERNANDEZ',
                        'ENG. PAULO VICTOR', 'ENG. JOSÉ UILIAN', 'ENG. ALTEMAR JÚNIOR', 'ENG. LUAN DEMARCO', 
                        'ENG. LUIZ NEVES', 'COORD. GENILSON MEDEIROS'],
            'senha': ['67321', '12345', '12345', '12345', '12345', '12345', '12345', '12345', '12345', '12345', 
                      '12345', '12345', '12345', '12345', '12345']
        })
        df.to_excel('usuarios_senhas.xlsx', index=False)
    return df

# Função para verificar login com DataFrame
def verificar_login_df(usuario, senha):
    df = carregar_usuarios()
    return not df[(df['usuario'] == usuario) & (df['senha'] == senha)].empty

# Função para alterar senha
def alterar_senha(usuario, nova_senha):
    df = carregar_usuarios()
    df.loc[df['usuario'] == usuario, 'senha'] = nova_senha
    df.to_excel('usuarios_senhas.xlsx', index=False)
    st.success("Senha alterada com sucesso!")

# Função principal do aplicativo
def app():
    if 'login' not in st.session_state or not st.session_state.login:
        st.title("BEM-VINDO! FAÇA SEU LOGIN")
        
        usuarios = carregar_usuarios()['usuario'].tolist()
        usuario_selecionado = st.selectbox("ESCOLHA O USUÁRIO", [''] + sorted(usuarios))
        
        senha = st.text_input("SENHA", type="password")
        
        if st.button("Entrar"):
            if usuario_selecionado and verificar_login_df(usuario_selecionado, senha):
                st.session_state.login = True
                st.session_state.usuario = usuario_selecionado
                st.success("LOGIN BEM-SUCEDIDO!")
            else:
                st.error("USUÁRIO OU SENHA INCORRETOS.")
    else:
        st.subheader(f"Bem-vindo, {st.session_state.usuario}")
        
        if st.session_state.usuario == 'COORDENAÇÃO':
            exibir_visualizacao_coordenação()
        else:
            escolha = st.radio("ESCOLHA UMA OPÇÃO", ('Check-in', 'Check-out', 'Alterar senha'))
            
            if escolha == 'Check-in':
                exibir_formulario_checkin(st.session_state.usuario)
            elif escolha == 'Check-out':
                exibir_formulario_checkout(st.session_state.usuario)
            elif escolha == 'Alterar senha':
                nova_senha = st.text_input("Digite a nova senha", type="password")
                confirmar_senha = st.text_input("Confirme a nova senha", type="password")
                
                if st.button("Alterar senha"):
                    if nova_senha == confirmar_senha:
                        alterar_senha(st.session_state.usuario, nova_senha)
                    else:
                        st.error("As senhas não coincidem.")

if __name__ == "__main__":
    app()
