from flask import Blueprint, jsonify
from services.supabase_service import supabase_service

users_bp = Blueprint('users', __name__)

@users_bp.route('/', methods=['GET'])
def get_users():
    try:
        users = supabase_service.get_all_users()
        return jsonify({'users': users}), 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch users', 'details': str(e)}), 500
