# Lupa Vicentina: Dashboard COOP Clima São Vicente

Painel web 100% estático de utilidade pública para os moradores de São Vicente (SP): demografia, escolas e unidades de saúde, bairro a bairro. Não há backend nem banco de dados — um script de ETL em Python lê as planilhas, trata os dados e gera um único index.html com todos os dados JSON embutidos, pronto para hospedar no GitHub Pages.

## Estrutura do Projeto

```text
├── assets/
│   └── logo_branco_verde.png            # Logo do projeto embutida no header
├── scripts/                             # Scripts de limpeza e obtenção de dados
│   ├── obter_coordenadas.py
│   ├── process_bases.py
│   └── process_census_data.py
├── dados.zip                            # Arquivo com os dados utilizados no Dashboard
├── etl.py                               # Script de ETL: gera o dashboard final
├── template.html                        # Template do dashboard com marcadores de injeção
├── index.html                           # ARQUIVO FINAL gerado pelo ETL (não editar à mão)
├── requirements.txt                     # Dependências do projeto
└── README.md
```

## Configuração do Ambiente

1. Extraia os dados
Descompacte o arquivo dados.zip na raiz do projeto. Isso populará a pasta dados/ com os arquivos CSV necessários.

2. Crie e ative o ambiente virtual (venv)
No Windows:
```bash
python -m venv .venv
.venv\Scripts\activate
```

No Linux/Mac:
```bash
python -m venv .venv
source .venv/bin/activate
```

3. Instale as bibliotecas necessárias
```bash
pip install -r requirements.txt
```

## Como Executar e Atualizar

1. Processar os dados base (Opcional / Se houver atualizações)
Caso precise rodar a limpeza dos dados novamente:
```bash
python scripts/process_census_data.py
```

2. Gerar o dashboard
Com as planilhas finalizadas em dados/, execute o ETL para criar o HTML:
```bash
python etl.py
```

Saída esperada:
> OK: index.html gerado.
> bairros do censo: 29 | escolas: 241 | saúde: 427
> bairros extras (sem censo): 15
> registros sem coordenada válida (fora do mapa): 47

3. Visualizar localmente
Basta abrir o index.html no navegador, ou iniciar um servidor local:
```bash
python -m http.server 8123
```

## Publicar no GitHub Pages

1. Faça commit do index.html gerado no repositório.
2. No GitHub, vá em Settings -> Pages e aponte para a branch/pasta que contém o index.html.
3. O painel ficará disponível no link gerado pelo GitHub Pages.

## O que o painel oferece

* Filtro global por bairro (dropdown) — KPIs, gráficos, mapa e tabelas atualizam sem recarregar a página.
* KPIs: população, renda média (salários mínimos), densidade (hab/ha), escolas ativas, capacidade estimada de matrículas, unidades de saúde e unidades de saúde por 10 mil habitantes.
* Gráficos (Chart.js): composição populacional por cor/raça, escolas por categoria administrativa, oferta de ensino por etapa/modalidade, porte das escolas, serviços de saúde disponíveis e cobertura SUS.
* Mapa interativo (Leaflet + OpenStreetMap): escolas públicas (laranja), escolas privadas (azul), saúde SUS (verde) e demais unidades de saúde (marrom), com controle de camadas e popups de detalhes.
* Rankings: TOP 10 bairros por escolas, por unidades de saúde e por densidade demográfica.
* Tabelas de detalhamento em abas (Escolas / Saúde), com busca por nome, endereço ou bairro.

## Decisões de Tratamento de Dados (ETL)

| Problema encontrado nos dados | Tratamento aplicado |
| :--- | :--- |
| Nomes de bairro divergentes | Normalização (maiúsculas, sem acento, abreviações expandidas), tabela de apelidos e casamento por prefixo para nomes truncados. |
| Coordenadas da base de saúde sem ponto decimal | Divisão sucessiva por 10 até a magnitude correta. |
| Pontos geocodificados fora de São Vicente | Excluídos do mapa (continuam nas tabelas); a legenda informa quantos ficaram de fora. |
| 23 escolas paralisadas | Ficam nas tabelas com status "Paralisada", mas fora dos KPIs e gráficos. |
| Porte "Mais de 1000 matrículas" (faixa aberta) | Capacidade contabilizada como 1.000 (piso da faixa) — por isso o KPI mostra valor aproximado. |
| Bairros presentes só nas bases de escolas/saúde | Aparecem no dropdown em "Outros bairros (sem dados do censo)": mapa e tabelas funcionam; indicadores demográficos exibem "-". |
| Renda média da cidade | Média por bairro ponderada pela população. |

## Identidade Visual

* Logo: A logo oficial é embutida no cabeçalho como data URI (lida pelo etl.py da pasta assets/), substituindo o título em texto. Integrada com fundo verde #007a4a.
* Cores institucionais: Verde #007a4a, marrom #874a33, azul claro #00a3e0, laranja #e87722; fundo off-white #f9f3f0.
* Tipografia: Londrina Solid (títulos) e Roboto (textos, tabelas e KPIs) via Google Fonts.
* Bibliotecas (CDN): Chart.js 4 e Leaflet 1.9 (requer internet para visualização correta).
