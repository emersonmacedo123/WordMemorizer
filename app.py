"""
Arquivo de compatibilidade para deploy no Render
Importa a aplicação Flask da estrutura organizada
"""
from run import app

# Este arquivo serve como ponte para o Render/Gunicorn
# que espera encontrar um objeto 'app' em app.py

# Para executar localmente: python run.py
# Para Gunicorn (Render): gunicorn app:app