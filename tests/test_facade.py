"""
Testes para o padrão FACADE - InveniraFacade
Demonstra como o padrão simplifica os testes
"""
import unittest
from app.facades.invenira_facade import InveniraFacade


class TestInveniraFacade(unittest.TestCase):
    """Testes da Facade - interface simplificada"""
    
    def setUp(self):
        """Inicializa a Facade para cada teste"""
        self.facade = InveniraFacade()
    
    # ========== TESTES DE CONFIGURAÇÃO ==========
    
    def test_get_configuration_page(self):
        """Testa se retorna HTML da página de configuração"""
        html = self.facade.get_configuration_page()
        self.assertIn("WordMemorizer", html)
        self.assertIn("deck_id", html)
    
    def test_get_json_parameters(self):
        """Testa se retorna os parâmetros corretos"""
        params = self.facade.get_json_parameters()
        self.assertEqual(len(params), 1)
        self.assertEqual(params[0]["name"], "deck_id")
    
    def test_get_analytics_list(self):
        """Testa se retorna as definições de métricas"""
        definitions = self.facade.get_analytics_list()
        self.assertIn("quantAnalytics", definitions)
        self.assertIn("qualAnalytics", definitions)
        self.assertEqual(len(definitions["quantAnalytics"]), 2)
    
    # ========== TESTES DE DEPLOY ==========
    
    def test_get_game_entry_url(self):
        """Testa se constrói a URL de entrada corretamente"""
        base_url = "https://wordmemorizer.onrender.com/"
        entry_url = self.facade.get_game_entry_url(base_url)
        self.assertEqual(entry_url, "https://wordmemorizer.onrender.com/game/entry")
    
    def test_get_game_entry_url_without_trailing_slash(self):
        """Testa URL sem barra final"""
        base_url = "https://wordmemorizer.onrender.com"
        entry_url = self.facade.get_game_entry_url(base_url)
        self.assertEqual(entry_url, "https://wordmemorizer.onrender.com/game/entry")
    
    # ========== TESTES DE ANALYTICS (COM VALIDAÇÃO) ==========
    
    def test_handle_analytics_request_success(self):
        """Testa requisição válida de analytics"""
        request_data = {"activityID": "instancia_turma_A"}
        
        success, result, status = self.facade.handle_analytics_request(request_data)
        
        self.assertTrue(success)
        self.assertEqual(status, 200)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["inveniraStdID"], "Student_Joao")
    
    def test_handle_analytics_request_missing_data(self):
        """Testa requisição sem dados"""
        request_data = None
        
        success, result, status = self.facade.handle_analytics_request(request_data)
        
        self.assertFalse(success)
        self.assertEqual(status, 400)
        self.assertIn("error", result)
    
    def test_handle_analytics_request_missing_activity_id(self):
        """Testa requisição sem activityID"""
        request_data = {"outro_campo": "valor"}
        
        success, result, status = self.facade.handle_analytics_request(request_data)
        
        self.assertFalse(success)
        self.assertEqual(status, 400)
        self.assertIn("activityID", result["error"])
    
    def test_handle_analytics_request_nonexistent_activity(self):
        """Testa busca de atividade inexistente"""
        request_data = {"activityID": "turma_inexistente"}
        
        success, result, status = self.facade.handle_analytics_request(request_data)
        
        self.assertTrue(success)  # Requisição válida, mas sem dados
        self.assertEqual(status, 200)
        self.assertEqual(len(result), 0)  # Lista vazia


class TestSubsystemsIntegration(unittest.TestCase):
    """Testes de integração entre subsistemas via Facade"""
    
    def setUp(self):
        self.facade = InveniraFacade()
    
    def test_facade_coordinates_all_subsystems(self):
        """Verifica que a Facade coordena todos os subsistemas corretamente"""
        # Testa subsistema de Config
        config_html = self.facade.get_configuration_page()
        self.assertIsNotNone(config_html)
        
        # Testa subsistema de Validation + Analytics
        valid_request = {"activityID": "instancia_turma_B"}
        success, data, _ = self.facade.handle_analytics_request(valid_request)
        self.assertTrue(success)
        self.assertEqual(len(data), 2)
        
        # Verifica dados específicos do Analytics
        self.assertEqual(data[0]["inveniraStdID"], "Student_Pedro")
        self.assertEqual(data[1]["inveniraStdID"], "Student_Ana")


if __name__ == '__main__':
    unittest.main()
