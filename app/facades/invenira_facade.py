"""
PADRÃO DE ESTRUTURA: FACADE

Este módulo implementa o padrão Facade para simplificar a interface
com a plataforma Inven!RA, coordenando múltiplos subsistemas complexos.
"""

from app.services.analytics_subsystem import AnalyticsSubsystem
from app.services.config_subsystem import ConfigSubsystem
from app.services.validation_subsystem import ValidationSubsystem


class InveniraFacade:
    """
    FACADE - Ponto de entrada unificado para todas as operações relacionadas à Inven!RA
    
    Esta classe simplifica a interface complexa dos subsistemas (Analytics, Config, Validation),
    fornecendo métodos de alto nível que coordenam as operações necessárias.
    
    Benefícios:
    - Reduz acoplamento entre as rotas Flask e a lógica de negócio
    - Facilita testes (mock de uma única facade ao invés de múltiplos componentes)
    - Centraliza a coordenação entre subsistemas
    - Melhora legibilidade e manutenibilidade
    """
    
    def __init__(self):
        # Instancia os subsistemas que serão coordenados
        self.analytics = AnalyticsSubsystem()
        self.config = ConfigSubsystem()
        self.validator = ValidationSubsystem()
    
    # ========== OPERAÇÕES DE CONFIGURAÇÃO ==========
    
    def get_configuration_page(self):
        """
        Retorna a página HTML de configuração da atividade
        
        Returns:
            str: HTML da página de configuração
        """
        return self.config.get_config_page_html()
    
    def get_json_parameters(self):
        """
        Retorna os parâmetros que a Inven!RA deve capturar
        
        Returns:
            list: Lista de definições de parâmetros
        """
        return self.config.get_json_params()
    
    def get_analytics_list(self):
        """
        Retorna a lista de métricas disponíveis
        
        Returns:
            dict: Dicionário com métricas quantitativas e qualitativas
        """
        return self.config.get_analytics_definitions()
    
    # ========== OPERAÇÕES DE DEPLOY ==========
    
    def get_game_entry_url(self, base_url):
        """
        Retorna a URL de entrada do jogo
        
        Args:
            base_url (str): URL base da aplicação
            
        Returns:
            str: URL completa para iniciar o jogo
        """
        clean_url = base_url.rstrip('/')
        return self.config.get_game_entry_url(clean_url)
    
    # ========== OPERAÇÕES DE ANALYTICS ==========
    
    def handle_analytics_request(self, request_data):
        """
        Processa uma requisição de analytics de forma completa
        
        Este método coordena:
        1. Validação dos dados recebidos
        2. Busca dos dados de analytics
        3. Formatação da resposta
        
        Args:
            request_data (dict): Dados recebidos no POST da Inven!RA
            
        Returns:
            tuple: (success, data_or_error, status_code)
                - success (bool): Se a operação foi bem-sucedida
                - data_or_error: Lista de analytics ou mensagem de erro
                - status_code (int): Código HTTP apropriado
        """
        # 1. VALIDAÇÃO
        is_valid, error_msg, activity_id = self.validator.validate_analytics_request(request_data)
        
        if not is_valid:
            return False, {"error": error_msg}, 400
        
        # 2. BUSCA E PROCESSAMENTO
        print(f"--> [FACADE] Processando analytics para: {activity_id}")
        analytics_data = self.analytics.get_analytics_for_activity(activity_id)
        
        # 3. RESPOSTA FORMATADA
        return True, analytics_data, 200
