"""
Rotas relacionadas ao jogo em si
"""
from flask import Blueprint

bp = Blueprint('game', __name__, url_prefix='/game')

@bp.route('/entry', methods=['GET', 'POST'])
def game_entry():
    """
    Ponto de entrada do jogo
    Aqui a Inven!RA envia o aluno para jogar
    """
    return "Aqui será o início do jogo - Implementar na próxima fase."
