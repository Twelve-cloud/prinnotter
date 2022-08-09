from django.conf import settings
from user.models import User
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
import jwt


class JWTMiddleware:
    def __init__(self, next):
        self.next = next

    def __call__(self, request):
        if 'access_token' in request.COOKIES and \
            request.path != '/user/registration/' and \
                request.path != '/user/login/':

            access_token = request.COOKIES['access_token']

            try:
                print('access')
                payload_access = jwt.decode(
                    access_token,
                    settings.SECRET_KEY,
                    algorithms=["HS256"]
                )
                user = User.objects.get(pk=payload_access.get('id'))
                user.access_expired = False
                request.user = user

            except ObjectDoesNotExist:
                return HttpResponse(status=404)

            except jwt.ExpiredSignatureError:
                refresh_token = request.COOKIES['refresh_token']

                try:
                    print('refresh')
                    payload_refresh = jwt.decode(
                        refresh_token,
                        settings.SECRET_KEY,
                        algorithms=["HS256"]
                    )

                    user = User.objects.get(pk=payload_refresh.get('id'))
                    user.access_expired = True
                    request.user = user

                except jwt.ExpiredSignatureError:
                    print('no token')
                    return redirect('login')

            response = self.next(request)

            if user.access_expired:
                response.set_cookie(
                    'access_token',
                    user.access_token
                )

                response.set_cookie(
                    'refresh_token',
                    user.refresh_token
                )

            return response
        else:
            response = self.next(request)
            return response
