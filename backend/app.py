from flask import Flask, jsonify
from flask_cors import CORS
from config import Config

# Import Blueprints
from routes.auth import auth_bp
from routes.users import users_bp
from routes.tasks import tasks_bp

def create_app():
    app = Flask(__name__)
    
    CORS(app)
    
    # Register routes
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(tasks_bp, url_prefix='/tasks')
    
    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({'status': 'healthy', 'message': 'API is running'}), 200
        
    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=Config.PORT, debug=True)
