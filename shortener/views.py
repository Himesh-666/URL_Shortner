import json
from datetime import timedelta

from django.contrib.auth.hashers import check_password, make_password
from django.db import transaction
from django.db.models import F
from django.http import Http404, JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST

from .models import URL
from .utils import base62_encode


TTL_MAP = {
    # shrtn-like TTL options
    "year": lambda now: now + timedelta(days=365),
    "month": lambda now: now + timedelta(days=30),
    "week": lambda now: now + timedelta(days=7),
    "day": lambda now: now + timedelta(days=1),
    "hour": lambda now: now + timedelta(hours=1),
}


def _parse_ttl(ttl_key: str | None, now):
    if not ttl_key or ttl_key == "never":
        return None
    if ttl_key not in TTL_MAP:
        return None
    return TTL_MAP[ttl_key](now)


@ensure_csrf_cookie
def home(request):
    if request.method == "POST":
        long_url = (request.POST.get("url") or "").strip()
        if not long_url:
            return render(request, "shortener/home.html", {"error": "Please enter a URL."})

        ttl_key = (request.POST.get("ttl") or "never").strip()
        now = timezone.now()
        expires_at = _parse_ttl(ttl_key, now)

        call_limit_raw = (request.POST.get("call_limit") or "").strip()
        calls_remaining = None
        if call_limit_raw:
            try:
                parsed = int(call_limit_raw)
                if parsed <= 0:
                    return render(
                        request,
                        "shortener/home.html",
                        {"error": "Call limit must be a positive number."},
                    )
                calls_remaining = parsed
            except ValueError:
                return render(
                    request,
                    "shortener/home.html",
                    {"error": "Call limit must be a number."},
                )

        password = (request.POST.get("password") or "").strip()
        password_hash = make_password(password) if password else ""

        with transaction.atomic():
            url = URL(
                original_url=long_url,
                expires_at=expires_at,
                calls_remaining=calls_remaining,
                password_hash=password_hash,
            )
            url.save()
            url.short_code = base62_encode(url.pk)
            url.save(update_fields=["short_code"])
        code = url.short_code

        # Our redirect route is defined as `/<code>/`, so generate URLs with
        # the trailing slash to avoid relying on Django's APPEND_SLASH.
        short_url = request.build_absolute_uri(f"{code}/")
        return render(
            request,
            "shortener/home.html",
            {
                "short_url": short_url,
                "short_code": code,
                "remember_original_url": long_url,
            },
        )

    return render(request, "shortener/home.html")


_MAX_STATS_CODES = 80


@require_POST
def link_stats(request):
    """Return click counts and destinations for a set of short codes (for Remember Links)."""
    try:
        body = json.loads(request.body.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"error": "Invalid JSON."}, status=400)

    codes = body.get("codes")
    if not isinstance(codes, list):
        return JsonResponse({"error": "Expected a JSON array field 'codes'."}, status=400)

    normalized = []
    seen = set()
    for raw in codes:
        if len(normalized) >= _MAX_STATS_CODES:
            break
        c = str(raw).strip()[:12]
        if not c or c in seen:
            continue
        seen.add(c)
        normalized.append(c)

    if not normalized:
        return JsonResponse({"links": {}})

    rows = URL.objects.filter(short_code__in=normalized).values(
        "short_code", "original_url", "click_count"
    )
    links = {
        row["short_code"]: {
            "short_code": row["short_code"],
            "original_url": row["original_url"],
            "click_count": row["click_count"],
        }
        for row in rows
    }
    return JsonResponse({"links": links})


def _handle_redirect_after_checks(request, url_obj: URL):
    """Redirect to original URL, record a click, and apply call decrement if configured."""
    updates: dict = {"click_count": F("click_count") + 1}
    if url_obj.calls_remaining is not None and url_obj.calls_remaining > 0:
        updates["calls_remaining"] = F("calls_remaining") - 1
    URL.objects.filter(pk=url_obj.pk).update(**updates)
    return redirect(url_obj.original_url)


def redirect_url(request, code):
    try:
        url_obj = URL.objects.get(short_code=code)
    except URL.DoesNotExist:
        raise Http404("Short URL not found.")

    now = timezone.now()
    if url_obj.expires_at is not None and now > url_obj.expires_at:
        return render(request, "shortener/expired.html", {"short_code": code})

    if url_obj.calls_remaining is not None and url_obj.calls_remaining <= 0:
        return render(request, "shortener/limit_reached.html", {"short_code": code})

    # If password-protected, require unlocking once per browser session.
    if url_obj.password_hash:
        session_key = "unlocked_short_codes"
        unlocked = set(request.session.get(session_key, []))

        if code not in unlocked:
            if request.method == "POST":
                provided_password = (request.POST.get("password") or "").strip()
                if provided_password and check_password(provided_password, url_obj.password_hash):
                    unlocked.add(code)
                    request.session[session_key] = list(unlocked)
                    return _handle_redirect_after_checks(request, url_obj)
                return render(
                    request,
                    "shortener/password_prompt.html",
                    {"short_code": code, "error": "Incorrect password."},
                )

            return render(request, "shortener/password_prompt.html", {"short_code": code})

    return _handle_redirect_after_checks(request, url_obj)

