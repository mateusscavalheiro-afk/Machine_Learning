# PARECER TÉCNICO E SOCIOÉTICO: SISTEMA INTEGRADO DE MANUTENÇÃO PREDITIVA E INSPEÇÃO VISUAL COMPUTACIONAL

**Empresa:** MetalTech Soluções Industriais S.A.  
**Projeto:** Fábrica Inteligente: Preditiva e Visão Computacional (Etapa 3)  
**Módulo:** Visão Computacional, APIs e Análise Socioética  
**Localização do Arquivo:** `Visao_Computacional/parecer_tecnico.md`  
**Data:** 20 de Outubro de 2026  

---

## 1. Sumário Executivo

O presente parecer técnico consolida as metodologias, extensões de software, algoritmos matemáticos e implicações socioéticas referentes à implementação do protótipo de Indústria 4.0 na MetalTech Soluções Industriais S.A. O projeto integra duas frentes tecnológicas complementares:

1. **Inteligência Preditiva em Tempo Real via API RESTful:** Disponibilização de rotas HTTP para inferência de falhas em motores a partir de telemetria de sensores IoT (temperatura, vibração e pressão).
2. **Controle de Qualidade Óptico Automatizado (OpenCV):** Inspeção de componentes mecânicos (tampas de mancais de motores elétricos) por meio de visão computacional diferencial em relação a um gabarito de referência íntegro.

---

## 2. Tecnologias, Bibliotecas e Extensões Utilizadas

Para garantir interoperabilidade entre os nós industriais (CLPs/SCADA) e os sistemas de visão e IA, foram adotadas as seguintes ferramentas em ambiente Python 3:

| Tecnologia / Biblioteca | Versão / Extensão | Finalidade no Projeto |
| :--- | :--- | :--- |
| **Python** | `3.14.x` | Linguagem base de computação científica e automação. |
| **OpenCV (`cv2`)** | `opencv-python` | Processamento digital de imagem, filtragem espacial, segmentação e morfologia matemática. |
| **NumPy** | `numpy` | Manipulação matricial de canais de cor e álgebra de tensores de imagem. |
| **Flask** | `flask` | Micro-framework web para exposição de endpoints HTTP RESTful para chão de fábrica. |
| **Scikit-Learn** | `scikit-learn` | Framework onde os modelos de regressão e árvore foram desenvolvidos e serializados. |
| **Joblib** | `joblib` | Desserialização de alta performance do pipeline preditivo (`Register_IA.joblib`). |
| **Pandas** | `pandas` | Estruturação e tipagem dos dados de entrada no formato tabular consumido pelo modelo. |

### Extensões de Arquivos Manipulados no Ecossistema
* `.joblib`: Arquivo binário de modelo preditivo treinado e serializado.
* `.png` / `.jpg`: Formatos de imagem utilizados para carregar amostras cruas da esteira e gravar os laudos visuais anotados.
* `.py`: Scripts executáveis de automação da visão (`analise.py`) e do servidor de predição (`api.py`).
* `.csv`: Bases de dados de telemetria bruta e tratada da fábrica.
* `.md`: Documentação técnica, arquitetura de MLOps e parecer ético-regulatório.

---

## 3. Metodologia de Visão Computacional: Análise e Geração da Peça

### 3.1. Conceito: Inspeção por Comparação com Padrão Gabarito (*Golden Template*)
Em linhas de usinagem e fundição da MetalTech, as peças conformes compartilham geometria, furações de fixação e nervuras estruturais milimetricamente padronizadas. Portanto, a inspeção visual foi implementada comparando a peça inspecionada contra um gabarito mestre de fábrica (`tampa_boa.jpg`).

### 3.2. Passo a Passo do Pipeline de Processamento (`analise.py`)
O fluxo implementado no script processa cada componente através das seguintes etapas sequenciais:

1. **Leitura e Equalização Dimensional:**
   * Leitura da imagem de referência ($I_{ref}$) e da imagem de teste ($I_{teste}$).
   * Se houver discrepância de resolução entre câmeras, a imagem de teste é redimensionada bilinearmente para coincidir exatamente com as dimensões de $I_{ref}$.

2. **Conversão para Escala de Cinza (`cv2.cvtColor`):**
   * Redução dos 3 canais de cor (BGR) para intensidade luminosa de 8 bits (valores de $0$ a $255$), reduzindo custo computacional e eliminando variações térmicas de cor do ambiente fabril.

