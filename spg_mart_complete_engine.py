
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

# Full Frontend HTML Interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="bn" class="light">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SPG MART | Super Power Group Shopping Platform</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    colors: {
                        spgYellow: '#FEEE00',
                        spgRed: '#E53E3E',
                        spgGreen: '#38A169',
                        spgDark: '#1A202C'
                    }
                }
            }
        }
    </script>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
</head>
<body class="bg-gray-50 dark:bg-gray-900 text-gray-800 dark:text-gray-100 font-sans pb-16 md:pb-0">

    <div class="bg-spgRed text-white text-xs text-center py-1 font-bold">
        ⚡ SPG MART মেগা সেল! চট্টগ্রামসহ সারা বাংলাদেশে দ্রুত ডেলিভারি ⚡
    </div>

    <header class="bg-spgYellow text-black sticky top-0 z-50 shadow-md">
        <div class="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between gap-4">
            <div class="flex items-center space-x-2 cursor-pointer" onclick="switchTab('home')">
                <div class="bg-black text-spgYellow font-extrabold text-2xl px-3 py-1 rounded shadow">SPG</div>
                <div class="flex flex-col">
                    <span class="font-extrabold text-lg leading-none">MART</span>
                    <span class="text-[9px] font-semibold tracking-widest text-gray-800">SUPER POWER GROUP</span>
                </div>
            </div>

            <div onclick="openLocationModal()" class="hidden md:flex items-center text-xs font-semibold cursor-pointer hover:bg-yellow-400 p-2 rounded transition">
                <i data-lucide="map-pin" class="w-4 h-4 mr-1 text-spgRed"></i>
                <div>
                    <div class="text-[10px] text-gray-700">ডেলিভারি লোকেশন</div>
                    <div class="font-bold">চট্টগ্রাম, বাংলাদেশ ▾</div>
                </div>
            </div>

            <div class="flex-1 max-w-2xl relative">
                <input type="text" placeholder="SPG লাইট, ফ্যান, সুইচ বা স্যানিটারি পণ্য খুঁজুন..." 
                       class="w-full pl-4 pr-10 py-2 rounded-lg text-sm bg-white dark:bg-gray-800 text-black dark:text-white border-none focus:ring-2 focus:ring-black outline-none shadow-inner">
                <button class="absolute right-2 top-2 text-gray-600 dark:text-gray-300">
                    <i data-lucide="search" class="w-5 h-5"></i>
                </button>
            </div>

            <div class="hidden md:flex items-center space-x-6 text-sm font-semibold">
                <button onclick="toggleDarkMode()" class="p-2 rounded-full hover:bg-yellow-400">
                    <i data-lucide="moon" class="w-5 h-5"></i>
                </button>
                <button onclick="switchTab('account')" class="flex items-center gap-1 hover:text-gray-700">
                    <i data-lucide="user" class="w-5 h-5"></i>
                    <span>অ্যাকাউন্ট</span>
                </button>
                <button onclick="switchTab('cart')" class="flex items-center gap-1 relative hover:text-gray-700">
                    <i data-lucide="shopping-cart" class="w-5 h-5"></i>
                    <span>কার্ট</span>
                    <span class="absolute -top-2 -right-2 bg-spgRed text-white text-[10px] rounded-full w-4 h-4 flex items-center justify-center font-bold">3</span>
                </button>
            </div>
        </div>
    </header>

    <nav class="bg-black text-white text-xs md:text-sm overflow-x-auto shadow-inner">
        <div class="max-w-7xl mx-auto px-4 flex items-center space-x-6 py-2 whitespace-nowrap">
            <span class="font-bold text-spgYellow flex items-center"><i data-lucide="menu" class="w-4 h-4 mr-1"></i> সব ক্যাটাগরি:</span>
            <a href="#" class="hover:text-spgYellow">ইলেকট্রিক্যাল পণ্য</a>
            <a href="#" class="hover:text-spgYellow">LED লাইট ও লাইটিং</a>
            <a href="#" class="hover:text-spgYellow">ফ্যান ও কুলিং</a>
            <a href="#" class="hover:text-spgYellow">সুইচ ও সকেট</a>
            <a href="#" class="hover:text-spgYellow">ইলেকট্রিক্যাল এক্সেসরিজ</a>
            <a href="#" class="hover:text-spgYellow">সোলার পণ্য</a>
            <a href="#" class="hover:text-spgYellow">স্যানিটারি পণ্য</a>
            <a href="#" class="font-bold text-spgYellow border-b-2 border-spgYellow">SPG ব্র্যান্ডের পণ্য</a>
        </div>
    </nav>

    <main class="max-w-7xl mx-auto px-4 py-6" id="main-content">
        <section id="view-home" class="space-y-8">
            <div class="relative bg-gradient-to-r from-yellow-500 to-red-600 rounded-2xl overflow-hidden text-white p-8 md:p-12 shadow-xl flex items-center justify-between">
                <div class="space-y-4 max-w-lg z-10">
                    <span class="bg-black text-spgYellow px-3 py-1 text-xs font-extrabold rounded-full uppercase tracking-widest">SPG Exclusive</span>
                    <h1 class="text-3xl md:text-5xl font-black leading-tight">প্রিমিয়াম কোয়ালিটি সুইচ ও মেগা লাইটিং</h1>
                    <p class="text-sm opacity-90">অফিসিয়াল SPG ব্র্যান্ডেড পণ্যে পান সর্বোচ্চ ৩০% পর্যন্ত ক্যাশব্যাক ও গ্যারান্টি।</p>
                    <button onclick="switchTab('cart')" class="bg-black text-white px-6 py-3 rounded-xl font-bold shadow-lg hover:bg-gray-800 transition transform hover:scale-105">এখনই কিনুন</button>
                </div>
                <div class="hidden lg:block">
                    <i data-lucide="zap" class="w-64 h-64 text-yellow-300 opacity-30"></i>
                </div>
            </div>

            <div>
                <h2 class="text-xl font-bold mb-4 flex items-center"><i data-lucide="grid" class="w-5 h-5 mr-2 text-spgRed"></i> জনপ্রিয় ক্যাটাগরি</h2>
                <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-4">
                    <div class="bg-white dark:bg-gray-800 p-4 rounded-xl shadow text-center cursor-pointer hover:shadow-md transition">
                        <i data-lucide="lightbulb" class="w-8 h-8 mx-auto text-spgYellow mb-2"></i>
                        <span class="text-xs font-bold">LED লাইট</span>
                    </div>
                    <div class="bg-white dark:bg-gray-800 p-4 rounded-xl shadow text-center cursor-pointer hover:shadow-md transition">
                        <i data-lucide="fan" class="w-8 h-8 mx-auto text-blue-500 mb-2"></i>
                        <span class="text-xs font-bold">ফ্যান ও কুলিং</span>
                    </div>
                    <div class="bg-white dark:bg-gray-800 p-4 rounded-xl shadow text-center cursor-pointer hover:shadow-md transition">
                        <i data-lucide="toggle-right" class="w-8 h-8 mx-auto text-spgGreen mb-2"></i>
                        <span class="text-xs font-bold">সুইচ ও সকেট</span>
                    </div>
                    <div class="bg-white dark:bg-gray-800 p-4 rounded-xl shadow text-center cursor-pointer hover:shadow-md transition">
                        <i data-lucide="sun" class="w-8 h-8 mx-auto text-yellow-600 mb-2"></i>
                        <span class="text-xs font-bold">সোলার পণ্য</span>
                    </div>
                    <div class="bg-white dark:bg-gray-800 p-4 rounded-xl shadow text-center cursor-pointer hover:shadow-md transition">
                        <i data-lucide="droplet" class="w-8 h-8 mx-auto text-cyan-500 mb-2"></i>
                        <span class="text-xs font-bold">স্যানিটারি</span>
                    </div>
                    <div class="bg-white dark:bg-gray-800 p-4 rounded-xl shadow text-center cursor-pointer hover:shadow-md transition border-2 border-spgYellow">
                        <i data-lucide="shield-check" class="w-8 h-8 mx-auto text-spgRed mb-2"></i>
                        <span class="text-xs font-bold text-spgRed">SPG নিজস্ব ব্র্যান্ড</span>
                    </div>
                </div>
            </div>

            <div class="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-md border border-gray-100 dark:border-gray-700">
                <div class="flex justify-between items-center mb-4">
                    <div class="flex items-center space-x-2">
                        <span class="bg-spgRed text-white p-1 rounded"><i data-lucide="flame" class="w-5 h-5"></i></span>
                        <h2 class="text-xl font-bold">ফ্ল্যাশ ডিল (Flash Sale)</h2>
                    </div>
                    <span class="text-xs bg-yellow-100 dark:bg-yellow-900 text-yellow-800 dark:text-yellow-200 px-3 py-1 rounded-full font-mono font-bold">সময় বাকি: 05h : 23m : 12s</span>
                </div>

                <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-6">
                    <div class="border rounded-xl p-4 relative hover:shadow-lg transition bg-white dark:bg-gray-800">
                        <span class="absolute top-2 left-2 bg-spgRed text-white text-[10px] font-bold px-2 py-0.5 rounded">-20%</span>
                        <div class="h-40 bg-gray-100 dark:bg-gray-700 rounded-lg mb-3 flex items-center justify-center">
                            <i data-lucide="zap" class="w-16 h-16 text-spgYellow"></i>
                        </div>
                        <span class="text-[10px] font-bold text-spgGreen uppercase">SPG Brand</span>
                        <h3 class="font-bold text-sm line-clamp-2 my-1">SPG 18W Smart Inverter LED Bulb</h3>
                        <div class="flex items-center text-xs text-yellow-500 mb-2">
                            ★★★★★ <span class="text-gray-400 text-[10px] ml-1">(48)</span>
                        </div>
                        <div class="flex items-baseline space-x-2">
                            <span class="text-base font-extrabold">৳৪৫০</span>
                            <span class="text-xs text-gray-400 line-through">৳৫৬০</span>
                        </div>
                        <button onclick="switchTab('cart')" class="w-full mt-3 bg-spgYellow text-black font-bold py-2 rounded-lg text-xs hover:bg-yellow-400 flex items-center justify-center gap-1">
                            <i data-lucide="shopping-cart" class="w-4 h-4"></i> কার্টে যোগ করুন
                        </button>
                    </div>

                    <div class="border rounded-xl p-4 relative hover:shadow-lg transition bg-white dark:bg-gray-800">
                        <span class="absolute top-2 left-2 bg-spgRed text-white text-[10px] font-bold px-2 py-0.5 rounded">-15%</span>
                        <div class="h-40 bg-gray-100 dark:bg-gray-700 rounded-lg mb-3 flex items-center justify-center">
                            <i data-lucide="fan" class="w-16 h-16 text-blue-400"></i>
                        </div>
                        <span class="text-[10px] font-bold text-spgGreen uppercase">SPG Electronics</span>
                        <h3 class="font-bold text-sm line-clamp-2 my-1">SPG High-Speed Ceiling Fan 56"</h3>
                        <div class="flex items-center text-xs text-yellow-500 mb-2">
                            ★★★★☆ <span class="text-gray-400 text-[10px] ml-1">(102)</span>
                        </div>
                        <div class="flex items-baseline space-x-2">
                            <span class="text-base font-extrabold">৳৩,২০০</span>
                            <span class="text-xs text-gray-400 line-through">৳৩,৭৫০</span>
                        </div>
                        <button onclick="switchTab('cart')" class="w-full mt-3 bg-spgYellow text-black font-bold py-2 rounded-lg text-xs hover:bg-yellow-400 flex items-center justify-center gap-1">
                            <i data-lucide="shopping-cart" class="w-4 h-4"></i> কার্টে যোগ করুন
                        </button>
                    </div>

                    <div class="border rounded-xl p-4 relative hover:shadow-lg transition bg-white dark:bg-gray-800">
                        <div class="h-40 bg-gray-100 dark:bg-gray-700 rounded-lg mb-3 flex items-center justify-center">
                            <i data-lucide="toggle-right" class="w-16 h-16 text-spgGreen"></i>
                        </div>
                        <span class="text-[10px] font-bold text-spgGreen uppercase">SPG Electrical</span>
                        <h3 class="font-bold text-sm line-clamp-2 my-1">SPG Luxury Piano Switch Board</h3>
                        <div class="flex items-center text-xs text-yellow-500 mb-2">
                            ★★★★★ <span class="text-gray-400 text-[10px] ml-1">(29)</span>
                        </div>
                        <div class="flex items-baseline space-x-2">
                            <span class="text-base font-extrabold">৳৬৮০</span>
                        </div>
                        <button onclick="switchTab('cart')" class="w-full mt-3 bg-spgYellow text-black font-bold py-2 rounded-lg text-xs hover:bg-yellow-400 flex items-center justify-center gap-1">
                            <i data-lucide="shopping-cart" class="w-4 h-4"></i> কার্টে যোগ করুন
                        </button>
                    </div>

                    <div class="border rounded-xl p-4 relative hover:shadow-lg transition bg-white dark:bg-gray-800">
                        <span class="absolute top-2 left-2 bg-spgRed text-white text-[10px] font-bold px-2 py-0.5 rounded">-10%</span>
                        <div class="h-40 bg-gray-100 dark:bg-gray-700 rounded-lg mb-3 flex items-center justify-center">
                            <i data-lucide="sun" class="w-16 h-16 text-yellow-500"></i>
                        </div>
                        <span class="text-[10px] font-bold text-spgGreen uppercase">SPG Solar</span>
                        <h3 class="font-bold text-sm line-clamp-2 my-1">SPG 100W Mono Solar Panel</h3>
                        <div class="flex items-center text-xs text-yellow-500 mb-2">
                            ★★★★★ <span class="text-gray-400 text-[10px] ml-1">(14)</span>
                        </div>
                        <div class="flex items-baseline space-x-2">
                            <span class="text-base font-extrabold">৳৪,৫০০</span>
                            <span class="text-xs text-gray-400 line-through">৳৫,০০০</span>
                        </div>
                        <button onclick="switchTab('cart')" class="w-full mt-3 bg-spgYellow text-black font-bold py-2 rounded-lg text-xs hover:bg-yellow-400 flex items-center justify-center gap-1">
                            <i data-lucide="shopping-cart" class="w-4 h-4"></i> কার্টে যোগ করুন
                        </button>
                    </div>
                </div>
            </div>
        </section>

        <section id="view-cart" class="hidden space-y-6">
            <h2 class="text-2xl font-bold flex items-center"><i data-lucide="shopping-bag" class="w-6 h-6 mr-2"></i> আপনার শপিং কার্ট</h2>
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div class="lg:col-span-2 space-y-4">
                    <div class="bg-white dark:bg-gray-800 p-4 rounded-xl shadow flex items-center justify-between border">
                        <div class="flex items-center space-x-4">
                            <div class="w-16 h-16 bg-gray-100 dark:bg-gray-700 rounded flex items-center justify-center">
                                <i data-lucide="zap" class="w-8 h-8 text-spgYellow"></i>
                            </div>
                            <div>
                                <h4 class="font-bold text-sm">SPG 18W Smart Inverter LED Bulb</h4>
                                <span class="text-xs text-gray-500">ওয়ারেন্টি: ২ বছর</span>
                                <div class="text-sm font-bold text-spgRed mt-1">৳৪৫০</div>
                            </div>
                        </div>
                        <div class="flex items-center space-x-3">
                            <button class="w-7 h-7 bg-gray-200 dark:bg-gray-700 rounded font-bold">-</button>
                            <span class="font-bold text-sm">2</span>
                            <button class="w-7 h-7 bg-gray-200 dark:bg-gray-700 rounded font-bold">+</button>
                            <button class="text-red-500 ml-2"><i data-lucide="trash-2" class="w-5 h-5"></i></button>
                        </div>
                    </div>
                </div>

                <div class="bg-white dark:bg-gray-800 p-6 rounded-xl shadow border h-fit space-y-4">
                    <h3 class="font-bold border-b pb-2">অর্ডার সামারি</h3>
                    <div class="space-y-2 text-sm">
                        <div class="flex justify-between"><span>সাবটোটাল</span><span>৳৯০০</span></div>
                        <div class="flex justify-between text-spgGreen"><span>ডিসকাウント (SUPER10)</span><span>-৳৯০</span></div>
                        <div class="flex justify-between"><span>ডেলিভারি চার্জ</span><span>৳৬০</span></div>
                        <hr>
                        <div class="flex justify-between font-bold text-base"><span>সর্বমোট</span><span>৳৮৭০</span></div>
                    </div>
                    <div class="flex gap-2">
                        <input type="text" placeholder="কুপন কোড (যেমন: SUPER10)" class="flex-1 border text-xs px-3 py-2 rounded focus:outline-none dark:bg-gray-700">
                        <button class="bg-black text-white px-3 py-2 rounded text-xs font-bold">আবেদন</button>
                    </div>
                    <button onclick="switchTab('checkout')" class="w-full bg-spgYellow text-black font-bold py-3 rounded-lg hover:bg-yellow-400">চেকআউট করুন (৫ ধাপ)</button>
                </div>
            </div>
        </section>

        <section id="view-checkout" class="hidden space-y-6">
            <h2 class="text-2xl font-bold">নিরাপদ চেকআউট</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div class="bg-white dark:bg-gray-800 p-6 rounded-xl shadow space-y-4">
                    <h3 class="font-bold text-lg text-spgRed">১. পেমেন্ট পদ্ধতি নির্বাচন করুন</h3>
                    <div class="grid grid-cols-2 gap-3">
                        <label class="border p-3 rounded-lg flex items-center space-x-2 cursor-pointer hover:border-spgRed">
                            <input type="radio" name="payment" checked>
                            <span class="font-bold text-xs">বিকাশ (bKash)</span>
                        </label>
                        <label class="border p-3 rounded-lg flex items-center space-x-2 cursor-pointer hover:border-spgRed">
                            <input type="radio" name="payment">
                            <span class="font-bold text-xs">নগদ (Nagad)</span>
                        </label>
                        <label class="border p-3 rounded-lg flex items-center space-x-2 cursor-pointer hover:border-spgRed">
                            <input type="radio" name="payment">
                            <span class="font-bold text-xs">ক্যাশ অন ডেলিভারি</span>
                        </label>
                        <label class="border p-3 rounded-lg flex items-center space-x-2 cursor-pointer hover:border-spgRed">
                            <input type="radio" name="payment">
                            <span class="font-bold text-xs">আন্তর্জাতিক কার্ড / PayPal</span>
                        </label>
                    </div>
                    <h3 class="font-bold text-lg text-spgRed pt-4">২. ডেলিভারি ঠিকানা</h3>
                    <p class="text-xs text-gray-500">চট্টগ্রাম শাখা / হোম ডেলিভারি নির্বাচিত</p>
                    <button onclick="alert('অর্ডার সফলভাবে সম্পন্ন হয়েছে! Order ID: #SPG89231')" class="w-full bg-spgGreen text-white font-bold py-3 rounded-lg text-sm mt-4">অর্ডার নিশ্চিত করুন (৳৮৭০)</button>
                </div>
                <div class="bg-gray-100 dark:bg-gray-800 p-6 rounded-xl">
                    <h3 class="font-bold mb-4">অর্ডার বিবরণ</h3>
                    <p class="text-xs mb-2">পণ্য: SPG 18W Smart Inverter LED Bulb (x2)</p>
                    <p class="text-xs font-bold text-spgGreen">সম্ভাব্য ডেলিভারি সময়: ২৪ - ৪৮ ঘণ্টা</p>
                </div>
            </div>
        </section>

        <section id="view-account" class="hidden space-y-6">
            <h2 class="text-2xl font-bold">মাই অ্যাকাউন্ট</h2>
            <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
                <div class="bg-white dark:bg-gray-800 p-4 rounded-xl shadow space-y-2 text-sm font-semibold">
                    <div class="p-2 bg-spgYellow text-black rounded cursor-pointer">My Profile</div>
                    <div class="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded cursor-pointer">My Orders</div>
                    <div class="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded cursor-pointer">Warranty & Guarantee</div>
                    <div class="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded cursor-pointer text-spgRed">Product Return & Refund</div>
                </div>
                <div class="md:col-span-3 bg-white dark:bg-gray-800 p-6 rounded-xl shadow space-y-4">
                    <h3 class="font-bold text-lg border-b pb-2">পণ্য রিটার্ন ও রিফান্ড আবেদন (Return & Refund)</h3>
                    <form onsubmit="event.preventDefault(); alert('আপনার রিটার্ন আবেদনটি জমা দেওয়া হয়েছে। তদন্তের পর রিফান্ড প্রক্রিয়া শুরু হবে।');" class="space-y-4">
                        <div>
                            <label class="block text-xs font-bold mb-1">অর্ডার নির্বাচন করুন</label>
                            <select class="w-full border p-2 rounded text-sm dark:bg-gray-700">
                                <option>Order #SPG89231 - SPG 18W LED Bulb (৳৮৭০)</option>
                            </select>
                        </div>
                        <div>
                            <label class="block text-xs font-bold mb-1">ফেরতের কারণ</label>
                            <select class="w-full border p-2 rounded text-sm dark:bg-gray-700">
                                <option>ত্রুটিপূর্ণ বা ক্ষতিগ্রস্ত পণ্য</option>
                                <option>ভুল পণ্য সরবরাহ করা হয়েছে</option>
                            </select>
                        </div>
                        <div>
                            <label class="block text-xs font-bold mb-1">পণ্যের ছবি আপলোড করুন</label>
                            <input type="file" class="text-xs">
                        </div>
                        <button type="submit" class="bg-spgRed text-white font-bold px-6 py-2 rounded text-sm">রিটার্ন আবেদন জমা দিন</button>
                    </form>
                </div>
            </div>
        </section>
    </main>

    <div id="location-modal" class="fixed inset-0 bg-black/50 hidden items-center justify-center z-50 p-4">
        <div class="bg-white dark:bg-gray-800 rounded-2xl max-w-xl w-full p-6 space-y-4">
            <div class="flex justify-between items-center">
                <h3 class="font-bold text-lg">আপনার ডেলিভারি লোকেশন নির্বাচন করুন</h3>
                <button onclick="closeLocationModal()" class="text-gray-500">✕</button>
            </div>
            <div id="map" class="h-64 w-full rounded-lg border"></div>
            <button onclick="closeLocationModal()" class="w-full bg-spgYellow text-black font-bold py-2 rounded">অবস্থান নিশ্চিত করুন</button>
        </div>
    </div>

    <div class="md:hidden fixed bottom-0 left-0 right-0 bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 flex justify-around py-2 z-50 text-[10px] font-bold">
        <button onclick="switchTab('home')" class="flex flex-col items-center text-spgRed">
            <i data-lucide="home" class="w-5 h-5"></i>
            <span>Home</span>
        </button>
        <button onclick="switchTab('home')" class="flex flex-col items-center text-gray-500">
            <i data-lucide="grid" class="w-5 h-5"></i>
            <span>Categories</span>
        </button>
        <button onclick="switchTab('home')" class="flex flex-col items-center text-gray-500">
            <i data-lucide="flame" class="w-5 h-5"></i>
            <span>Sales</span>
        </button>
        <button onclick="switchTab('account')" class="flex flex-col items-center text-gray-500">
            <i data-lucide="user" class="w-5 h-5"></i>
            <span>Account</span>
        </button>
        <button onclick="switchTab('cart')" class="flex flex-col items-center text-gray-500 relative">
            <i data-lucide="shopping-cart" class="w-5 h-5"></i>
            <span>Cart</span>
            <span class="absolute top-0 right-2 bg-spgRed text-white text-[8px] rounded-full w-3 h-3 flex items-center justify-center">3</span>
        </button>
    </div>

    <script>
        lucide.createIcons();

        function switchTab(tabId) {
            document.getElementById('view-home').classList.add('hidden');
            document.getElementById('view-cart').classList.add('hidden');
            document.getElementById('view-checkout').classList.add('hidden');
            document.getElementById('view-account').classList.add('hidden');

            document.getElementById('view-' + tabId).classList.remove('hidden');
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }

        function toggleDarkMode() {
            document.documentElement.classList.toggle('dark');
        }

        let mapInitialized = false;
        function openLocationModal() {
            document.getElementById('location-modal').classList.remove('hidden');
            document.getElementById('location-modal').classList.add('flex');
            
            if (!mapInitialized) {
                setTimeout(() => {
                    const map = L.map('map').setView([22.3569, 91.7832], 12);
                    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                        maxZoom: 19,
                    }).addTo(map);
                    L.marker([22.3569, 91.7832]).addTo(map).bindPopup('SPG MART Chittagong Main Hub').openPopup();
                    mapInitialized = true;
                }, 200);
            }
        }

        function closeLocationModal() {
            document.getElementById('location-modal').classList.add('hidden');
            document.getElementById('location-modal').classList.remove('flex');
        }
    </script>
</body>
</html>
"""

# API Views
def home_view(request):
    return HttpResponse(HTML_TEMPLATE)

def health_check(request):
    return JsonResponse({
        "status": "online",
        "platform": "SPG MART E-Commerce Platform API",
        "message": "Backend engine is successfully running on Render!"
    })

# URL Routing
urlpatterns = [
    path("", home_view),
    path("api/status/", health_check),
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
