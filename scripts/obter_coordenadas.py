import time
import re
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

geolocator = Nominatim(user_agent="resgate_coordenadas_sv")

# =======================================================
# Configurações de Arquivos
# =======================================================
arquivo_saude = "estabelecimento_saude_filtrado_geolocalizado.csv"
arquivo_escolas = "escolas_com_bairro_filtrado_geolocalizado.csv"

# Sua lista exata de falhas
texto_falhas = """
[ SAÚDE ]
Linha 070 | AV PREFEITO JOSE MONTEIRO, 422, CENTRO, 11340190, Brasil
Linha 101 | AV CAP MOR AGUIAR, 658, CENTRO, 11310100, Brasil
Linha 103 | AV CAPITAO MOR AGUIAR, 658, CENTRO, 11310020, Brasil
Linha 117 | AVPRESIDENTE WILSON, 1473, CENTRO, 11320001, Brasil
Linha 289 | AMADOR BUENO DA RIBEIRA, 64, GONZAGUINHA, 11320060, Brasil
Linha 290 | GONCALO MONTEIRO, 189, GONZAGUINHA, 11320110, Brasil
Linha 309 | AVENIDA PRESIDENTE WILSON, 1033, ITARARE, 11320001, Brasil
Linha 311 | AV PRES WILSON, 1033, ITARARE, 11320001, Brasil
Linha 312 | AV PRES WILSON, 1033, ITARARE, 11320001, Brasil
Linha 314 | R ONZE DE JUNHO, 96, ITARARE, 11320160, Brasil
Linha 339 | RUA FRANCISCO SILVA SANTOS, 20, JD GUASSU, 11370350, Brasil
Linha 346 | AV PREFEITO JOSE MONTEIRO, 765, JD INDEPENDENCIA, 11380001, Brasil
Linha 348 | RUA PROPRIA, 114, JD PARAISO, 11370570, Brasil
Linha 355 | AV ULISSES GUIMARAES, 791, JD RIO BRANCO, 11347000, Brasil
Linha 356 | AV DEPUTADO ULISSES GUIMARAES, 1546, JD RIO BRANCO, 11347000, Brasil
Linha 385 | AV ANTONIO EMMERICH, 110, VILA CASCATINHA, 11390000, Brasil
Linha 398 | RUA ERNESTO INTRIERI, 65, VILA MARGARIDA, 11335000, Brasil
Linha 405 | AV ANTONIO EMMERICH, 1748, VILA SAO JORGE, 11380001, Brasil
Linha 411 | AV MARECHAL DEODORO, 581, VILA VALENCA, 11390100, Brasil
Linha 413 | AV MAL DEODORO, 581, VILA VALENCA, 11390100, Brasil
Linha 414 | AV MAL DEODORO, 581, VILA VALENCA, 11390100, Brasil
Linha 417 | AV MAL DEODORO, 737, VILA VALENCA, 11320000, Brasil

[ ESCOLAS ]
Linha 002 | MONTE BELVEDERE, 984 VILA MARGARIDA. 11330-580 São Vicente - SP.
Linha 021 | SANTA CRUZ, 110 CENTRO. 11310-290 São Vicente - SP.
Linha 022 | CAPITAOMOR AGUIAR, 898 CENTRO. 11310-200 São Vicente - SP.
Linha 023 | ENGENHEIRO ANDRE REBOUCAS, 10 VILA MATEO BEI. 11335-340 São Vicente - SP.
Linha 025 | MARECHAL DEODORO, 219 VILA VALENCA. 11390-100 São Vicente - SP.
Linha 031 | PERO VAZ DE CAMINHA, 303 VILA VALENCA. 11390-040 São Vicente - SP.
Linha 032 | STELIO MACHADO LOUREIRO, 66 VILA NOSSA SENHORA DE FATIMA. 11355-240 São Vicente - SP.
Linha 035 | RIO SERCHIO, SN VILA MARGARIDA. 11330-640 São Vicente - SP.
Linha 037 | PADRE MANOEL DA NOBREGA, KM283 SAMARITA. 11346-300 São Vicente - SP.
Linha 038 | ANTONIO EMMERICK, 877 VILA CASCATINHA. 11390-001 São Vicente - SP.
Linha 043 | CAPITAOMOR AGUIAR, 512 CENTRO. 11310-200 São Vicente - SP.
Linha 044 | ANTONIO EMMERICK, 410 VILA CASCATINHA. 11390-001 São Vicente - SP.
Linha 047 | MARECHAL MASCARENHAS DE MORAES, 390 VILA MARGARIDA. 11330-000 São Vicente - SP.
Linha 048 | JACOB EMERICK, 1062 CENTRO. 11310-070 São Vicente - SP.
Linha 049 | VICENTE GIL, 368 CATIAPOA. 11390-320 São Vicente - SP.
Linha 051 | GOIAS, 740 JARDIM IRMA DOLORES. 11347-515 São Vicente - SP.
Linha 052 | MONTE PLANO, 513 VILA MARGARIDA. 11335-020 São Vicente - SP.
Linha 053 | TIBIRICA, 370 CENTRO. 11320-020 São Vicente - SP.
Linha 209 | EMILIO JUSTO DEPUTADO, 202 RUA. CONJUNTO RESIDENCIAL HUMAITA. 11349-030 São Vicente - SP.
Linha 214 | PRAIA DE PARANAPUA, SN AVENIDA. ALDEIA PARANAPUA. 11325-010 São Vicente - SP.
Linha 220 | RODOVIA PADRE MANOEL DA NOBREGA, SAMARITA. 11346-300 São Vicente - SP.
Linha 225 | PC ADALBERTO PANZAN, 151 ESPLANADA DOS BARREIROS. 11340-265 São Vicente - SP.
Linha 226 | JEQUIE, 1888 RUA. JARDIM RIO NEGRO. 11347-400 São Vicente - SP.
Linha 228 | PADRE MANOEL DA NOBREGA, SN KM 282. PARQUE CONTINENTAL. 11348-910 São Vicente - SP.
Linha 235 | VALE DO PO, 400 VL MARGARIDA. 11330-670 São Vicente - SP.
"""


