from django.db import models


class URL(models.Model):
    original_url = models.URLField()
    short_code = models.CharField(max_length=12, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    click_count = models.PositiveIntegerField(default=0)

    # Optional feature fields (used by the updated shrtn-like UI).
    expires_at = models.DateTimeField(null=True, blank=True)
    calls_remaining = models.PositiveIntegerField(null=True, blank=True)
    password_hash = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.original_url

    @property
    def is_expired(self):
        # Lazy import to avoid timezone dependency at import-time.
        from django.utils import timezone

        return self.expires_at is not None and timezone.now() > self.expires_at

    @property
    def is_call_limit_reached(self):
        return self.calls_remaining is not None and self.calls_remaining <= 0
