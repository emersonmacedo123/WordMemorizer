"""
Rotas relacionadas à integração com Inven!RA
"""
from flask import Blueprint, jsonify, request
from app.services.analytics_service import AnalyticsService

bp = Blueprint('invenra', __name__)

# Instância do serviço de analytics
analytics_service = AnalyticsService()

@bp.route('/')
def home():
    return "WordMemorizer Activity Provider is Running!"

@bp.route('/config', methods=['GET'])
def config_page():
    """
    Página de configuração da atividade
    """
    return """
    <!DOCTYPE html>
    <html><body>
    <h2>Configuração do WordMemorizer</h2>
    <form>
        <label>Tema do Deck:</label><br>
        <input type="text" id="tema" name="tema" value="Cores em Alemão"><br><br>
        
        <input type="hidden" name="deck_id" value="deck_123_exemplo">
        
        <p><em>(Ao salvar, o ID 'deck_123_exemplo' será enviado à Inven!RA)</em></p>
    </form>
    </body></html>
    """

@bp.route('/json-params', methods=['GET'])
def json_params():
    """
    Define quais parâmetros a Inven!RA deve ler
    """
    return jsonify([
        {"name": "deck_id", "type": "text/plain"}
    ])

@bp.route('/deploy', methods=['GET', 'POST'])
def deploy_activity():
    """
    Retorna a URL de entrada da atividade para a Inven!RA
    """
    base_url = request.host_url.rstrip('/')
    return f"{base_url}/game/entry"

@bp.route('/analytics-list', methods=['GET'])
def analytics_list():
    """
    Lista as métricas disponíveis
    """
    return jsonify({
        "quantAnalytics": [
            {"name": "tempo_jogado", "type": "integer"},
            {"name": "palavras_aprendidas", "type": "integer"}
        ],
        "qualAnalytics": [
            {"name": "feedback_professor", "type": "text/plain"}
        ]
    })

@bp.route('/analytics-data', methods=['POST'])
def analytics_data():
    """
    Retorna os dados de analytics para uma atividade
    """
    # Captura os dados enviados pela Inven!RA
    data = request.get_json()
    
    # Validação básica
    if not data or 'activityID' not in data:
        return jsonify({"error": "Bad Request: activityID is missing"}), 400
        
    activity_id = data['activityID']
    print(f"--> Recebido pedido de analytics para a atividade: {activity_id}")

    # Usa o serviço para buscar e processar os dados
    response_list = analytics_service.get_analytics_for_activity(activity_id)
    
    return jsonify(response_list)
