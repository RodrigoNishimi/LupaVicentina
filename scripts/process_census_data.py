import re
import unicodedata
from functools import reduce

import numpy as np
import pandas as pd

drop_cols = [
    "CD_REGIAO",
    "NM_REGIAO",
    "CD_UF",
    "CD_SIT",
    "CD_TIPO",
    "NM_UF",
    "CD_MUN",
    "NM_MUN",
    "CD_SUBDIST",
    "NM_SUBDIST",
    "CD_NU",
    "NM_NU",
    "CD_FCU",
    "NM_FCU",
    "CD_AGLOM",
    "NM_AGLOM",
    "CD_RGINT",
    "NM_RGINT",
    "CD_RGI",
    "NM_RGI",
    "CD_CONCURB",
    "NM_CONCURB",
    "Censo_20_1",
    "Censo_20_2",
    "Censo_20_3",
    "Censo_20_4",
    "Censo_20_5",
    "Censo_20_6",
    "Censo_20_7",
    "Censo_20_8",
    "Censo_20_9",
    "Censo_2010",
    "Censo_2011",
    "Censo_2012",
    "Censo_2013",
    "Censo_2014",
    "Censo_2015",
    "Censo_2016",
    "Censo_2017",
    "Censo_2018",
    "Censo_2019",
    "Censo_2020",
    "Censo_2021",
    "Censo_2022",
    "Censo_2023",
    "Censo_2024",
    "Censo_2025",
    "Censo_2026",
    "Censo_2027",
    "Censo_2028",
    "area_setor",
    "CD_DIST",
    "NM_DIST",
    "CD_BAIRRO",
]


unified_mapping = {
    "BEIRA MAR": "Beira Mar",
    "BOA VISTA": "Boa Vista",
    "CATIAPOA": "Catiapoã",
    "CENTRO": "Centro",
    "CIDADE NAUTICA": "Cidade Náutica",
    "COMPANHIA NAUTICA": "Cidade Náutica",
    "CIDADE NAUTICA III": "Cidade Náutica III",
    "NAUTICA III": "Cidade Náutica III",
    "CJTO HUMAITA": "Humaitá",
    "CONJUNTO RESIDENCIAL": "Conjunto Residencial",
    "CONJUNTO RESIDENCIAL HUMAITA": "Humaitá",
    "HUMAITA": "Humaitá",
    "ESPLANADA DOS BARREI": "Esplanada dos Barreiros",
    "ESP BARREIROS": "Esplanada dos Barreiros",
    "GONZAGUINHA": "Gonzaguinha",
    "ITARARE": "Itararé",
    "JAPUI": "Japuí",
    "JARDIM GUASSU": "Jardim Guassu",
    "JD GUASSU": "Jardim Guassu",
    "JARDIM INDEPENDENCIA": "Jardim Independência",
    "JD INDEPENDENCIA": "Jardim Independência",
    "JARDIM IRMA DOLORES": "Jardim Irmã Dolores",
    "JD IRMA DOLORES": "Jardim Irmã Dolores",
    "JARDIM PARAISO": "Jardim Paraíso",
    "JD PARAISO": "Jardim Paraíso",
    "JARDIM RIO BRANCO": "Jardim Rio Branco",
    "JD RIO BRANCO": "Jardim Rio Branco",
    "JARDIM RIO NEGRO": "Jardim Rio Negro",
    "JOQUEI CLUBE": "Jóckey Club",
    "VILA JOQUEI CLUBE": "Jóckey Club",
    "VILA JOCKEI CLUBE": "Jóckey Club",
    "JOCKEY CLUB": "Jóckey Club",
    "PARQUE BITARU": "Parque Bitaru",
    "PQ BITARU": "Parque Bitaru",
    "PARQUE CONTINENTAL": "Parque Continental",
    "PQ CONTINENTAL": "Parque Continental",
    "PARQUE DAS BANDEIRAS": "Parque das Bandeiras",
    "PQ DAS BANDEIRAS": "Parque das Bandeiras",
    "PRQ DAS BANDEIRAS": "Parque das Bandeiras",
    "PARQUE BANDEIRAS": "Parque das Bandeiras",
    "PARQUE SAO VICENTE": "Parque São Vicente",
    "POMPEBA": "Pompeba",
    "PONTE NOVA": "Ponte Nova",
    "QUARENTENARIO": "Jardim Quarentenário",
    "SAMARITA": "Samarita",
    "VILA CASCATINHA": "Vila Cascatinha",
    "VL CASCATINHA": "Vila Cascatinha",
    "VILA EMA": "Vila Ema",
    "VILA MARGARIDA": "Vila Margarida",
    "VL MARGARIDA": "Vila Margarida",
    "VILA MELO": "Vila Melo",
    "VILA NOSSA DO AMPARO": "Vila Nossa do Amparo",
    "VILA NOSSA SENHORA DE FATIMA": "Vila Nossa Senhora de Fátima",
    "VL NOSSA SRA DE FATI": "Vila Nossa Senhora de Fátima",
    "VILA FATIMA": "Vila Nossa Senhora de Fátima",
    "VILA NOSSA FATIMA": "Vila Nossa Senhora de Fátima",
    "VILA SAO JORGE": "Vila São Jorge",
    "VILA SAO JOSE": "Vila São José",
    "VILA VALENCA": "Vila Valença",
    "VL VALENCA": "Vila Valença",
    "VILA VOTURUA": "Vila Voturuá",
    "NOVA SAO VICENTE": "Nova São Vicente",
    "VILA NOVA SAO VICENTE": "Nova São Vicente",
    "VILA NOVA MARIANA": "Vila Nova Mariana",
    "ESPLANADA DOS BARREIROS": "Esplanada dos Barreiros",
}


