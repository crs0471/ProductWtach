from datetime import datetime
import pytz
from django.utils import timezone

def now():
    return datetime.now(tz=pytz.timezone('Asia/Kolkata'))
    