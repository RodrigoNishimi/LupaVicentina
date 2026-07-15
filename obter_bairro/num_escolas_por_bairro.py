import pandas as pd

# 1. Carrega a planilha gerada no passo anterior
nome_arquivo_entrada = "escolas_completo.csv"
df = pd.read_csv(nome_arquivo_entrada)

# 2. Conta o número de escolas por bairro
# O reset_index() transforma o resultado da contagem de volta em um DataFrame tabular
contagem_bairros = df["bairro_encontrado"].value_counts(dropna=False).reset_index()

# 3. Renomeia as colunas para deixar a planilha final bem organizada
contagem_bairros.columns = ["Bairro", "Numero_de_Escolas"]

# (Opcional) Mostra os 10 bairros com mais escolas direto no terminal
print("Top 10 Bairros com mais escolas:")
print(contagem_bairros.head(10))
print("-" * 50)

# 4. Salva o resultado final em uma nova planilha
nome_arquivo_saida = "contagem_escolas_por_bairro.csv"
contagem_bairros.to_csv(nome_arquivo_saida, index=False)

print(f"\nResumo gerado com sucesso! Salvo como: {nome_arquivo_saida}")
