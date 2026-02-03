from datetime import datetime
import pytz
from .logger import get_logger

logger = get_logger(__name__)

def current_ist_date():
    """Return current date string in Asia/Kolkata as YYYY-MM-DD"""
    try:
        IST = pytz.timezone("Asia/Kolkata")
        return datetime.now(IST).strftime("%Y-%m-%d")
    except Exception:
        logger.exception("Failed to compute IST date")
        return datetime.now().strftime("%y-%m-%d")