3. **Filtro Gaussiano (`cv2.GaussianBlur`):**
   * Aplicação de convolução com kernel $7 \times 7$ com desvio padrão nulo ajustado automaticamente ($\sigma = 0$) para eliminar micro-ruídos estocásticos de iluminação, trepidação de esteira e artefatos de compressão JPEG.

4. **Diferença Absoluta de Intensidade (`cv2.absdiff`):**
   * Cálculo da divergência ponto a ponto:
     $$D(x, y) = |I_{ref}(x, y) - I_{teste}(x, y)|$$
   * Regiões intactas e sem alteração resultam em valor próximo a zero (preto); riscos, trincas, quebras e corrosões geram picos luminosos de diferença.

5. **Limiarização Binária (`cv2.threshold`):**
   * Segmentação das regiões que ultrapassam o limiar de sensibilidade ($\text{threshold} = 28$), convertendo o mapa contínuo em uma máscara booleana preliminar de defeito.

6. **Morfologia Matemática de Abertura (`cv2.morphologyEx` com `MORPH_OPEN`):**
   * Aplicação de um elemento estruturante retangular $3 \times 3$ para erodir pixels isolados de ruído de sensor e em seguida dilatar as regiões conexas, isolando o granulado real dos danos mecânicos.

7. **Cálculo da Severidade do Dano:**
   * Para evitar falsos positivos do fundo da bancada, o sistema gera uma máscara da geometria da peça (pixels com $\text{intensidade} < 245$).
   * A severidade do defeito é mensurada percentualmente:
     $$\text{Área Danificada (\%)} = \left( \frac{\sum \text{Pixels de Defeito}}{\sum \text{Pixels Totais da Peça}} \right) \times 100$$
   * **Critério de Aceitação:** Tolerância máxima de até $1.00\%$ de área superficial afetada. Se superior, o lote é automaticamente classificado como **REPROVADO**.

### 3.3. Geração dos Laudos Visuais
O algoritmo exporta dois artefatos visuais na pasta `assets/`:
* **Máscara Granular (`_granulado_mascara.png`):** Imagem binária pura exibindo com precisão espacial o desenho das falhas, fissuras e áreas desgastadas.
* **Overlay com Mapeamento Térmico (`_analise_dano.png`):** Fusão com transparência ponderada ($60\%$ da peça original somada a $40\%$ da camada vermelha nas coordenadas do defeito), acompanhada de texto com o status de homologação e a porcentagem quantificada de avaria. No teste da tampa oxidada/danificada (`tampa_ruim.jpg`), o sistema identificou e demarcou com precisão **7,98% de danos estruturais superficiais**, emitindo a reprovação imediata.

---

## 4. Integração com a Linha de Produção via API RESTful (`api.py`)

A tomada de decisão preditiva quanto ao risco mecânico dos motores da MetalTech foi encapsulada em um microserviço HTTP desenvolvido em Flask.

* **Arquivo:** `Visao_Computacional/api.py`
* **Porta de Execução:** `5000` (`http://127.0.0.1:5000`)
* **Modelo Conectado:** `ML/Ficheiro_IA/Register_IA.joblib`

### Especificação do Endpoint `/predict`
* **Método:** `POST`
* **Headers:** `Content-Type: application/json`
* **Payload de Entrada (Telemetria IoT):**
  ```json
  {
    "Temperatura_C": 78.5,
    "Vibracao_mms": 4.8,
    "Pressao_bar": 43.2
  }
  ```
* **Lógica de Inferência Operacional:** O valor gerado pela equação linear é submetido ao limiar de segurança de $0.5$ ($50\%$):
  * $\text{Score} < 0.5 \implies$ `"alerta": false`, `"risco_de_falha": "Não"`, `"status_operacional": "Normal"`.
  * $\text{Score} \ge 0.5 \implies$ `"alerta": true`, `"risco_de_falha": "Sim"`, `"status_operacional": "Crítico"`.
* **Payload de Retorno (Diagnóstico para CLP/SCADA):**
  ```json
  {
    "alerta": false,
    "risco_de_falha": "Não",
    "score_falha": 0.0755,
    "status_operacional": "Normal"
  }
  ```

---

## 5. Parecer Socioético e Regulatório

### 5.1. Impacto Sociolaboral: Transição e Valorização da Mão de Obra
A implantação de sistemas de visão computacional e predição algorítmica suscita preocupações sobre a substituição do trabalho humano na inspeção dimensional de qualidade:

