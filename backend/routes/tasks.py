from flask import Blueprint, request, jsonify
from services.supabase_service import supabase_service
from services.gmail_service import gmail_service

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/', methods=['GET'])
def get_tasks():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400
        
    try:
        tasks = supabase_service.get_tasks_for_user(user_id)
        return jsonify({'tasks': tasks}), 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch tasks', 'details': str(e)}), 500

@tasks_bp.route('/', methods=['POST'])
def create_task():
    data = request.json
    title = data.get('title')
    description = data.get('description')
    assigned_to = data.get('assigned_to')
    created_by = data.get('created_by')
    
    if not all([title, description, assigned_to, created_by]):
        return jsonify({'error': 'Missing required fields'}), 400
        
    try:
        task_data = {
            'title': title,
            'description': description,
            'assigned_to': assigned_to,
            'created_by': created_by,
            'status': 'Pending'
        }
        task = supabase_service.create_task(task_data)
        
        # Send email to the assigned user
        assigned_user = supabase_service.get_user_by_id(assigned_to)
        creator_user = supabase_service.get_user_by_id(created_by)
        
        if assigned_user and creator_user:
            subject = "New Task Assigned"
            body = f"You have been assigned a new task.\n\nTask: {title}\nDescription: {description}\nAssigned by: {creator_user['name']}"
            gmail_service.send_email(assigned_user['email'], subject, body)
            
        return jsonify({'message': 'Task created successfully', 'task': task}), 201
    except Exception as e:
        return jsonify({'error': 'Failed to create task', 'details': str(e)}), 500

@tasks_bp.route('/<task_id>/complete', methods=['PATCH'])
def complete_task(task_id):
    data = request.json
    user_id = data.get('user_id')
    
    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400
        
    try:
        task = supabase_service.get_task_by_id(task_id)
        if not task:
            return jsonify({'error': 'Task not found'}), 404
            
        if str(task['assigned_to']) != str(user_id):
            return jsonify({'error': 'Unauthorized: Only the assigned user can complete this task'}), 403

        updated_task = supabase_service.update_task_status(task_id, 'Completed')
        
        creator_user = supabase_service.get_user_by_id(task['created_by'])
        assigned_user = supabase_service.get_user_by_id(task['assigned_to'])
        
        if creator_user and assigned_user:
            subject = "Task Completed"
            body = f"Your task has been completed.\n\nTask: {task['title']}\nCompleted by: {assigned_user['name']}"
            gmail_service.send_email(creator_user['email'], subject, body)
            
        return jsonify({'message': 'Task completed successfully', 'task': updated_task}), 200
    except Exception as e:
        return jsonify({'error': 'Failed to complete task', 'details': str(e)}), 500
