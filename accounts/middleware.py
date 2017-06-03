from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.deprecation import MiddlewareMixin


class DeactivatedMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            if not request.user.is_active:
                path = request.path_info.lstrip('/')
                print(path)

                if path and not any(path != p for p in ["admin", "/accounts"]):
                    return redirect(reverse_lazy('accounts:deactivated'))
