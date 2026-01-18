"""
PADRÃO DE COMPORTAMENTO: COMMAND

Este módulo implementa o padrão Command para encapsular operações
do jogo como objetos independentes, permitindo:
- Enfileiramento de operações
- Histórico de ações (logging)
- Desfazer/refazer operações
- Parametrização de requisições
"""

from .base_command import Command
from .game_commands import (
    SaveStudentProgressCommand,
    RetrieveAnalyticsCommand,
    UpdateStudentScoreCommand,
    ResetStudentProgressCommand
)
from .command_invoker import CommandInvoker

__all__ = [
    'Command',
    'SaveStudentProgressCommand',
    'RetrieveAnalyticsCommand',
    'UpdateStudentScoreCommand',
    'ResetStudentProgressCommand',
    'CommandInvoker'
]
