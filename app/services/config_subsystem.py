"""
Subsistema de Configuração
Responsável por gerenciar configurações e metadados da atividade
Parte do padrão FACADE
"""

class ConfigSubsystem:
    """
    Subsistema que encapsula a lógica de configuração 
    da atividade e seus metadados
    """
    
    def __init__(self):
        self.activity_name = "WordMemorizer Game"
        self.default_deck = "deck_123_exemplo"
        
    def get_config_page_html(self):
        """
        Retorna o HTML da página de configuração
        
        Returns:
            str: HTML da página de configuração
        """
        return f"""
        <!DOCTYPE html>
        <html><body>
        <h2>Configuração do {self.activity_name}</h2>
        <form>
            <label>Tema do Deck:</label><br>
            <input type="text" id="tema" name="tema" value="Cores em Alemão"><br><br>
            
            <input type="hidden" name="deck_id" value="{self.default_deck}">
            
            <p><em>(Ao salvar, o ID '{self.default_deck}' será enviado à Inven!RA)</em></p>
        </form>
        </body></html>
        """
    
    def get_json_params(self):
        """
        Define os parâmetros que a Inven!RA deve capturar
        
        Returns:
            list: Lista de parâmetros
        """
        return [
            {"name": "deck_id", "type": "text/plain"}
        ]
    
    def get_analytics_definitions(self):
        """
        Define as métricas disponíveis para analytics
        
        Returns:
            dict: Definição das métricas quantitativas e qualitativas
        """
        return {
            "quantAnalytics": [
                {"name": "tempo_jogado", "type": "integer"},
                {"name": "palavras_aprendidas", "type": "integer"}
            ],
            "qualAnalytics": [
                {"name": "feedback_professor", "type": "text/plain"}
            ]
        }
    
    def get_game_entry_url(self, base_url):
        """
        Constrói a URL de entrada do jogo
        
        Args:
            base_url (str): URL base da aplicação
            
        Returns:
            str: URL completa para entrada do jogo
        """
        return f"{base_url}/game/entry"