# =======================================================
# Funções
# =======================================================
def limpar_endereco(linha, categoria):
    num_linha, endereco_ruim = [p.strip() for p in linha.split("|")]

    if categoria == "saude":
        endereco_limpo = re.sub(r",\s*\d{8},?\s*Brasil", "", endereco_ruim)
        endereco_limpo = endereco_limpo.replace("AVPRESIDENTE", "Avenida Presidente")
        endereco_limpo = endereco_limpo.replace("AV PRES ", "Avenida Presidente ")
        endereco_limpo = endereco_limpo.replace("AV CAP MOR", "Avenida Capitão-Mor")
        endereco_limpo = endereco_limpo.replace("AV CAPITAO MOR", "Avenida Capitão-Mor")
        endereco_limpo = endereco_limpo.replace("AV MAL ", "Avenida Marechal ")
        endereco_limpo = endereco_limpo.replace("R ONZE DE JUNHO", "Rua Onze de Junho")
        endereco_limpo = f"{endereco_limpo}, São Vicente, SP, Brasil"

    else:
        endereco_limpo = re.sub(r"\d{5}-\d{3}\s*", "", endereco_ruim)
        endereco_limpo = endereco_limpo.replace(".", ",")
        endereco_limpo = endereco_limpo.replace(" RUA,", ",")
        endereco_limpo = endereco_limpo.replace(" AVENIDA,", ",")
        endereco_limpo = endereco_limpo.replace("CAPITAOMOR", "CAPITAO MOR")
        endereco_limpo = re.sub(r"(\d+)\s+([A-Za-z])", r"\1, \2", endereco_limpo)

    return num_linha, endereco_limpo


def buscar(endereco):
    try:
        loc = geolocator.geocode(endereco, timeout=10)
        time.sleep(1)
        if loc:
            return loc.latitude, loc.longitude
    except:
        time.sleep(2)
    return None, None


def validar_coordenadas_leaflet(df, nome_base, col_lat, col_lon):
    """
    Verifica se todas as coordenadas do DataFrame estão no formato e range
    aceitáveis pelo Leaflet.js (numéricos, sem vazios e dentro dos limites terrestres).
    """
    print(f"\n--- Verificando integridade para o Leaflet.js: {nome_base} ---")
    if df is None or df.empty:
        print("Aviso: Base de dados vazia ou não carregada.")
        return

    # Força a conversão para numérico (qualquer texto ou lixo vira NaN)
    lat_num = pd.to_numeric(df[col_lat], errors="coerce")
    lon_num = pd.to_numeric(df[col_lon], errors="coerce")

    # Identifica onde existem problemas:
    mask_vazias = lat_num.isna() | lon_num.isna()
    mask_lat_invalida = (lat_num < -90.0) | (lat_num > 90.0)
    mask_lon_invalida = (lon_num < -180.0) | (lon_num > 180.0)

    # Junta todas as condições de erro
    mask_erros = mask_vazias | mask_lat_invalida | mask_lon_invalida
    linhas_com_erro = df[mask_erros]

    if linhas_com_erro.empty:
        print(
            "✓ SUCESSO: Todas as coordenadas estão válidas e perfeitamente formatadas para o Leaflet!"
        )
    else:
        print(
            f"⚠ ATENÇÃO: Encontradas {len(linhas_com_erro)} linhas incompatíveis com o mapa."
        )
        print("Esses itens farão o marcador quebrar ou não renderizar. Verifique-os:")
        for idx, row in linhas_com_erro.iterrows():
            linha_excel = idx + 2
            v_lat = row[col_lat]
            v_lon = row[col_lon]
            print(f"   -> Linha Excel {linha_excel}: Lat = {v_lat}, Lon = {v_lon}")


