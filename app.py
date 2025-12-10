from flask import Flask, jsonify, request, url_for

app = Flask(__name__)

# --- ROTA 1: HOME (Apenas para verificar se está online) ---
@app.route('/')
def home():
    return "WordMemorizer Activity Provider is Running!"

# --- ROTA 2: CONFIGURAÇÃO (Retorna o HTML do formulário) ---
# Ref: InvenRA-config.pdf [cite: 168, 183]
@app.route('/config', methods=['GET'])
def config_page():
    # Este HTML simula a interface onde o professor define o deck.
    # O campo 'deck_id' é o que a Inven!RA vai "ler" e salvar.
    html_content = """
    <!DOCTYPE html>
    <html>
    <head><title>Configurar WordMemorizer</title></head>
    <body>
        <h2>Configuração do Jogo de Memória</h2>
        <form>
            <label>Tema do Deck:</label><br>
            <input type="text" id="tema" name="tema" value="Cores em Alemão"><br><br>
            
            <label>Lista de Palavras do Deck:</label><br>
            <textarea id="palavras" rows="4" cols="50">Rot=Vermelho; Blau=Azul</textarea><br><br>
            
            <input type="hidden" name="deck_id" value="deck_123_exemplo">
            
            <p><em>(Simulação: Ao salvar, o ID 'deck_123_exemplo' será enviado à Inven!RA)</em></p>
        </form>
    </body>
    </html>
    """
    return html_content

# --- ROTA 3: PARÂMETROS JSON (Diz à Inven!RA o que ler do HTML) ---
# Ref: InvenRA-config.pdf [cite: 169, 206]
@app.route('/json-params', methods=['GET'])
def json_params():
    # Instrui a Inven!RA a procurar um campo chamado 'deck_id' no HTML acima
    return jsonify([
        {
            "name": "deck_id",
            "type": "text/plain"
        }
    ])

# --- ROTA 4: DEPLOY (Cria a instância e retorna a URL) ---
# Ref: InvenRA-config.pdf [cite: 170, 253]
@app.route('/deploy', methods=['GET', 'POST'])
def deploy_activity():
    # A Inven!RA chama isto para obter o link base da atividade.
    # Aqui retornamos uma URL fictícia para onde a Inven!RA enviará os alunos.
    # Num cenário real, você geraria um token único aqui.
    # Na Rota 4 (/deploy), você só retorna a URL genérica de entrada. Não se preocupe com o aluno.
    
    # Assumindo que o seu site está hospedado em 'meu-site.com':
    base_url = request.host_url.rstrip('/')  # Pega a URL do servidor atual
    activity_entry_point = f"{base_url}/game/entry"
    
    # Retorna APENAS a string da URL, conforme o exemplo do PDF [cite: 255]
    return activity_entry_point

# --- ROTA 5: LISTA DE ANALYTICS (O Contrato) ---
# Ref: InvenRA-config.pdf [cite: 173, 220]
@app.route('/analytics-list', methods=['GET'])
def analytics_list():
    # Lista as métricas que o seu jogo é capaz de medir.
    return jsonify({
        "quantAnalytics": [
            {"name": "tempo_jogado_total", "type": "integer"},
            {"name": "palavras_aprendidas", "type": "integer"},
            {"name": "percentual_acerto", "type": "integer"}
        ],
        "qualAnalytics": [
            {"name": "detalhes_sessao", "type": "text/plain"}
        ]
    })

# --- ROTA 6: DADOS DE ANALYTICS (Retorna os dados dos alunos) ---
# Ref: InvenRA-config.pdf [cite: 171, 270]
@app.route('/analytics-data', methods=['POST'])
def analytics_data():
    # A Inven!RA envia um POST com o ID da atividade.
    # Nós respondemos com dados FALSOS (Dummy Data) para teste.
    
    # Simulação de dados recebidos da Inven!RA (não usado agora, mas para constar)
    # data = request.get_json()
    # activity_id = data.get('activityID')

    return jsonify([
        {
            "inveniraStdID": "Student_A",
            "quantAnalytics": [
                {"name": "tempo_jogado_total", "type": "integer", "value": 120},
                {"name": "palavras_aprendidas", "type": "integer", "value": 15},
                {"name": "percentual_acerto", "type": "integer", "value": 85}
            ],
            "qualAnalytics": [
                {"name": "detalhes_sessao", "type": "text/plain", "value": "O aluno teve dificuldade com a cor 'Vermelho'."}
            ]
        },
        {
            "inveniraStdID": "Student_B",
            "quantAnalytics": [
                {"name": "tempo_jogado_total", "type": "integer", "value": 300},
                {"name": "palavras_aprendidas", "type": "integer", "value": 20},
                {"name": "percentual_acerto", "type": "integer", "value": 95}
            ],
            "qualAnalytics": [
                {"name": "detalhes_sessao", "type": "text/plain", "value": "Sessão concluída sem erros."}
            ]
        }
    ])

# --- ROTA EXTRA: ENTRADA DO JOGO (Simulação futura) ---
# A rota /deploy aponta para cá. Ainda não precisa funcionar
@app.route('/game/entry', methods=['GET', 'POST'])
def game_entry():
    # Aqui seria o ponto de entrada do jogo.
    # O JSON que a Inven!RA envia para a sua URL de entrada nesse momento será assim:
    # {
    #     "activityID": "instancia_123",
    #     "InvenRAstdID": "Student_A",  <-- O ID DO ALUNO ESTÁ AQUI
    #     "json_params": {
    #      "deck_id": "50"}
    # }   

    return "Aqui será o início do jogo (Provide Activity) - Implementar na próxima fase."

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)