# Função para carregar check-ins do arquivo
def carregar_checkins():
    try:
        df = pd.read_excel('dados_checkin_checkout.xlsx')
    except FileNotFoundError:
        df = pd.DataFrame(columns=[
            'carro', 'km_inicial', 'km_final', 'origem', 'destino', 'usuario', 
            'data_hora_checkin', 'data_hora_checkout', 'litros_abastecidos', 
            'valor_nota', 'preco_por_litro'
        ])
    return df

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

# Função para exibir apenas a visualização de registros para a coordenação
def exibir_visualizacao_coordenação():
    st.title("Visualização de Registros de Check-in e Check-out")
    
    # Carregar os dados existentes
    df = carregar_checkins()
    
    if df.empty:
        st.warning("Nenhum registro encontrado.")
    else:
        # Exibir os dados incluindo informações de abastecimento
        st.dataframe(df)

# Resto do código permanece igual...

if __name__ == "__main__":
    app()
