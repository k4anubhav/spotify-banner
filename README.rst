=====
Spotify-banner
=====

Spotify banner is a simple django app that allows you to display a spotify banner on your site that links to Spotify.


Quick start
-----------

1. Add "spotify_banner" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'spotify_banner',
    ]

2. Include the spotify_banner URLconf in your project urls.py like this::

    path('spotify/', include('spotify_banner.urls')),

3. Run ``python manage.py migrate``.

5. Visit http://127.0.0.1:8000/spotify/register to get banner url.
