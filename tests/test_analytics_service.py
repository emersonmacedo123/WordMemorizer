"""
Exemplo de teste unitário para o serviço de analytics
"""
import unittest
from app.services.analytics_service import AnalyticsService

class TestAnalyticsService(unittest.TestCase):
    def setUp(self):
        self.service = AnalyticsService()
    
    def test_get_analytics_existing_activity(self):
        """Testa busca de analytics para atividade existente"""
        result = self.service.get_analytics_for_activity("instancia_turma_A")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["inveniraStdID"], "Student_Joao")
    
    def test_get_analytics_nonexistent_activity(self):
        """Testa busca de analytics para atividade inexistente"""
        result = self.service.get_analytics_for_activity("nao_existe")
        self.assertEqual(len(result), 0)

if __name__ == '__main__':
    unittest.main()
