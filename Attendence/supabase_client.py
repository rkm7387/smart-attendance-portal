from .clients import create_supabase_client

supabase = None

try:
    supabase = create_supabase_client()
except Exception:
    supabase = None