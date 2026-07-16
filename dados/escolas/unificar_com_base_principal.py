import unicodedata
import pandas as pd

# 1. Carregar os dados
df_censo = pd.read_csv("dados_censo_limpos.csv", encoding="utf-8-sig")
df_escolas = pd.read_csv("num_escolas_por_bairro.csv", encoding="utf-8-sig")


# 2. Função para normalizar os nomes (remover acentos, maiúsculas e espaços extras)
def normalizar_nome(nome):
    if not isinstance(nome, str):
        return ""
    n = unicodedata.normalize("NFKD", nome).encode("ascii", "ignore").decode("utf-8")
    return " ".join(n.upper().split())


df_censo["bairro_norm"] = df_censo["NM_BAIRRO"].apply(normalizar_nome)
df_escolas["bairro_norm"] = df_escolas["Bairro"].apply(normalizar_nome)

# 3. Mapeamento de variações e abreviações
mapeamento_especial = {
    "CONJUNTO RESIDENCIAL HUMAITA": "HUMAITA",
    "VILA JOQUEI CLUBE": "JOCKEY CLUB",
    "VILA NOVA SAO VICENTE": "NOVA SAO VICENTE",
}
df_escolas["bairro_norm"] = df_escolas["bairro_norm"].replace(mapeamento_especial)

# 4. Realizar o cruzamento (merge) dos dados pelo nome normalizado
df_resultado = pd.merge(
    df_censo,
    df_escolas[["bairro_norm", "Numero_de_Escolas"]],
    on="bairro_norm",
    how="left",
)

# Renomear e tratar valores ausentes
df_resultado = df_resultado.rename(columns={"Numero_de_Escolas": "num_escolas"})
df_resultado["num_escolas"] = df_resultado["num_escolas"].fillna(0).astype(int)

# Remover coluna auxiliar
df_resultado = df_resultado.drop(columns=["bairro_norm"])

# 5. Salvar o resultado
df_resultado.to_csv("dados_censo_limpos.csv", index=False, encoding="utf-8-sig")
