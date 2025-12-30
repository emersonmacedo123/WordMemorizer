"""
Rotas relacionadas à integração com Inven!RA
Utiliza o padrão FACADE para simplificar a interface
"""
from flask import Blueprint, jsonify, request
from app.facades.invenira_facade import InveniraFacade

bp = Blueprint('invenra', __name__)

# Instância da FACADE - ponto único de entrada para operações Inven!RA
invenira_facade = InveniraFacade()

@bp.route('/')
def home():
    return "WordMemorizer Activity Provider is Running!"

@bp.route('/config', methods=['GET'])
def config_page():
    """
    Página de configuração da atividade
    Delegada à Facade
    """
    return invenira_facade.get_configuration_page()

@bp.route('/json-params', methods=['GET'])
def json_params():
    """
    Define quais parâmetros a Inven!RA deve ler
    Delegada à Facade
    """
    return jsonify(invenira_facade.get_json_parameters())

@bp.route('/deploy', methods=['GET', 'POST'])
def deploy_activity():
    """
    Retorna a URL de entrada da atividade para a Inven!RA
    Delegada à Facade
    """
    base_url = request.host_url
    return invenira_facade.get_game_entry_url(base_url)

@bp.route('/analytics-list', methods=['GET'])
def analytics_list():
    """
    Lista as métricas disponíveis
    Delegada à Facade
    """
    return jsonify(invenira_facade.get_analytics_list())

@bp.route('/analytics-data', methods=['POST'])
def analytics_data():
    """
    Retorna os dados de analytics para uma atividade
    Delegada à Facade - toda a lógica de validação e processamento está encapsulada
    """
    # Captura os dados enviados pela Inven!RA
    data = request.get_json()
    
    # A Facade coordena: validação + busca + processamento
    success, result, status_code = invenira_facade.handle_analytics_request(data)
    
    return jsonify(result), status_code
