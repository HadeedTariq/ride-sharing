from django import http
from django.shortcuts import redirect
from authentication import utils


class RideMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/ride/"):
            access_token = request.COOKIES.get("access_token")
            if access_token:
                try:
                    user = utils.validate_access_token(access_token)
                    if (
                        request.path.startswith("/ride/driver")
                        and user["role"] != "driver"
                    ):
                        return redirect("/ride/home/")

                    request.user_data = user
                    response = self.get_response(request)
                    return response
                except Exception as e:
                    print(e)
                    return http.HttpResponse("Ivalid Token")

            else:
                return redirect("/auth/login/")

        else:
            request.validation_err = ""
            response = self.get_response(request)
            return response
