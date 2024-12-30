from datetime import datetime

def current_time_and_year(request):
    """
    Контекстный процессор для передачи текущего времени и года.
    """
    now = datetime.now()
    return {
        'current_time': now.strftime('%H:%M:%S'),
        'current_year': now.year,
    }