# =======================================================
# Carregamento das Planilhas
# =======================================================
df_saude = None
df_escolas = None

try:
    print(f"Carregando {arquivo_saude}...")
    df_saude = pd.read_csv(arquivo_saude, encoding="utf-8-sig")
except Exception as e:
    print(f"Erro ao carregar base de Saúde: {e}")

try:
    print(f"Carregando {arquivo_escolas}...")
    df_escolas = pd.read_csv(arquivo_escolas, encoding="utf-8-sig")
except Exception as e:
    print(f"Erro ao carregar base de Escolas: {e}")


# =======================================================
# Processamento e Resgate
# =======================================================
lista_enderecos_otimizados = []
lista_falhas_finais = []
categoria_atual = ""

print("\nIniciando resgate e preenchimento de coordenadas...")
print("================ PROGRESSO ==================")

for linha in texto_falhas.strip().split("\n"):
    if not linha.strip():
        continue
    if "[ SAÚDE ]" in linha:
        categoria_atual = "saude"
        print("\n--- PROCESSANDO SAÚDE ---")
        continue
    if "[ ESCOLAS ]" in linha:
        categoria_atual = "escolas"
        print("\n--- PROCESSANDO ESCOLAS ---")
        continue

    num_linha_str, endereco_otimizado = limpar_endereco(linha, categoria_atual)
    lista_enderecos_otimizados.append(f"{num_linha_str} | {endereco_otimizado}")

    # Converte string "Linha 070" para o índice real do Pandas (Ex: 70 - 2 = 68)
    num_linha_int = int(num_linha_str.replace("Linha", "").strip())
    idx_pandas = num_linha_int - 2

    lat, lon = buscar(endereco_otimizado)
    usou_rua = False

    if not lat:
        # Tenta buscar só pela rua
        rua = endereco_otimizado.split(",")[0]
        cidade = "São Vicente, SP"
        lat, lon = buscar(f"{rua}, {cidade}")
        usou_rua = True if lat else False

    # Se encontrou coordenadas, injeta na planilha correta
    if lat and lon:
        if categoria_atual == "saude" and df_saude is not None:
            df_saude.at[idx_pandas, "NU_LATITUDE"] = lat
            df_saude.at[idx_pandas, "NU_LONGITUDE"] = lon

        elif categoria_atual == "escolas" and df_escolas is not None:
            df_escolas.at[idx_pandas, "Latitude"] = lat
            df_escolas.at[idx_pandas, "Longitude"] = lon

        texto_sucesso = "(Baseado apenas na Rua)" if usou_rua else ""
        print(f"{num_linha_str}: {lat}, {lon} {texto_sucesso} -> SALVO NA PLANILHA")
    else:
        print(f"{num_linha_str}: FAIÔ - Não encontrado nem pela rua.")
        lista_falhas_finais.append(f"{num_linha_str} | {endereco_otimizado}")


# =======================================================
# Validação Leaflet.js
# =======================================================
print("\n================ VALIDAÇÃO LEAFLET ==============")
if df_saude is not None:
    validar_coordenadas_leaflet(
        df_saude, "Planilha de Saúde", "NU_LATITUDE", "NU_LONGITUDE"
    )

if df_escolas is not None:
    validar_coordenadas_leaflet(
        df_escolas, "Planilha de Escolas", "Latitude", "Longitude"
    )


# =======================================================
# Exportação das Planilhas Finais
# =======================================================
print("\n================ SALVAMENTO =================")
if df_saude is not None:
    saude_out = "estabelecimento_saude_final.csv"
    df_saude.to_csv(saude_out, index=False, encoding="utf-8-sig", sep=",")
    print(f"Planilha de Saúde atualizada salva como: {saude_out}")

if df_escolas is not None:
    escolas_out = "escolas_com_bairro_final.csv"
    df_escolas.to_csv(escolas_out, index=False, encoding="utf-8-sig", sep=",")
    print(f"Planilha de Escolas atualizada salva como: {escolas_out}")


# =======================================================
# Saídas no Terminal (Relatórios Finais)
# =======================================================
print("\n=============================================")
print("        ENDEREÇOS OTIMIZADOS (LIMPOS)        ")
print("=============================================")
for item in lista_enderecos_otimizados:
    print(item)

print("\n=============================================")
print("  FALHAS DEFINITIVAS (API NÃO ENCONTROU)     ")
print("=============================================")
if len(lista_falhas_finais) > 0:
    for falha in lista_falhas_finais:
        print(falha)
else:
    print("Nenhuma! Todos os endereços foram encontrados na fase de resgate.")
print("=============================================\n")
