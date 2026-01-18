"""
Invoker do padrão Command

Responsável por executar comandos e manter histórico de operações.
"""

from typing import List
from .base_command import Command


class CommandInvoker:
    """
    INVOKER - Gerencia a execução de comandos
    
    Responsabilidades:
    - Executar comandos
    - Manter histórico de comandos executados
    - Permitir replay de operações
    - Fornecer logs de auditoria
    
    Benefícios:
    - Desacopla quem solicita a operação de quem a executa
    - Permite logging automático de todas as operações
    - Facilita debugging e auditoria
    - Possibilita implementar filas de comandos
    """
    
    def __init__(self):
        self.history: List[Command] = []
        self.max_history_size = 100  # Limita o tamanho do histórico
    
    def execute_command(self, command: Command):
        """
        Executa um comando e adiciona ao histórico
        
        Args:
            command (Command): O comando a ser executado
            
        Returns:
            Resultado da execução do comando
        """
        result = command.execute()
        
        # Adiciona ao histórico
        self.history.append(command)
        
        # Mantém o histórico dentro do limite
        if len(self.history) > self.max_history_size:
            self.history.pop(0)
        
        return result
    
    def get_history(self, limit: int = None):
        """
        Retorna o histórico de comandos executados
        
        Args:
            limit (int, optional): Número máximo de entradas a retornar
            
        Returns:
            list: Lista de entradas de log dos comandos
        """
        history_to_return = self.history if limit is None else self.history[-limit:]
        return [cmd.get_log_entry() for cmd in history_to_return]
    
    def get_last_command(self):
        """
        Retorna o último comando executado
        
        Returns:
            Command ou None: O último comando ou None se o histórico está vazio
        """
        return self.history[-1] if self.history else None
    
    def clear_history(self):
        """Limpa o histórico de comandos"""
        self.history.clear()
        
    def replay_commands(self, start_index: int = 0, end_index: int = None):
        """
        Reexecuta comandos do histórico
        Args:
            start_index (int): Índice inicial (inclusivo)
            end_index (int, optional): Índice final (exclusivo)
            
        Returns:
            list: Resultados das re-execuções
        """
        end = end_index if end_index is not None else len(self.history)
        commands_to_replay = self.history[start_index:end]
        
        results = []
        for cmd in commands_to_replay:
            result = cmd.execute()
            results.append({
                "command": cmd.get_description(),
                "result": result
            })
        
        return results
