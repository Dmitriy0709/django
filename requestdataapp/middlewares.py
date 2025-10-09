import time
from django.http import HttpRequest, JsonResponse


class ThrottleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.visits = {}
        self.TIME_PERIOD = 2  # Минимальный интервал между запросами (в секундах)

    def __call__(self, request):
        # Получаем IP адрес пользователя
        ip = request.META.get('REMOTE_ADDR') or request.META.get('HTTP_X_FORWARDED_FOR')
        if not ip:
            ip = 'unknown'

        now = time.time()

        # Проверяем последний визит с этого IP
        last_visit = self.visits.get(ip)
        if last_visit and (now - last_visit < self.TIME_PERIOD):
            return JsonResponse({
                'error': 'Слишком много запросов. Попробуйте позже.'
            }, status=429)

        # Сохраняем время текущего запроса
        self.visits[ip] = now

        response = self.get_response(request)
        return response


def setup_useragent_on_request_middleware(get_response):
    print("initial call")

    def middleware(request: HttpRequest):
        print("before get response")
        request.user_agent = request.META["HTTP_USER_AGENT"]
        response = get_response(request)
        print("after get response")
        return response

    return middleware

class CountRequestsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests_count = 0
        self.responses_count = 0
        self.exception_count = 0

    def __call__(self, request: HttpRequest):
        self.requests_count += 1
        print("requests count", self.requests_count)
        response = self.get_response(request)
        self.responses_count += 1
        print("responses count", self.responses_count)
        return response

    def process_exception(self, request: HttpRequest, exception: Exception):
        self.exception_count += 1
        print("got", self.exception_count, "exceptions so far")
