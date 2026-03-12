from datetime import datetime

def parse_time(time_str):
    try:
        return datetime.strptime(time_str, "%H:%M")
    except ValueError:
        raise ValueError("Invalid time format. Use HH:MM")

def format_time(time_obj):
    return time_obj.strftime("%H:%M")