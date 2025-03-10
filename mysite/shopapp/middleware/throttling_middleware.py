import json
import os
from datetime import datetime, timedelta
from django.http import JsonResponse

# Путь к файлу для хранения посещений
LOG_FILE = "daily_visits.json"

# Время блокировки IP после последнего запроса
THROTTLE_TIME = timedelta(seconds=10)


class ThrottlingMiddleware:
    """Middleware для учета посещений и ограничения частоты запросов"""

    def __init__(self, get_response):
        self.get_response = get_response
        self.visits = self.load_visits()

    def __call__(self, request):
        """Обрабатывает каждый запрос"""
        response = self.process_request(request)
        return response if response else self.get_response(request)

    def load_visits(self):
        """Загружает данные посещений из JSON-файла"""
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r", encoding="utf-8") as file:
                try:
                    return json.load(file)
                except json.JSONDecodeError:
                    return {}
        return {}

    def save_visits(self):
        """Сохраняет данные посещений в JSON-файл"""
        with open(LOG_FILE, "w", encoding="utf-8") as file:
            json.dump(self.visits, file, ensure_ascii=False, indent=4)

    def process_request(self, request):
        """Обрабатывает входящие запросы"""
        ip = self.get_client_ip(request)
        today = datetime.now().strftime("%Y-%m-%d")
        now = datetime.now()

        # Если запись за сегодняшний день отсутствует, создаем её
        if today not in self.visits:
            self.visits[today] = {"ips": {}, "total_visits": 0}

        # Гарантируем, что есть ключ "ips"
        if "ips" not in self.visits[today]:
            self.visits[today]["ips"] = {}

        # Проверяем последний запрос от IP
        if ip in self.visits[today]["ips"]:
            last_visit_time = datetime.fromisoformat(self.visits[today]["ips"][ip])
            if now - last_visit_time < THROTTLE_TIME:
                return JsonResponse({"error": "Too many requests, try again later"}, status=429)

        # Записываем текущее время посещения
        self.visits[today]["ips"][ip] = now.isoformat()

        # Обновляем количество уникальных посещений
        self.visits[today]["total_visits"] = len(self.visits[today]["ips"])

        # Сохраняем обновленные данные
        self.save_visits()

    def get_client_ip(self, request):
        """Получает IP-адрес клиента"""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]
        return request.META.get("REMOTE_ADDR")
