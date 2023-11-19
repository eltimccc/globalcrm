from django.shortcuts import redirect
from django.urls import reverse


class LogoutRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if not request.user.is_authenticated and request.path == reverse('users:logout'):
            return redirect('tasks:index')

        return response