"""
Serviço responsável pela lógica de analytics
Simula um banco de dados e processa os dados dos alunos
"""
from app.models.metrics import MetricFactory

class AnalyticsService:
    def __init__(self):
        # Simulação de Banco de Dados Multi-Turma
        self.fake_database = {
            "instancia_turma_A": [
                {"student_id": "Student_Joao", "time": 120, "words": 15, "note": "Bom começo"},
                {"student_id": "Student_Maria", "time": 300, "words": 50, "note": "Excelente"}
            ],
            "instancia_turma_B": [
                {"student_id": "Student_Pedro", "time": 10, "words": 0, "note": "Desistiu"},
                {"student_id": "Student_Ana", "time": 400, "words": 45, "note": "Muito dedicada"}
            ]
        }

    def get_analytics_for_activity(self, activity_id):
        """
        Busca e processa os dados de analytics para uma atividade específica
        """
        # Busca os dados brutos baseados no ID recebido
        class_raw_data = self.fake_database.get(activity_id, [])
        
        response_list = []
        
        # Processamento com Factory Method
        for student in class_raw_data:
            # Criação das métricas usando a Fábrica
            metric_time = MetricFactory.create_metric("quant", "tempo_jogado", student["time"])
            metric_words = MetricFactory.create_metric("quant", "palavras_aprendidas", student["words"])
            metric_feedback = MetricFactory.create_metric("qual", "feedback_professor", student["note"])

            # Montagem do objeto do aluno
            student_response = {
                "inveniraStdID": student["student_id"],
                "quantAnalytics": [
                    metric_time.to_json(),
                    metric_words.to_json()
                ],
                "qualAnalytics": [
                    metric_feedback.to_json()
                ]
            }
            response_list.append(student_response)
        
        return response_list
