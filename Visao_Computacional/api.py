import os
import joblib
import pandas as pd
from flask import Flask, request, jsonify

app = Flask(__name__)

# Resolução do caminho do modelo salvo na Etapa 2
import os
import joblib

# Diretório onde o api.py está (Visao_Computacional)
DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))

# Sobe um nível para a raiz do repositório (Machine_Learning) e entra em ML/Ficheiro_IA
CAMINHO_MODELO = os.path.abspath(
    os.path.join(DIRETORIO_ATUAL, "..", "ML", "Ficheiro_IA", "Register_IA.joblib")
)

# Caso o script venha a ser movido para a raiz no futuro:
if not os.path.exists(CAMINHO_MODELO):
    CAMINHO_MODELO = os.path.abspath(
        os.path.join(DIRETORIO_ATUAL, "ML", "Ficheiro_IA", "Register_IA.joblib")
    )

try:
    modelo = joblib.load(CAMINHO_MODELO)
    print(f"[OK] Modelo carregado com sucesso de: {CAMINHO_MODELO}")
except Exception as e:
    modelo = None
    print(f"[Erro] Falha ao carregar o modelo: {e}")


@app.route("/", methods=["GET"])
def home():
    """Rota inicial para checagem do status da API."""
    return jsonify({
        "sistema": "MetalTech Soluções Industriais S.A.",
        "servico": "API Preditiva de Falhas de Motores",
        "status": "Online",
        "modelo_carregado": modelo is not None
    }), 200


@app.route("/predict", methods=["POST"])
def predict():
    """
    Rota que recebe as leituras de telemetria via JSON
    e retorna o risco de falha do motor.
    """
    if modelo is None:
        return jsonify({"erro": "Modelo preditivo não carregado no servidor."}), 500

    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "Corpo da requisição deve ser um JSON válido."}), 400

    # Validação dos campos obrigatórios esperados pelo modelo
    campos_obrigatorios = ["Temperatura_C", "Vibracao_mms", "Pressao_bar"]
    for campo in campos_obrigatorios:
        if campo not in dados:
            return jsonify({"erro": f"Campo obrigatório ausente: {campo}"}), 400

    try:
        # Monta DataFrame com as variáveis na ordem esperada
        entrada_df = pd.DataFrame([{
            "Temperatura_C": float(dados["Temperatura_C"]),
            "Vibracao_mms": float(dados["Vibracao_mms"]),
            "Pressao_bar": float(dados["Pressao_bar"])
        }])

        # Inferência
        predicao_valor = float(modelo.predict(entrada_df)[0])

        # Se o modelo for regressão, usamos limiar 0.5 para falha; se for classificação, já vem 0 ou 1
        tem_falha = predicao_valor >= 0.5
        score_falha = max(0.0, min(1.0, predicao_valor))

        return jsonify({
            "risco_de_falha": "Sim" if tem_falha else "Não",
            "score_falha": round(score_falha, 4),
            "status_operacional": "Crítico" if tem_falha else "Normal",
            "alerta": tem_falha
        }), 200

    except Exception as e:
        return jsonify({"erro": f"Erro interno ao processar predição: {str(e)}"}), 500


if __name__ == "__main__":
    # Roda o servidor local na porta 5000
    app.run(host="0.0.0.0", port=5000, debug=True)