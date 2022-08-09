from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer


def create_response(data,
        status=status.HTTP_200_OK,
        accepted_renderer = JSONRenderer(),
        accepted_media_type='application/json',
        renderer_context={}
    ):
    response = Response(
        data=data,
        status=status
    )
    response.accepted_renderer = accepted_renderer
    response.accepted_media_type = accepted_media_type
    response.renderer_context = renderer_context
    response.render()
    return response
