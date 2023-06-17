import logging
from io import BytesIO

import requests
from PIL import Image
from django.http import HttpResponse
from django.shortcuts import redirect, resolve_url
from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from .client import SpotifyClient
from .exceptions import NoTrackPlaying
from .mixins import SpotifyClientMixin
from .models import SpotifyToken
from .serializers import CurrentTrackSerializer
from .utils import SpotifyBanner, ASSETS_DIR

logger = logging.getLogger(__name__)


class SpotifyRegisterView(GenericAPIView):

    @staticmethod
    def get(request):
        url = SpotifyClient.get_oauth_url()
        return redirect(url)


class SpotifyCallbackView(GenericAPIView):

    @staticmethod
    def get(request: Request):
        url = request.get_full_path()
        client = SpotifyClient()
        code = client.auth_manager.get_authorization_code(url)
        client.auth_manager.get_access_token(code)
        token: SpotifyToken = client.get_spotify_token()
        # if request allows html content-type, redirect to banner
        http_accept = request.META.get('HTTP_ACCEPT', '')
        if http_accept.contains('text/html') or http_accept.contains('*'):
            return redirect(resolve_url('current-track-banner', auth_id=token.id))

        return redirect(resolve_url('current-track-banner', auth_id=token.id))


class CurrentTrackView(SpotifyClientMixin, RetrieveAPIView):
    serializer_class = CurrentTrackSerializer

    def get_object(self):
        current_track = self.client.current_user_playing_track()
        if not current_track:
            raise NoTrackPlaying
        return current_track


class CurrentTrackBannerView(SpotifyClientMixin, GenericAPIView):

    def get(self, request: Request, *args, **kwargs):
        track = self.client.current_user_playing_track()
        banner = None
        if track:
            banner = SpotifyBanner(track).banner
        else:
            fallback_image = request.query_params.get('fallback')
            if fallback_image:
                try:
                    image_response = requests.get(fallback_image)
                    image_response.raise_for_status()
                    image_io = BytesIO(image_response.content)
                    banner = Image.open(image_io)
                except Exception as e:
                    logger.error(e)

        if not banner:
            banner = Image.open(fr'{ASSETS_DIR}/NotListening.png')

        response = HttpResponse(content_type='image/png')
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        # noinspection PyTypeChecker
        banner.save(response, 'PNG')
        return response


class CurrentTrackRedirectView(SpotifyClientMixin, GenericAPIView):
    def get(self, request, **kwargs):
        current_track = self.client.current_user_playing_track()
        if current_track:
            return redirect(current_track['item']['external_urls']['spotify'])
        return Response(status=status.HTTP_204_NO_CONTENT)
