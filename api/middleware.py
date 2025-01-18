from django.http import JsonResponse
import os

class ApiKeyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # API 키 확인이 필요없는 경로는 여기서 처리
        if request.path.startswith('/admin/'):  # 예시: admin 페이지 제외
            return self.get_response(request)

        api_key = request.headers.get('X-API-KEY')
        valid_keys = os.getenv('API_KEYS', '').split(',')

        print(api_key)
        print(valid_keys)

        if not api_key or api_key not in valid_keys:
            return JsonResponse(
                {'error': '유효하지 않은 API 키입니다.'}, 
                status=401
            )

        return self.get_response(request)