"""
Rotas relacionadas ao jogo em si

PADRÃO DE COMPORTAMENTO: COMMAND
Este módulo demonstra o uso do padrão Command para operações do jogo.
"""
from flask import Blueprint, request, jsonify
from app.services.analytics_service import AnalyticsService
from app.commands import (
    SaveStudentProgressCommand,
    RetrieveAnalyticsCommand,
    UpdateStudentScoreCommand,
    ResetStudentProgressCommand,
    CommandInvoker
)

bp = Blueprint('game', __name__, url_prefix='/game')

# Instancia global do invoker para manter histórico durante a sessão
game_invoker = CommandInvoker()
analytics_service = AnalyticsService()

@bp.route('/entry', methods=['GET', 'POST'])
def game_entry():
    """
    Ponto de entrada do jogo
    Aqui a Inven!RA envia o aluno para jogar
    """
    return "Aqui será o início do jogo - Implementar na próxima fase."


# ========== ENDPOINTS DEMONSTRANDO O PADRÃO COMMAND ==========

@bp.route('/save-progress', methods=['POST'])
def save_progress():
    """
    Salva o progresso de um estudante usando o padrão Command
    
    Esperado no body:
    {
        "activity_id": "instancia_turma_A",
        "student_id": "Student_Carlos",
        "time_played": 180,
        "words_learned": 25,
        "feedback": "Progredindo bem"
    }
    """
    data = request.get_json()
    
    # Cria o comando com todos os parâmetros
    command = SaveStudentProgressCommand(
        analytics_service=analytics_service,
        activity_id=data.get('activity_id'),
        student_id=data.get('student_id'),
        time_played=data.get('time_played', 0),
        words_learned=data.get('words_learned', 0),
        feedback=data.get('feedback', '')
    )
    
    # Executa o comando através do invoker
    result = game_invoker.execute_command(command)
    
    return jsonify(result), 200 if result['success'] else 400


@bp.route('/get-progress/<activity_id>', methods=['GET'])
def get_progress(activity_id):
    """
    Recupera o progresso de uma turma usando o padrão Command
    
    URL: /game/get-progress/instancia_turma_A
    """
    # Cria o comando de recuperação
    command = RetrieveAnalyticsCommand(
        analytics_service=analytics_service,
        activity_id=activity_id
    )
    
    # Executa através do invoker
    result = game_invoker.execute_command(command)
    
    return jsonify(result), 200


@bp.route('/update-score', methods=['POST'])
def update_score():
    """
    Atualiza incrementalmente a pontuação de um estudante
    
    Esperado no body:
    {
        "activity_id": "instancia_turma_A",
        "student_id": "Student_Joao",
        "additional_words": 5,
        "additional_time": 30
    }
    """
    data = request.get_json()
    
    command = UpdateStudentScoreCommand(
        analytics_service=analytics_service,
        activity_id=data.get('activity_id'),
        student_id=data.get('student_id'),
        additional_words=data.get('additional_words', 0),
        additional_time=data.get('additional_time', 0)
    )
    
    result = game_invoker.execute_command(command)
    
    return jsonify(result), 200 if result['success'] else 404


@bp.route('/reset-progress', methods=['POST'])
def reset_progress():
    """
    Reseta o progresso de um estudante
    
    Esperado no body:
    {
        "activity_id": "instancia_turma_A",
        "student_id": "Student_Maria"
    }
    """
    data = request.get_json()
    
    command = ResetStudentProgressCommand(
        analytics_service=analytics_service,
        activity_id=data.get('activity_id'),
        student_id=data.get('student_id')
    )
    
    result = game_invoker.execute_command(command)
    
    return jsonify(result), 200 if result['success'] else 404


@bp.route('/command-history', methods=['GET'])
def command_history():
    """
    Retorna o histórico de comandos executados
    
    Query params:
    - limit: número de comandos a retornar (padrão: todos)
    """
    limit = request.args.get('limit', type=int)
    history = game_invoker.get_history(limit=limit)
    
    return jsonify({
        "history": history,
        "count": len(history)
    }), 200
