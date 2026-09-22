from supabase import create_client, Client
from config import Config

class SupabaseService:
    def __init__(self):
        if not Config.SUPABASE_URL or not Config.SUPABASE_KEY:
            self.client = None
            print("WARNING: Supabase URL or Key is missing.")
        else:
            self.client: Client = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)
    
    def get_user_by_google_id(self, google_id):
        response = self.client.table('users').select('*').eq('google_id', google_id).execute()
        return response.data[0] if response.data else None
    
    def create_user(self, user_data):
        response = self.client.table('users').insert(user_data).execute()
        return response.data[0] if response.data else None
    
    def get_all_users(self):
        response = self.client.table('users').select('*').execute()
        return response.data
    
    def get_user_by_id(self, user_id):
        response = self.client.table('users').select('*').eq('id', user_id).execute()
        return response.data[0] if response.data else None

    def get_tasks_for_user(self, user_id):

        response = self.client.table('tasks').select('*, created_by(*), assigned_to(*)').or_(f"created_by.eq.{user_id},assigned_to.eq.{user_id}").order('created_at', desc=True).execute()
        return response.data

    def create_task(self, task_data):
        response = self.client.table('tasks').insert(task_data).execute()
        return response.data[0] if response.data else None

    def update_task_status(self, task_id, status):
        response = self.client.table('tasks').update({'status': status}).eq('id', task_id).execute()
        return response.data[0] if response.data else None
    
    def get_task_by_id(self, task_id):
        response = self.client.table('tasks').select('*').eq('id', task_id).execute()
        return response.data[0] if response.data else None

supabase_service = SupabaseService()
