from datetime import datetime


def validate_gender(gender_string):
    return gender_string.upper() in ['М', 'Ж']


def validate_date(date_string):
    try:
        date = datetime.strptime(date_string, "%Y-%m-%d")
        if date > datetime.now():
            return False  # Дата не должна быть в будущем
        return True
    except ValueError:
        return False


def validate_date_event(date_str):
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        if date_obj.date() < datetime.now().date():
            print("Ошибка: дата не может быть в прошлом.")
            return None
        return date_obj
    except ValueError:
        print("Ошибка: дата должна быть в формате YYYY-MM-DD.")
        return None
