from django.contrib import admin

from .models import URL


@admin.register(URL)
class URLAdmin(admin.ModelAdmin):
    list_display = ("short_code", "original_url", "click_count", "created_at")
    search_fields = ("short_code", "original_url")
