import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

# Importar configurações
from src.config import config

# Importar modelos e middleware
from src.models import db, init_db
from src.middleware import TenantMiddleware

# Importar blueprints
from src.routes.user import user_bp
from src.routes.auth import auth_bp
from src.routes.tenant import tenant_bp
from src.routes.public import public_bp
from src.routes.services import services_bp
from src.routes.staff import staff_bp
from src.routes.clients import clients_bp
from src.routes.appointments import appointments_bp
from src.routes.upload import upload_bp
from src.routes.customization import customization_bp

def create_app(config_name=None):
    """Factory function para criar a aplicação Flask"""
    
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    # Configurar pasta de arquivos estáticos
    static_folder = os.path.join(os.path.dirname(__file__), '..', 'static')
    app = Flask(__name__, static_folder=static_folder, static_url_path='/static')
    
    # Configurar Flask
    config_class = config[config_name]
    app.config.from_object(config_class)
    
    # Inicializar extensões
    db.init_app(app)
    CORS(app, origins=app.config['CORS_ORIGINS'])
    JWTManager(app)
    Migrate(app, db)
    
    # Inicializar middleware de tenant
    TenantMiddleware(app)
    
    # Registrar blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(tenant_bp, url_prefix='/api/tenant')
    app.register_blueprint(public_bp, url_prefix='/api/public')
    app.register_blueprint(services_bp, url_prefix='/api/services')
    app.register_blueprint(staff_bp, url_prefix='/api/staff')
    app.register_blueprint(clients_bp, url_prefix='/api/clients')
    app.register_blueprint(appointments_bp, url_prefix='/api/appointments')
    app.register_blueprint(upload_bp, url_prefix='/api/upload')
    app.register_blueprint(customization_bp, url_prefix='/api/customization')
    
    # Inicializar banco de dados
    with app.app_context():
        init_db(app)
    
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        """Servir arquivos estáticos e SPA"""
        static_folder_path = app.static_folder
        if static_folder_path is None:
            return "Static folder not configured", 404

        if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
            return send_from_directory(static_folder_path, path)
        else:
            index_path = os.path.join(static_folder_path, 'index.html')
            if os.path.exists(index_path):
                return send_from_directory(static_folder_path, 'index.html')
            else:
                return "index.html not found", 404
    
    @app.errorhandler(404)
    def not_found(error):
        return {"error": "Recurso não encontrado"}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return {"error": "Erro interno do servidor"}, 500
    
    @app.errorhandler(503)
    def service_unavailable(error):
        return {"error": "Serviço temporariamente indisponível"}, 503
    
    return app

# Criar instância da aplicação
app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
