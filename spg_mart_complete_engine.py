import os
import sys
import django
from django.conf import settings
from django.core.wsgi import get_wsgi_application
from django.http import JsonResponse, HttpResponse
from django.urls import path
from django.db import models
import dj_database_url

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Configure Django Settings first
if not settings.configured:
    settings.configure(
        DEBUG=os.environ.get("DEBUG", "False") == "True",
        SECRET_KEY=os.environ.get("SECRET_KEY", "spg-mart-super-secret-key-2026"),
        ALLOWED_HOSTS=["*"],
        ROOT_URLCONF=__name__,
        MIDDLEWARE=[
            "corsheaders.middleware.CorsMiddleware",
            "django.middleware.security.SecurityMiddleware",
            "whitenoise.middleware.WhiteNoiseMiddleware",
            "django.middleware.common.CommonMiddleware",
            "django.middleware.csrf.CsrfViewMiddleware",
            "django.middleware.clickjacking.XFrameOptionsMiddleware",
        ],
        INSTALLED_APPS=[
            "django.contrib.contenttypes",
            "django.contrib.auth",
            "django.contrib.staticfiles",
            "corsheaders",
            "rest_framework",
        ],
        DATABASES={
            "default": dj_database_url.config(
                default="postgresql://postgres:postgres@localhost:5432/spg_mart_db",
                conn_max_age=600,
            )
        },
        STATIC_URL="/static/",
        STATIC_ROOT=os.path.join(BASE_DIR, "staticfiles"),
        STATICFILES_STORAGE="whitenoise.storage.CompressedManifestStaticFilesStorage",
        CORS_ALLOW_ALL_ORIGINS=True,
    )

# Setup Django apps after configuration
django.setup()

# Database Models
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        app_label = "spg_app"

class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.IntegerField(default=0)
    sku = models.CharField(max_length=50, unique=True)
    is_spg_brand = models.BooleanField(default=False)
    description = models.TextField(blank=True)

    class Meta:
        app_label = "spg_app"

# API Views
def home_view(request):
    return JsonResponse({
        "status": "online",
        "platform": "SPG MART E-Commerce Platform API",
        "message": "Backend engine is successfully running on Render!"
    })

def health_check(request):
    return HttpResponse("OK", status=200)

# URL Routing
urlpatterns = [
    path("", home_view),
    path("health/", health_check),
]

# WSGI Application for Gunicorn / Render
app = get_wsgi_application()
application = app

def main():
    """Run administrative tasks."""
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
