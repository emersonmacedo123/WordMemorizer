"""
Subsistema de Validação
Responsável por validar requisições da plataforma Inven!RA
Parte do padrão FACADE
"""

class ValidationSubsystem:
    """
    Subsistema que encapsula toda a lógica de validação 
    de dados recebidos da Inven!RA
    """
    
    @staticmethod
    def validate_analytics_request(data):
        """
        Valida se a requisição de analytics contém os dados necessários
        
        Args:
            data (dict): Dados recebidos no POST
            
        Returns:
            tuple: (is_valid, error_message, activity_id)
        """
        if not data:
            return False, "Bad Request: No data provided", None
            
        if 'activityID' not in data:
            return False, "Bad Request: activityID is missing", None
            
        activity_id = data['activityID']
        
        if not activity_id or not isinstance(activity_id, str):
            return False, "Bad Request: activityID must be a non-empty string", None
            
        return True, None, activity_id
    
    @staticmethod
    def validate_deploy_request(params):
        """
        Valida parâmetros para deploy da atividade
        
        Args:
            params (dict): Parâmetros recebidos
            
        Returns:
            tuple: (is_valid, error_message)
        """
        # Por enquanto, deploy não requer validação específica
        # Pode ser expandido futuramente
        return True, None