def normalize_text(text):
    if not isinstance(text, str):
        return ""
    n = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("utf-8")
    return " ".join(n.upper().split())


def extract_neighborhood(address):
    if pd.isna(address):
        return None
    match = re.search(r"^(.*?)\.?\s*\b\d{5}-\d{3}\b", address)
    if match:
        part = match.group(1).strip()
        parts = part.split(".")
        if len(parts) > 1 and parts[-1].strip():
            return parts[-1].strip()
        match_num = re.search(r"\b(\d+|SN|S/N)\b(.*?)$", part, re.IGNORECASE)
        if match_num:
            return match_num.group(2).strip()
    return None


df_income = pd.read_csv("./dados/renda_2022.csv").rename(
    columns={"field_5": "renda_media"}
)
df_pop_y_i = pd.read_csv("./dados/pop_amarelos_e_indigenas_2022.csv").drop(
    columns=["field_6", "field_7", "field_8"]
)
df_pop_w_b = pd.read_csv("./dados/pop_brancos_e_negros_2022.csv").drop(
    columns=["field_2", "field_5"]
)

df_list = [df_income, df_pop_y_i, df_pop_w_b]
common_columns = list(set.intersection(*(set(df.columns) for df in df_list)))
df_census = reduce(
    lambda left, right: pd.merge(left, right, on=common_columns, how="outer"), df_list
)

df_census["NM_BAIRRO"] = (
    df_census["NM_BAIRRO"].apply(normalize_text).replace(unified_mapping)
)

df_census_clean = pd.DataFrame(
    df_census.drop(columns=[c for c in drop_cols if c in df_census.columns])
    .dropna(subset=["NM_BAIRRO"])
    .loc[df_census["NM_BAIRRO"] != "", :]
    .drop_duplicates(subset=["CD_SETOR"])
    .groupby("NM_BAIRRO", as_index=False)
    .agg(
        SITUACAO=("SITUACAO", lambda x: x.mode()[0] if not x.mode().empty else np.nan),
        AREA_KM2=("AREA_KM2", "sum"),
        pop_amarel=("pop_amarel", "sum"),
        pop_indige=("pop_indige", "sum"),
        pop_branco=("pop_branco", "sum"),
        pop_negros=("pop_negros", "sum"),
        renda_sal=(
            "renda_sal",
            lambda x: x.mode()[0] if not x.mode().empty else np.nan,
        ),
    )
)

pop_cols = ["pop_amarel", "pop_indige", "pop_branco", "pop_negros"]
df_census_clean["hab_setor"] = df_census_clean[pop_cols].sum(axis=1)
df_census_clean["AREA_KM2"] = df_census_clean["AREA_KM2"].round(15)
df_census_clean["densidade"] = (
    df_census_clean["hab_setor"] / df_census_clean["AREA_KM2"]
)
df_census_clean["hab/ha"] = df_census_clean["hab_setor"] / (
    df_census_clean["AREA_KM2"] * 100
)

df_health = pd.read_csv("./dados/estabelecimento_saude.csv").rename(
    columns={"NO_BAIRRO": "NM_BAIRRO"}
)
df_health["NM_BAIRRO"] = (
    df_health["NM_BAIRRO"].apply(normalize_text).replace(unified_mapping)
)
valid_neighborhoods = set(df_census_clean["NM_BAIRRO"].unique())
df_health = df_health[df_health["NM_BAIRRO"].isin(list(valid_neighborhoods))]
health_facilities_count = pd.DataFrame(
    df_health.groupby("NM_BAIRRO", as_index=False).agg(
        qtd_estabelecimentos=("CO_UNIDADE", "count")
    )
)

df_schools = pd.read_csv("./dados/escolas.csv", encoding="utf-8-sig")
df_schools["NM_BAIRRO"] = (
    df_schools["Endereço"]
    .apply(extract_neighborhood)
    .apply(normalize_text)
    .replace(unified_mapping)
)
schools_count = pd.DataFrame(
    df_schools.groupby("NM_BAIRRO", as_index=False).agg(
        num_escolas=("Endereço", "count")
    )
)

df_final = (
    df_census_clean.merge(health_facilities_count, on="NM_BAIRRO", how="left")
    .merge(schools_count, on="NM_BAIRRO", how="left")
    .fillna({"qtd_estabelecimentos": 0, "num_escolas": 0})
)

df_final["qtd_estabelecimentos"] = df_final["qtd_estabelecimentos"]
df_final["num_escolas"] = df_final["num_escolas"].astype(int)

col_order = [
    "NM_BAIRRO",
    "SITUACAO",
    "AREA_KM2",
    "pop_amarel",
    "pop_indige",
    "pop_branco",
    "pop_negros",
    "hab_setor",
    "densidade",
    "hab/ha",
    "renda_sal",
    "qtd_estabelecimentos",
    "num_escolas",
]

df_final = df_final[[c for c in col_order if c in df_final.columns]]
df_final.to_csv("./dados/dados_censo_limpos.csv", index=False, encoding="utf-8-sig")
