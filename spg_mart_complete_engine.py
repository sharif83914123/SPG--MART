import os
import sys

spg_mart_complete_engine.py
import os
import sys
from django.conf import settings
from django.core.wsgi import get_wsgi_application
from django.http import JsonResponse, HttpResponse
from django.urls import path
from django.db import models
import dj_database_url
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if not settings.configured:
    settings.configure(
        DEBUG=os.environ.get("DEBUG", "False") == "True",
        SECRET_KEY=os.environ.get("SECRET_KEY", "spg-mart-super-secret-key-12345"),
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
# Database Models
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    class Meta:
        app_label = "spg_app"
class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products", null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.IntegerField(default=0)
    sku = models.CharField(max_length=50, unique=True)
    is_spg_brand = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    class Meta:
        app_label = "spg_app"
# Frontend Views
def home_view(request):
    html_content = """
    <!DOCTYPE html>
    <html lang="bn">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>SUPER POWER GROUP (SPG MART)</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    </head>
    <body class="bg-gray-100 font-sans pb-16 md:pb-0">
        <!-- Top Header -->
        <header class="bg-[#FEEE00] sticky top-0 z-50 shadow-md">
            <div class="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between gap-4">
                <div class="flex items-center gap-2">
                    <span class="font-extrabold text-2xl tracking-wider text-black">SPG<span class="text-red-600">MART</span></span>
                </div>
                <div class="flex-1 max-w-2xl">
                    <div class="relative">
                        <input type="text" placeholder="পণ্য বা ব্র্যান্ড খুঁজুন..." class="w-full pl-4 pr-10 py-2 rounded-lg border-none focus:outline-none focus:ring-2 focus:ring-red-500">
                        <button class="absolute right-3 top-2.5 text-gray-500"><i class="fas fa-search"></i></button>
                    </div>
                </div>
                <div class="hidden md:flex items-center gap-6 font-semibold">
                    <a href="#" class="hover:text-red-600"><i class="fas fa-user mr-1"></i> অ্যাকাউন্ট</a>
                    <a href="#" class="hover:text-red-600"><i class="fas fa-shopping-cart mr-1"></i> কার্ট</a>
                </div>
            </div>
        </header>
        <!-- Main Banner -->
        <main class="max-w-7xl mx-auto px-4 mt-6">
            <div class="bg-gradient-to-r from-red-600 to-yellow-500 rounded-2xl p-8 text-white mb-8 shadow-lg">
                <h1 class="text-3xl font-bold mb-2">SUPER POWER GROUP (SPG MART)</h1>
                <p class="text-lg">চট্টগ্ৰাম ও সারা বাংলাদেশে ইলেকট্রিক্যাল, ইলেকট্রনিক্স ও লাইটিং সামগ্রীর বিশ্বস্ত প্রতিষ্ঠান!</p>
            </div>
            <!-- Products Section -->
            <h2 class="text-xl font-bold mb-4 text-gray-800">জনপ্রিয় পণ্যসমূহ</h2>
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div class="bg-white p-4 rounded-xl shadow border">
                    <div class="w-full h-32 bg-gray-200 rounded-lg mb-3 flex items-center justify-center text-gray-500 font-semibold">SPG Product</div>
                    <span class="text-xs bg-red-100 text-red-600 font-bold px-2 py-1 rounded">SPG Brand</span>
                    <h3 class="font-bold mt-2 text-gray-800">স্মার্ট সুইচেস ও সকেট</h3>
                    <p class="text-red-600 font-bold mt-1">৳ ৪৫০ <span class="text-gray-400 line-through text-sm">৳ ৬০০</span></p>
                    <button class="w-full mt-3 bg-[#FEEE00] font-bold py-2 rounded-lg hover:bg-yellow-400 text-black shadow">Add to Cart</button>
                </div>
            </div>
        </main>
        <!-- Bottom Mobile Navigation -->
        <nav class="fixed bottom-0 left-0 right-0 bg-white border-t flex justify-around py-2 md:hidden z-50 shadow-lg">
            <a href="#" class="flex flex-col items-center text-red-600"><i class="fas fa-home"></i><span class="text-xs">Home</span></a>
            <a href="#" class="flex flex-col items-center text-gray-600"><i class="fas fa-th-large"></i><span class="text-xs">Categories</span></a>
            <a href="#" class="flex flex-col items-center text-gray-600"><i class="fas fa-tags"></i><span class="text-xs">Sales</span></a>
            <a href="#" class="flex flex-col items-center text-gray-600"><i class="fas fa-user"></i><span class="text-xs">Account</span></a>
            <a href="#" class="flex flex-col items-center text-gray-600"><i class="fas fa-shopping-cart"></i><span class="text-xs">Cart</span></a>
        </nav>
    </body>
    </html>
    """
    return HttpResponse(html_content)
def health_check(request):
    return JsonResponse({"status": "OK", "service": "SPG MART Engine"})
urlpatterns = [
    path("", home_view, name="home"),
    path("api/health/", health_check, name="health"),
]
app = get_wsgi_application()

