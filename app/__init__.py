from flask import Flask

def create_app():
    app = Flask(__name__)
    app.secret_key = "super-secret-key"  # You can replace this with a .env variable later

    # Import and register blueprints
    from app.routes import user,admin
    app.register_blueprint(user.user_bp)
    app.register_blueprint(admin.admin_bp)
    return app
