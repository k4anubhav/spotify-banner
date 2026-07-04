from .models import SpotifyToken


@admin.register(SpotifyToken)
class ModelNameAdmin(admin.ModelAdmin):
    list_display = ('user', 'access_token', 'refresh_token', 'expires_at')
    search_fields = ('user__username', 'user__email')
    list_filter = ('expires_at',)
