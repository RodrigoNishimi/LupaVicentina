import pandas as pd
import re


def extrair_bairro(endereco):
    if pd.isna(endereco):
        return None

    # 1. Pega tudo o que vem antes do CEP (ex: 11330-580)
    match = re.search(r"^(.*?)\.?\s*\b\d{5}-\d{3}\b", endereco)

    if match:
        parte_anterior = match.group(1).strip()

        # 2. Se o endereço tiver ponto antes (ex: "AVENIDA. VILA CASCATINHA"), o bairro fica na última parte
        partes = parte_anterior.split(".")
        if len(partes) > 1:
            bairro = partes[-1].strip()
            if bairro:
                return bairro

        # 3. Se não tiver ponto (ex: "984 VILA MARGARIDA"), pega o texto após o número da rua ou SN
        match_num = re.search(r"\b(\d+|SN|S/N)\b(.*?)$", parte_anterior, re.IGNORECASE)
        if match_num:
            return match_num.group(2).strip()

    return None


# Carregando a planilha original
df = pd.read_csv("escolas.csv", encoding="utf-8-sig")

# Aplicando a função para criar a coluna 'Bairro'
df["Bairro"] = df["Endereço"].apply(extrair_bairro)

# Create a mapping dictionary for standardizing names
mapping = {
    "COMPANHIA NAUTICA": "CIDADE NAUTICA",
    "VL MARGARIDA": "VILA MARGARIDA",
    "PARQUE BANDEIRAS": "PARQUE DAS BANDEIRAS",
    "HUMAITA": "CONJUNTO RESIDENCIAL HUMAITA",
    "ESP BARREIROS": "ESPLANADA DOS BARREIROS",
    "VILA JOCKEI CLUBE": "VILA JOQUEI CLUBE",
    "JOQUEI CLUBE": "VILA JOQUEI CLUBE",
    "VILA FATIMA": "VILA NOSSA SENHORA DE FATIMA",
    "VILA NOSSA FATIMA": "VILA NOSSA SENHORA DE FATIMA",
    "QUARENTENARIO": "JARDIM QUARENTENARIO",
}

# Apply the mapping, if a value is not in mapping, it remains the same
df["Bairro"] = df["Bairro"].replace(mapping)

# Salvando a nova planilha
df.to_csv("escolas_com_bairro.csv", index=False, encoding="utf-8-sig")

# Conta o número de escolas por bairro
# O reset_index() transforma o resultado da contagem de volta em um DataFrame tabular
contagem_bairros = df["Bairro"].value_counts(dropna=False).reset_index()

# 3. Renomeia as colunas para deixar a planilha final bem organizada
contagem_bairros.columns = ["Bairro", "Numero_de_Escolas"]

# Sort by number of schools descending, then by neighborhood name
contagem_bairros = contagem_bairros.sort_values(
    by=["Numero_de_Escolas", "Bairro"], ascending=[False, True]
)

# Save to a new CSV just in case
contagem_bairros.to_csv("num_escolas_por_bairro.csv", index=False)
