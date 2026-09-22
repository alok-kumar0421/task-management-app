from flask import Blueprint, request, jsonify
from google.oauth2 import id_token
from google.auth.transport import requests
from services.supabase_service import supabase_service

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/google', methods=['POST'])
def google_auth():
    data = request.json
    token = data.get('token')
    
    if not token:
        return jsonify({'error': 'Token is missing'}), 400

    try:
        idinfo = id_token.verify_oauth2_token(token, requests.Request())
        
        google_id = idinfo['sub']
        email = idinfo['email']
        name = idinfo.get('name', '')
        picture = idinfo.get('picture', '')
        
        user = supabase_service.get_user_by_google_id(google_id)
        
        if not user:
            # Create new user
            user_data = {
                'google_id': google_id,
                'email': email,
                'name': name,
                'profile_picture': picture
            }
            user = supabase_service.create_user(user_data)
            
        return jsonify({'message': 'Login successful', 'user': user}), 200

    except ValueError as e:
        return jsonify({'error': 'Invalid token', 'details': str(e)}), 401
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500
