from fastapi import FastAPI
import pandas as pd

app = FastAPI()

# Lê o CSV e mostra os nomes das colunas no terminal
try:
    df = pd.read_csv("medicamentos.csv", sep=";", encoding="latin1")
    print("Colunas do CSV:", list(df.columns))
except Exception as e:
    print("Erro ao carregar CSV:", e)
    df = pd.DataFrame()

@app.get("/verificar/{nome_medicamento}")
def verificar_medicamento(nome_medicamento: str):
    if df.empty:
        return {"erro": "Arquivo CSV não carregado"}

    nome_medicamento = nome_medicamento.lower()

    try:
        # ATENÇÃO: aqui usa o nome real da coluna com underline
        resultado = df[df['NOME_PRODUTO'].str.lower().str.contains(nome_medicamento, na=False)]
    except Exception as e:
        return {"erro": f"Erro ao buscar medicamento: {str(e)}"}

    if resultado.empty:
        return {"medicamento": nome_medicamento, "status": "Não encontrado"}

    registro = resultado.iloc[0]

    return {
        "medicamento": registro.get("NOME_PRODUTO", ""),
        "princípio_ativo": registro.get("PRINCÍPIO_ATIVO", ""),
        "registro_anvisa": registro.get("NUMERO_REGISTRO_PRODUTO", ""),
        "empresa": registro.get("EMPRESA_DETENTORA_REGISTRO", ""),
        "validade": registro.get("DATA_VENCIMENTO_REGISTRO", ""),
        "status": "Liberado pela Anvisa"
    }