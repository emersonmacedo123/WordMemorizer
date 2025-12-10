from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Registrar blueprints (rotas)
    from app.routes import invenra_routes, game_routes
    app.register_blueprint(invenra_routes.bp)
    app.register_blueprint(game_routes.bp)
    
    return app
