"""
Testes para o padrão Command

Valida o funcionamento dos comandos e do invoker.
"""

import unittest
from app.services.analytics_service import AnalyticsService
from app.commands import (
    SaveStudentProgressCommand,
    RetrieveAnalyticsCommand,
    UpdateStudentScoreCommand,
    ResetStudentProgressCommand,
    CommandInvoker
)


class TestCommandPattern(unittest.TestCase):
    """Testes para o padrão de comportamento Command"""
    
    def setUp(self):
        """Configuração antes de cada teste"""
        self.analytics_service = AnalyticsService()
        self.invoker = CommandInvoker()
        
        # Limpa dados de teste
        if "test_activity" in self.analytics_service.fake_database:
            del self.analytics_service.fake_database["test_activity"]
    
    def test_save_progress_command(self):
        """Testa o comando de salvar progresso"""
        command = SaveStudentProgressCommand(
            analytics_service=self.analytics_service,
            activity_id="test_activity",
            student_id="Student_Test",
            time_played=100,
            words_learned=10,
            feedback="Test feedback"
        )
        
        result = self.invoker.execute_command(command)
        
        self.assertTrue(result['success'])
        self.assertIn("test_activity", self.analytics_service.fake_database)
        
        # Verifica se o estudante foi salvo
        students = self.analytics_service.fake_database["test_activity"]
        self.assertEqual(len(students), 1)
        self.assertEqual(students[0]["student_id"], "Student_Test")
        self.assertEqual(students[0]["time"], 100)
        self.assertEqual(students[0]["words"], 10)
    
    def test_retrieve_analytics_command(self):
        """Testa o comando de recuperar analytics"""
        # Primeiro salva alguns dados
        save_cmd = SaveStudentProgressCommand(
            analytics_service=self.analytics_service,
            activity_id="test_activity",
            student_id="Student_A",
            time_played=50,
            words_learned=5,
            feedback="Good"
        )
        self.invoker.execute_command(save_cmd)
        
        # Agora recupera
        retrieve_cmd = RetrieveAnalyticsCommand(
            analytics_service=self.analytics_service,
            activity_id="test_activity"
        )
        
        result = self.invoker.execute_command(retrieve_cmd)
        
        self.assertTrue(result['success'])
        self.assertEqual(result['count'], 1)
        self.assertIsInstance(result['data'], list)
    
    def test_update_score_command(self):
        """Testa o comando de atualização incremental"""
        # Primeiro salva um progresso inicial
        save_cmd = SaveStudentProgressCommand(
            analytics_service=self.analytics_service,
            activity_id="test_activity",
            student_id="Student_B",
            time_played=100,
            words_learned=10,
            feedback="Initial"
        )
        self.invoker.execute_command(save_cmd)
        
        # Atualiza incrementalmente
        update_cmd = UpdateStudentScoreCommand(
            analytics_service=self.analytics_service,
            activity_id="test_activity",
            student_id="Student_B",
            additional_words=5,
            additional_time=30
        )
        
        result = self.invoker.execute_command(update_cmd)
        
        self.assertTrue(result['success'])
        self.assertEqual(result['new_totals']['time'], 130)
        self.assertEqual(result['new_totals']['words'], 15)
    
    def test_reset_progress_command(self):
        """Testa o comando de reset de progresso"""
        # Salva progresso
        save_cmd = SaveStudentProgressCommand(
            analytics_service=self.analytics_service,
            activity_id="test_activity",
            student_id="Student_C",
            time_played=200,
            words_learned=20,
            feedback="To be reset"
        )
        self.invoker.execute_command(save_cmd)
        
        # Verifica que existe
        students_before = len(self.analytics_service.fake_database["test_activity"])
        self.assertEqual(students_before, 1)
        
        # Reseta
        reset_cmd = ResetStudentProgressCommand(
            analytics_service=self.analytics_service,
            activity_id="test_activity",
            student_id="Student_C"
        )
        
        result = self.invoker.execute_command(reset_cmd)
        
        self.assertTrue(result['success'])
        
        # Verifica que foi removido
        students_after = len(self.analytics_service.fake_database["test_activity"])
        self.assertEqual(students_after, 0)
    
    def test_command_undo(self):
        """Testa a funcionalidade de undo do comando de reset"""
        # Salva progresso
        save_cmd = SaveStudentProgressCommand(
            analytics_service=self.analytics_service,
            activity_id="test_activity",
            student_id="Student_D",
            time_played=150,
            words_learned=15,
            feedback="Test undo"
        )
        self.invoker.execute_command(save_cmd)
        
        # Reseta
        reset_cmd = ResetStudentProgressCommand(
            analytics_service=self.analytics_service,
            activity_id="test_activity",
            student_id="Student_D"
        )
        self.invoker.execute_command(reset_cmd)
        
        # Verifica que foi removido
        self.assertEqual(len(self.analytics_service.fake_database["test_activity"]), 0)
        
        # Desfaz o reset
        undo_result = reset_cmd.undo()
        
        self.assertTrue(undo_result['success'])
        
        # Verifica que foi restaurado
        students = self.analytics_service.fake_database["test_activity"]
        self.assertEqual(len(students), 1)
        self.assertEqual(students[0]["student_id"], "Student_D")
    
    def test_invoker_history(self):
        """Testa o histórico do invoker"""
        # Executa alguns comandos
        cmd1 = SaveStudentProgressCommand(
            self.analytics_service, "test_activity", "S1", 10, 1, "A"
        )
        cmd2 = SaveStudentProgressCommand(
            self.analytics_service, "test_activity", "S2", 20, 2, "B"
        )
        
        self.invoker.execute_command(cmd1)
        self.invoker.execute_command(cmd2)
        
        # Verifica histórico
        history = self.invoker.get_history()
        self.assertEqual(len(history), 2)
        
        # Verifica que cada entrada tem os campos esperados
        for entry in history:
            self.assertIn('command', entry)
            self.assertIn('description', entry)
            self.assertIn('executed_at', entry)
    
    def test_command_description(self):
        """Testa se os comandos retornam descrições legíveis"""
        command = SaveStudentProgressCommand(
            self.analytics_service,
            "activity_123",
            "Student_X",
            100,
            10,
            "Test"
        )
        
        description = command.get_description()
        
        self.assertIsInstance(description, str)
        self.assertIn("Student_X", description)
        self.assertIn("activity_123", description)


if __name__ == '__main__':
    unittest.main()