1. **Requalificação Técnica (*Upskilling*):** A automação não deve ter como objetivo a eliminação sumária dos postos de trabalho dos inspetores de qualidade. Recomenda-se a condução de planos de capacitação interna para transformar os operadores de bancada em **Auditores de Sistemas Automatizados** e **Técnicos de Supervisão de Qualidade**, responsáveis pela calibração óptica das câmeras, auditoria por amostragem e parametrização dos limites de tolerância dos algoritmos.
2. **Abordagem *Human-in-the-Loop* (HITL):** A decisão algorítmica não deve ser adotada de forma cega em casos limítrofes. Casos onde o granulado de defeito se situe na faixa de incerteza (ex.: entre $0,8\%$ e $1,2\%$) devem ser automaticamente direcionados para uma estação de conferência assistida com operador humano qualificado.
3. **Ergonomia e Redução de Riscos à Saúde:** A substituição da inspeção visual exaustiva em bancadas com iluminação de alto contraste elimina causas frequentes de fadiga ocular crônica, cefaleias e lesões por esforço repetitivo (LER/DORT) decorrentes do manuseio contínuo de peças pesadas de ferro fundido.

### 5.2. Cibersegurança em Redes Industriais e Automação (TA / OT)
A disponibilização da API RESTful na rede corporativa conecta o ambiente analítico (TI) diretamente aos Controladores Lógicos Programáveis (CLPs) e redes operacionais (OT):

1. **Validação de Entrada e Blindagem de Endpoints:** A API deve rejeitar entradas anômalas ou fora dos limites físicos plausíveis da fábrica (ex.: temperaturas negativas extremas ou pressões impossíveis) a fim de frustrar tentativas de injeção de código, ataques de *Denial of Service* (DoS) ou ataques de envenenamento de inferência (*Evasion Attacks*).
2. **Segmentação de Redes Conforme ISA/IEC 62443:** A porta de serviço (`5000`) jamais deve estar aberta à rede corporativa externa ou internet. Deve-se isolar o servidor da API em uma DMZ industrial (*Demilitarized Zone*), permitindo tráfego apenas a partir dos endereços IP autenticados dos gateways de automação e CLPs.
3. **Criptografia e Autenticação Robusta:** O protocolo HTTP simples utilizado no protótipo de desenvolvimento deve ser migrado em ambiente produtivo para **HTTPS com TLS 1.3** e autenticação mútua via certificados digitais (mTLS) ou chaves secretas de API (*API Keys* com rotação periódica).

### 5.3. Conformidade com a LGPD (Lei nº 13.709/2018) no Monitoramento Óptico
A introdução de câmeras industriais de alta definição no galpão produtivo pode acidentalmente registrar imagens faciais, crachás ou comportamentos de operadores no entorno da esteira:

1. **Princípio da Necessidade e Adequação (Art. 6º, LGPD):** O tratamento de dados visuais deve limitar-se rigorosamente ao objeto da atividade fabril (a peça usinada). O enquadramento legal reside no **Legítimo Interesse** da empresa e na **Garantia da Segurança dos Processos**, sendo vedada a utilização dessas câmeras para fiscalização disciplinar ou vigilância comportamental de funcionários sem previsão explícita.
2. **Salvaguardas de *Privacy by Design*:**
   * **Enclausuramento Óptico Físico:** As câmeras devem ser instaladas dentro de cabines ópticas opacas ou túneis de iluminação fechados, focadas em plano fechado (*close-up*) na esteira, tornando fisicamente impossível a captura do rosto de operadores ou transeuntes.
   * **Filtros de Anonimização em Tempo Real:** Na hipótese de utilização de câmeras de plano aberto, o software deve conter rotinas obrigatórias de detecção facial para aplicação imediata de desfoque gaussiano (*Blurring*) antes da gravação de qualquer frame no disco.
3. **Minimização e Descarte de Metadados:** As imagens arquivadas de peças defeituosas para auditoria e retreinamento de modelos devem conter apenas carimbo de data, lote e número de série da peça, sendo proibido correlacionar os registros ao identificador pessoal do operador em turno.

---

## 6. Parecer Conclusivo
A solução desenvolvida para a MetalTech Soluções Industriais S.A. na Etapa 3 cumpre com rigor técnico os requisitos de:
* Processamento e detecção dimensional por visão computacional com mapeamento granular de danos;
* Exposição de serviço preditivo RESTful validado via requisições industriais JSON;
* Alinhamento ético e legal com as melhores práticas de cibersegurança e proteção de dados (LGPD).

Aprovado para homologação em bancada e testes de integração com os controladores de chão de fábrica.