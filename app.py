from flask import Flask, send_from_directory
from config.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import os
from flask_migrate import Migrate, migrate as flask_migrate, upgrade, init

# Inicializando extensões
db = SQLAlchemy()
jwt = JWTManager()
migrator = Migrate()

def run_migrations(app):
    """Executa as migrations automaticamente ao iniciar."""
    with app.app_context():
        migrations_folder = os.path.join(os.getcwd(), "migrations")

        if not os.path.exists(migrations_folder):
            print("[INFO] Criando diretório de migrations automaticamente...")
            init()

        print("[INFO] Gerando nova migration, se necessário...")
        flask_migrate(message="Automated migration")

        print("[INFO] Aplicando migrations ao banco de dados...")
        upgrade()
        print("[INFO] Migrations aplicadas com sucesso!")

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializando extensões
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)
    migrator.init_app(app, db)

    IMAGE_FOLDER = os.path.join(os.getcwd(), "uploads")

    @app.route('/uploads/<path:filename>')
    def serve_image(filename):
        return send_from_directory(IMAGE_FOLDER, filename)

    # Blueprints
    from flask_auth.routes import auth
    from controllers.post_controller import post_controller
    from controllers.comment_controller import comment_controller
    from controllers.user_controller import user_controller

    app.register_blueprint(auth, url_prefix="/api")
    app.register_blueprint(post_controller, url_prefix="/api/posts")
    app.register_blueprint(comment_controller, url_prefix="/api/comments")
    app.register_blueprint(user_controller, url_prefix="/api/user")

    run_migrations(app)

    return app

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_data):
    from models.models import RevokedToken
    jti = jwt_data["jti"]
    return RevokedToken.query.filter_by(jti=jti).first() is not None
