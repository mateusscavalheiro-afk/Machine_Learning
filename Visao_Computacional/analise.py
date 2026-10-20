import os
import cv2
import numpy as np

def analisar_diferenca_referencia(
    caminho_referencia: str,
    caminho_teste: str,
    limiar_sensibilidade: int = 28,
    tolerancia_defeito_pct: float = 1.0
):
    """
    Compara uma peca de teste contra a peca padrao (gabarito).
    Detecta e mapeia granulados de danos, riscos, trincas ou desgaste.
    """
    if not os.path.exists(caminho_referencia):
        print(f"[Erro] Imagem de referência não encontrada: {caminho_referencia}")
        return
    if not os.path.exists(caminho_teste):
        print(f"[Erro] Imagem de teste não encontrada: {caminho_teste}")
        return

    # 1. Leitura das imagens
    img_ref = cv2.imread(caminho_referencia)
    img_teste = cv2.imread(caminho_teste)

    # Redimensiona para o mesmo tamanho caso venham de fontes com resoluções diferentes
    if img_ref.shape != img_teste.shape:
        img_teste = cv2.resize(img_teste, (img_ref.shape[1], img_ref.shape[0]))

    # 2. Conversão para escala de cinza
    gray_ref = cv2.cvtColor(img_ref, cv2.COLOR_BGR2GRAY)
    gray_teste = cv2.cvtColor(img_teste, cv2.COLOR_BGR2GRAY)

    # 3. Suavização para filtrar ruídos finos de iluminação
    blur_ref = cv2.GaussianBlur(gray_ref, (7, 7), 0)
    blur_teste = cv2.GaussianBlur(gray_teste, (7, 7), 0)

    # 4. Diferença Absoluta entre a referência boa e a peça em teste
    diferenca = cv2.absdiff(blur_ref, blur_teste)

    # 5. Segmentação do dano (Limiarização)
    _, mascara_defeito = cv2.threshold(diferenca, limiar_sensibilidade, 255, cv2.THRESH_BINARY)

    # Limpeza de micro-ruídos pontuais mantendo os riscos e falhas reais
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    mascara_limpa = cv2.morphologyEx(mascara_defeito, cv2.MORPH_OPEN, kernel)

    # 6. Cálculo da severidade do defeito
    # Ignora o fundo branco da imagem (pixels próximos de 255) para medir apenas a área da peça
    mascara_peca = gray_teste < 245
    total_pixels_peca = np.sum(mascara_peca)
    pixels_com_defeito = np.sum((mascara_limpa > 0) & mascara_peca)

    pct_defeito = (pixels_com_defeito / total_pixels_peca) * 100 if total_pixels_peca > 0 else 0

    status = "APROVADO" if pct_defeito <= tolerancia_defeito_pct else "REPROVADO"
    cor_status = (0, 255, 0) if status == "APROVADO" else (0, 0, 255)

    # 7. Criar o Mapa Visual com o Granulado do Dano
    overlay_defeito = img_teste.copy()
    # Pinta em vermelho (BGR: 0, 0, 255) exatamente os pontos de dano detectados
    overlay_defeito[mascara_limpa > 0] = [0, 0, 255]

    # Mescla com transparência sobre a peça inspecionada
    resultado_final = cv2.addWeighted(img_teste, 0.60, overlay_defeito, 0.40, 0)

    # Anotações visuais no resultado
    cv2.putText(resultado_final, f"Status: {status}", (40, 80), cv2.FONT_HERSHEY_SIMPLEX, 1.8, cor_status, 4)
    cv2.putText(resultado_final, f"Area Danificada: {pct_defeito:.2f}%", (40, 150), cv2.FONT_HERSHEY_SIMPLEX, 1.4, (0, 255, 255), 3)

    # Salvar a imagem de granulado isolada e a imagem com o dano sobreposto
    pasta_destino = os.path.dirname(caminho_teste)
    nome_arquivo = os.path.splitext(os.path.basename(caminho_teste))[0]
    
    caminho_granulado = os.path.join(pasta_destino, f"{nome_arquivo}_granulado_mascara.png")
    caminho_analise = os.path.join(pasta_destino, f"{nome_arquivo}_analise_dano.png")

    cv2.imwrite(caminho_granulado, mascara_limpa)
    cv2.imwrite(caminho_analise, resultado_final)

    print(f"\n=======================================================")
    print(f"Peça Inspecionada: {os.path.basename(caminho_teste)}")
    print(f"Dano Detectado   : {pct_defeito:.2f}% da superfície")
    print(f"Decisão          : {status}")
    print(f"Mapeamento salvo : {caminho_analise}")
    print(f"Máscara granular : {caminho_granulado}")
    print(f"=======================================================")


if __name__ == "__main__":
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    pasta_assets = os.path.join(diretorio_atual, "assets")

    # Caminho da peça gabarito (referência perfeita)
    # Certifique-se de que o arquivo tampa_boa.jpg está salvo dentro de Visao_Computacional/assets/
    peca_referencia = os.path.join(pasta_assets, "tampa_boa.jpg")

    # Lista todas as peças de teste na pasta assets (exceto a própria referência e imagens de resultado)
    if os.path.exists(peca_referencia):
        arquivos = [
            os.path.join(pasta_assets, f)
            for f in os.listdir(pasta_assets)
            if f.lower().endswith((".png", ".jpg", ".jpeg"))
            and f != "tampa_boa.jpg"
            and not f.endswith("_analise_dano.png")
            and not f.endswith("_granulado_mascara.png")
            and not f.endswith("_resultado.png")
            and not f.endswith("_resultado.jpg")
        ]

        for peca_teste in arquivos:
            analisar_diferenca_referencia(peca_referencia, peca_teste)
    else:
        print(f"[Alerta] Coloque a imagem padrão 'tampa_boa.jpg' dentro de: {pasta_assets}")