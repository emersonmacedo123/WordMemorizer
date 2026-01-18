"""
Comandos concretos para operações do jogo

Cada comando encapsula uma operação específica do WordMemorizer,
incluindo todos os parâmetros necessários para sua execução.
"""

from .base_command import Command
from app.services.analytics_service import AnalyticsService


class SaveStudentProgressCommand(Command):
    """
    Comando para salvar o progresso de um estudante
    
    Encapsula a operação de persistir dados de uma sessão de jogo.
    """
    
    def __init__(self, analytics_service: AnalyticsService, activity_id: str, 
                 student_id: str, time_played: int, words_learned: int, feedback: str):
        super().__init__()
        self.analytics_service = analytics_service
        self.activity_id = activity_id
        self.student_id = student_id
        self.time_played = time_played
        self.words_learned = words_learned
        self.feedback = feedback
    
    def execute(self):
        """Executa o salvamento do progresso"""
        self.mark_executed()
        
        # Verifica se a turma existe no banco simulado
        if self.activity_id not in self.analytics_service.fake_database:
            self.analytics_service.fake_database[self.activity_id] = []
        
        # Adiciona ou atualiza o registro do estudante
        students = self.analytics_service.fake_database[self.activity_id]
        
        # Procura se o estudante já existe
        student_found = False
        for student in students:
            if student["student_id"] == self.student_id:
                # Atualiza dados existentes
                student["time"] = self.time_played
                student["words"] = self.words_learned
                student["note"] = self.feedback
                student_found = True
                break
        
        # Se não existe, cria novo registro
        if not student_found:
            students.append({
                "student_id": self.student_id,
                "time": self.time_played,
                "words": self.words_learned,
                "note": self.feedback
            })
        
        self.result = f"Progress saved for {self.student_id}"
        return {"success": True, "message": self.result}
    
    def get_description(self):
        return f"Save progress for student {self.student_id} in activity {self.activity_id}"


class RetrieveAnalyticsCommand(Command):
    """
    Comando para recuperar analytics de uma atividade
    
    Encapsula a operação de busca de dados analíticos.
    """
    
    def __init__(self, analytics_service: AnalyticsService, activity_id: str):
        super().__init__()
        self.analytics_service = analytics_service
        self.activity_id = activity_id
    
    def execute(self):
        """Executa a recuperação dos analytics"""
        self.mark_executed()
        
        analytics_data = self.analytics_service.get_analytics_for_activity(self.activity_id)
        self.result = f"Retrieved {len(analytics_data)} student records"
        
        return {
            "success": True,
            "data": analytics_data,
            "count": len(analytics_data)
        }
    
    def get_description(self):
        return f"Retrieve analytics for activity {self.activity_id}"


class UpdateStudentScoreCommand(Command):
    """
    Comando para atualizar apenas a pontuação de um estudante
    
    Útil para atualizações incrementais durante o jogo.
    """
    
    def __init__(self, analytics_service: AnalyticsService, activity_id: str, 
                 student_id: str, additional_words: int, additional_time: int):
        super().__init__()
        self.analytics_service = analytics_service
        self.activity_id = activity_id
        self.student_id = student_id
        self.additional_words = additional_words
        self.additional_time = additional_time
    
    def execute(self):
        """Executa a atualização incremental"""
        self.mark_executed()
        
        if self.activity_id not in self.analytics_service.fake_database:
            return {"success": False, "message": "Activity not found"}
        
        students = self.analytics_service.fake_database[self.activity_id]
        
        for student in students:
            if student["student_id"] == self.student_id:
                # Atualiza incrementalmente
                student["time"] += self.additional_time
                student["words"] += self.additional_words
                
                self.result = f"Updated score for {self.student_id}"
                return {
                    "success": True,
                    "message": self.result,
                    "new_totals": {
                        "time": student["time"],
                        "words": student["words"]
                    }
                }
        
        return {"success": False, "message": "Student not found"}
    
    def get_description(self):
        return f"Update score for {self.student_id}: +{self.additional_words} words, +{self.additional_time}s"


class ResetStudentProgressCommand(Command):
    """
    Comando para resetar o progresso de um estudante
    
    Útil para permitir que estudantes reiniciem o jogo.
    """
    
    def __init__(self, analytics_service: AnalyticsService, activity_id: str, student_id: str):
        super().__init__()
        self.analytics_service = analytics_service
        self.activity_id = activity_id
        self.student_id = student_id
        self.backup = None  # Para possível undo
    
    def execute(self):
        """Executa o reset do progresso"""
        self.mark_executed()
        
        if self.activity_id not in self.analytics_service.fake_database:
            return {"success": False, "message": "Activity not found"}
        
        students = self.analytics_service.fake_database[self.activity_id]
        
        for i, student in enumerate(students):
            if student["student_id"] == self.student_id:
                # Guarda backup para possível undo
                self.backup = student.copy()
                
                # Remove o estudante
                students.pop(i)
                
                self.result = f"Reset progress for {self.student_id}"
                return {"success": True, "message": self.result}
        
        return {"success": False, "message": "Student not found"}
    
    def undo(self):
        """
        Desfaz o reset (funcionalidade extra do Command)
        
        Returns:
            dict: Resultado da operação de undo
        """
        if self.backup is None:
            return {"success": False, "message": "No backup available"}
        
        if self.activity_id in self.analytics_service.fake_database:
            self.analytics_service.fake_database[self.activity_id].append(self.backup)
            return {"success": True, "message": "Progress restored"}
        
        return {"success": False, "message": "Activity not found"}
    
    def get_description(self):
        return f"Reset progress for student {self.student_id}"
