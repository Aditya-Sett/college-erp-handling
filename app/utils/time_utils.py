from datetime import datetime

def parse_time(time_str):
    try:
        return datetime.strptime(time_str, "%H:%M")
    except ValueError:
        raise ValueError("Invalid time format. Use HH:MM")

def format_time(time_obj):
    return time_obj.strftime("%H:%M")

def parse_datetime(dt_str):
    try:
        # Try ISO format first (your current working format)
        return datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
    except:
        try:
            # Try RFC 1123 format (frontend case)
            return datetime.strptime(dt_str, "%a, %d %b %Y %H:%M:%S GMT")
        except:
            raise ValueError("Unsupported datetime format")