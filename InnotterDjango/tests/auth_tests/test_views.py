from jwt_auth.serializers import SignInSerializer
from jwt_auth.views import AuthViewSet
from rest_framework import status
import pytest


pytestmark = pytest.mark.django_db

sign_in_view = AuthViewSet.as_view({'post': 'sign_in'})
refresh_view = AuthViewSet.as_view({'get': 'refresh'})


class TestAuthViews:
    def test_sign_in(self, api_factory, user_json, mocker):
        mocker.patch.object(AuthViewSet, 'serializer_class', SignInSerializer)

        request = api_factory.post('', user_json, format='json')
        response = sign_in_view(request)
        assert response.status_code == status.HTTP_200_OK

    def test_refresh(self, api_factory, refresh_token):
        request = api_factory.get('')
        response = refresh_view(request)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        request.COOKIES = {'refresh_token': refresh_token}
        response = refresh_view(request)
        assert response.status_code == status.HTTP_200_OK
