# Interface base do padrão Command: Define o contrato que todos os comandos concretos devem seguir.

from abc import ABC, abstractmethod
from datetime import datetime


class Command(ABC):
    """
    Interface Command - Define a operação execute()
    
    Todos os comandos concretos implementam esta interface,
    encapsulando uma ação específica e seus parâmetros.
    """
    
    def __init__(self):
        self.executed_at = None
        self.result = None
    
    @abstractmethod
    def execute(self):
        """
        Executa a operação encapsulada pelo comando
        
        Returns:
            Resultado da operação (varia por comando)
        """
        pass
    
    @abstractmethod
    def get_description(self):
        """
        Retorna uma descrição legível do comando
        
        Returns:
            str: Descrição do comando
        """
        pass
    
    def mark_executed(self):
        """Marca o timestamp de execução"""
        self.executed_at = datetime.now()
    
    def get_log_entry(self):
        """
        Retorna entrada para log de histórico
        
        Returns:
            dict: Informações sobre a execução do comando
        """
        return {
            "command": self.__class__.__name__,
            "description": self.get_description(),
            "executed_at": self.executed_at.isoformat() if self.executed_at else None,
            "result": str(self.result) if self.result else None
        }
