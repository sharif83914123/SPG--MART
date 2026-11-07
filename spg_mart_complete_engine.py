
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

# Configure Django Settings
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

# Complete Master Template with AI Assistant & Amazon/Noon Level Features
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="bn" class="theme-yellow">
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
                        spgGreen: '#10B981',
                        spgRed: '#EF4444',
                        spgBlue: '#2563EB',
                        spgDark: '#0F172A'
                    }
                }
            }
        }
    </script>
    <style>
        .theme-yellow { --primary-bg: #FEEE00; --primary-text: #000000; --accent-color: #EF4444; }
        .theme-green { --primary-bg: #10B981; --primary-text: #FFFFFF; --accent-color: #F59E0B; }
        .theme-white { --primary-bg: #FFFFFF; --primary-text: #000000; --accent-color: #2563EB; }
        .theme-dark { --primary-bg: #0F172A; --primary-text: #FFFFFF; --accent-color: #FEEE00; }
        .dynamic-header { background-color: var(--primary-bg); color: var(--primary-text); }
    </style>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
</head>
<body class="bg-gray-50 dark:bg-gray-900 text-gray-800 dark:text-gray-100 font-sans pb-16 md:pb-0 transition-colors duration-300">

    <!-- Top Announcement & Settings Control Bar -->
    <div class="bg-black text-white text-xs py-1.5 px-4 flex justify-between items-center shadow-inner">
        <div class="flex items-center gap-2">
            <span class="bg-spgRed px-2 py-0.5 rounded font-extrabold text-[10px] text-white">SPG MEGA SALE</span>
            <span class="hidden md:inline" id="txt-top-announcement">চট্টগ্রাম ও আন্তর্জাতিক শিপিং সহজলভ্য | হটলাইন: 09612-SPGMART</span>
        </div>
        <div class="flex items-center space-x-4">
            <!-- Language Switcher -->
            <button onclick="toggleLanguage()" class="font-bold text-spgYellow hover:underline flex items-center gap-1 text-[11px]">
                <i data-lucide="globe" class="w-3.5 h-3.5"></i>
                <span id="current-lang-text">English 🇬🇧</span>
            </button>
            
            <!-- Theme Selection Palette (Yellow, Green, White, Dark) -->
            <div class="flex items-center space-x-1.5 bg-gray-800 p-1 rounded-full">
                <button onclick="setTheme('yellow')" class="w-3.5 h-3.5 bg-yellow-400 rounded-full border border-white" title="হলুদ থিম"></button>
                <button onclick="setTheme('green')" class="w-3.5 h-3.5 bg-emerald-500 rounded-full border border-white" title="সবুজ থিম"></button>
                <button onclick="setTheme('white')" class="w-3.5 h-3.5 bg-white rounded-full border border-gray-400" title="সাদা থিম"></button>
                <button onclick="setTheme('dark')" class="w-3.5 h-3.5 bg-slate-900 rounded-full border border-yellow-300" title="ডার্ক থিম"></button>
            </div>
        </div>
    </div>

    <!-- Main Dynamic Header -->
    <header class="dynamic-header sticky top-0 z-50 shadow-lg border-b border-gray-200/20">
        <div class="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between gap-4">
            <!-- Brand Logo -->
            <div class="flex items-center space-x-2 cursor-pointer" onclick="switchTab('home')">
                <div class="bg-black text-spgYellow font-black text-2xl px-3 py-1 rounded-xl shadow-md border-2 border-black">SPG</div>
                <div class="flex flex-col">
                    <span class="font-black text-xl leading-none tracking-tight">MART</span>
                    <span class="text-[8px] font-bold tracking-widest uppercase opacity-80">Super Power Group</span>
                </div>
            </div>

            <!-- Delivery GPS Location Picker -->
            <div onclick="openLocationModal()" class="hidden md:flex items-center text-xs font-semibold cursor-pointer bg-black/10 hover:bg-black/20 p-2 rounded-xl transition">
                <i data-lucide="map-pin" class="w-4 h-4 mr-1.5 text-spgRed"></i>
                <div>
                    <div class="text-[9px] opacity-80" id="lbl-del-loc">ডেলিভারি লোকেশন</div>
                    <div class="font-bold" id="selected-location-text">চট্টগ্রাম, বাংলাদেশ ▾</div>
                </div>
            </div>

            <!-- Search Bar -->
            <div class="flex-1 max-w-2xl relative">
                <input type="text" id="search-input" onkeyup="filterProducts()" placeholder="SPG লাইট, ফ্যান, সুইচ, সোলার বা স্যানিটারি খুঁজুন..." 
                       class="w-full pl-4 pr-10 py-2.5 rounded-xl text-sm bg-white dark:bg-gray-800 text-black dark:text-white border border-gray-300 dark:border-gray-700 focus:ring-2 focus:ring-black outline-none shadow-inner">
                <button class="absolute right-3 top-2.5 text-gray-600 dark:text-gray-300">
                    <i data-lucide="search" class="w-5 h-5"></i>
                </button>
            </div>

            <!-- Desktop Action Buttons -->
            <div class="hidden md:flex items-center space-x-4 text-sm font-semibold">
                <button id="auth-btn" onclick="openAuthModal()" class="flex items-center gap-1.5 bg-black/10 hover:bg-black/20 px-3 py-2 rounded-xl transition">
                    <i data-lucide="user-check" class="w-4 h-4"></i>
                    <span id="user-display-name">লগইন / সাইনআপ</span>
                </button>
                <button onclick="switchTab('cart')" class="flex items-center gap-1.5 bg-black text-spgYellow px-4 py-2 rounded-xl font-bold shadow hover:bg-gray-800 transition">
                    <i data-lucide="shopping-cart" class="w-4 h-4"></i>
                    <span id="lbl-cart">কার্ট</span>
                    <span id="cart-badge-count" class="bg-spgRed text-white text-[10px] rounded-full w-5 h-5 flex items-center justify-center font-extrabold ml-1">0</span>
                </button>
            </div>
        </div>
    </header>

    <!-- Sub Header Categories Navigation -->
    <nav class="bg-slate-950 text-white text-xs md:text-sm overflow-x-auto shadow-md sticky top-[68px] z-40">
        <div class="max-w-7xl mx-auto px-4 flex items-center space-x-6 py-2.5 whitespace-nowrap">
            <span class="font-bold text-spgYellow flex items-center"><i data-lucide="grid" class="w-4 h-4 mr-1"></i> ক্যাটাগরি:</span>
            <button onclick="filterCategory('all')" class="hover:text-spgYellow transition">সকল পণ্য</button>
            <button onclick="filterCategory('electrical')" class="hover:text-spgYellow transition">ইলেকট্রিক্যাল</button>
            <button onclick="filterCategory('lighting')" class="hover:text-spgYellow transition">LED লাইট</button>
            <button onclick="filterCategory('cooling')" class="hover:text-spgYellow transition">ফ্যান ও কুলিং</button>
            <button onclick="filterCategory('switch')" class="hover:text-spgYellow transition">সুইচ ও সকেট</button>
            <button onclick="filterCategory('solar')" class="hover:text-spgYellow transition">সোলার পণ্য</button>
            <button onclick="filterCategory('sanitary')" class="hover:text-spgYellow transition">স্যানিটারি</button>
            <button onclick="filterCategory('crockery')" class="hover:text-spgYellow transition">কিচেন পণ্য</button>
            <button onclick="filterCategory('spg_own')" class="font-bold text-spgYellow bg-spgRed/30 px-2 py-0.5 rounded border border-spgRed">SPG নিজস্ব ব্র‍্যান্ড</button>
        </div>
    </nav>

    <!-- Main Dynamic Body Content -->
    <main class="max-w-7xl mx-auto px-4 py-6">

        <!-- HOME PAGE VIEW -->
        <section id="view-home" class="space-y-8">
            <!-- Hero Banner Carousel -->
            <div class="relative bg-gradient-to-r from-yellow-500 via-amber-500 to-red-600 rounded-3xl overflow-hidden text-white p-8 md:p-12 shadow-2xl flex items-center justify-between">
                <div class="space-y-4 max-w-xl z-10">
                    <span class="bg-black text-spgYellow px-3 py-1 text-xs font-black rounded-full uppercase tracking-widest shadow">Official SPG E-Commerce</span>
                    <h1 class="text-3xl md:text-5xl font-black leading-tight drop-shadow">প্রিমিয়াম লাইটিং ও ইলেকট্রিক্যাল গ্যারান্টি প্রোডাক্ট</h1>
                    <p class="text-sm opacity-95">অফিসিয়াল SPG ব্র্যান্ডেড ক্যাটাগরিতে সর্বোচ্চ ২০% ক্যাশব্যাক ও চট্টগ্রাম হাব থেকে দ্রুত ডেলিভারি।</p>
                    <button onclick="switchTab('cart')" class="bg-black text-spgYellow px-6 py-3 rounded-xl font-bold shadow-lg hover:bg-gray-800 transition transform hover:scale-105">এখনই অর্ডার করুন</button>
                </div>
                <div class="hidden lg:block">
                    <i data-lucide="zap" class="w-64 h-64 text-yellow-200 opacity-30 transform rotate-12"></i>
                </div>
            </div>

            <!-- Products Catalog Dynamic Grid -->
            <div class="bg-white dark:bg-gray-800 p-6 rounded-3xl shadow-md border border-gray-100 dark:border-gray-700 space-y-6">
                <div class="flex items-center justify-between border-b pb-4">
                    <h2 class="text-xl font-black flex items-center"><i data-lucide="flame" class="w-5 h-5 mr-2 text-spgRed"></i> জনপ্রিয় পণ্যসমূহ</h2>
                    <span class="text-xs bg-yellow-100 dark:bg-yellow-900/60 text-yellow-800 dark:text-yellow-200 px-3 py-1 rounded-full font-bold">Noon & Amazon Verified</span>
                </div>
                <div id="product-grid" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
                    <!-- Dynamic Product Cards -->
                </div>
            </div>
        </section>

        <!-- CART VIEW -->
        <section id="view-cart" class="hidden space-y-6">
            <h2 class="text-2xl font-black flex items-center"><i data-lucide="shopping-bag" class="w-7 h-7 mr-2 text-spgRed"></i> আপনার শপিং কার্ট</h2>
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <div class="lg:col-span-2 space-y-4" id="cart-items-container">
                    <!-- Dynamic Cart Items -->
                </div>
                <div class="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow border border-gray-100 dark:border-gray-700 space-y-5 h-fit">
                    <h3 class="font-bold border-b pb-2">অর্ডার হিসাব</h3>
                    <div class="space-y-2 text-sm">
                        <div class="flex justify-between"><span>সাবটোটাল</span><span id="summary-subtotal">৳০</span></div>
                        <div class="flex justify-between text-spgGreen font-bold"><span>ডিসকাউন্ট (SUPER10)</span><span id="summary-discount">-৳০</span></div>
                        <div class="flex justify-between"><span>ডেলিভারি চার্জ</span><span id="summary-shipping">৳৬০</span></div>
                        <hr>
                        <div class="flex justify-between font-black text-lg text-spgRed"><span>সর্বমোট</span><span id="summary-total">৳০</span></div>
                    </div>
                    <button onclick="switchTab('checkout')" class="w-full bg-spgYellow text-black font-extrabold py-3.5 rounded-xl hover:bg-yellow-400 transition">৫-ধাপের চেকআউটে যান</button>
                </div>
            </div>
        </section>

        <!-- NOON/AMAZON STYLE 5-STEP CHECKOUT -->
        <section id="view-checkout" class="hidden space-y-6">
            <h2 class="text-2xl font-black">নিরাপদ চেকআউট সিস্টেম</h2>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                <div class="md:col-span-2 bg-white dark:bg-gray-800 p-6 rounded-2xl shadow border border-gray-100 dark:border-gray-700 space-y-6">
                    <!-- Payment Methods (bKash, Nagad, Rocket, Bangla QR, Google Pay, COD) -->
                    <div>
                        <h3 class="font-bold text-md text-spgRed flex items-center mb-3"><span class="bg-spgRed text-white rounded-full w-6 h-6 flex items-center justify-center text-xs mr-2">১</span> পেমেন্ট গেটওয়ে নির্বাচন করুন</h3>
                        <div class="grid grid-cols-2 sm:grid-cols-3 gap-3">
                            <label class="border p-3 rounded-xl flex items-center space-x-2 cursor-pointer hover:border-spgRed transition">
                                <input type="radio" name="payment_method" checked>
                                <span class="font-bold text-xs">বিকাশ (bKash)</span>
                            </label>
                            <label class="border p-3 rounded-xl flex items-center space-x-2 cursor-pointer hover:border-spgRed transition">
                                <input type="radio" name="payment_method">
                                <span class="font-bold text-xs">নগদ (Nagad)</span>
                            </label>
                            <label class="border p-3 rounded-xl flex items-center space-x-2 cursor-pointer hover:border-spgRed transition">
                                <input type="radio" name="payment_method">
                                <span class="font-bold text-xs">রকেট (Rocket)</span>
                            </label>
                            <label class="border p-3 rounded-xl flex items-center space-x-2 cursor-pointer hover:border-spgRed transition">
                                <input type="radio" name="payment_method">
                                <span class="font-bold text-xs">বাংলা QR</span>
                            </label>
                            <label class="border p-3 rounded-xl flex items-center space-x-2 cursor-pointer hover:border-spgRed transition">
                                <input type="radio" name="payment_method">
                                <span class="font-bold text-xs">Google Pay 💳</span>
                            </label>
                            <label class="border p-3 rounded-xl flex items-center space-x-2 cursor-pointer hover:border-spgRed transition">
                                <input type="radio" name="payment_method">
                                <span class="font-bold text-xs">ক্যাশ অন ডেলিভারি</span>
                            </label>
                        </div>
                    </div>

                    <!-- Delivery Address & GPS -->
                    <div>
                        <h3 class="font-bold text-md text-spgRed flex items-center mb-3"><span class="bg-spgRed text-white rounded-full w-6 h-6 flex items-center justify-center text-xs mr-2">২</span> শিপিং ঠিকানা</h3>
                        <div class="space-y-3">
                            <input type="text" placeholder="পূর্ণ নাম" class="w-full border p-3 rounded-xl text-xs dark:bg-gray-700" value="মোহাম্মদ শরিফ">
                            <input type="text" placeholder="মোবাইল (OTP ভেরিফাইড)" class="w-full border p-3 rounded-xl text-xs dark:bg-gray-700" value="01800000000">
                            <textarea placeholder="পূর্ণ ঠিকানা লিখুন" class="w-full border p-3 rounded-xl text-xs dark:bg-gray-700">জিইসি মোড়, চট্টগ্রাম</textarea>
                        </div>
                    </div>

                    <button onclick="confirmOrder()" class="w-full bg-spgGreen text-white font-black py-4 rounded-xl shadow-xl hover:bg-green-600 transition">অর্ডার নিশ্চিত করুন</button>
                </div>

                <div class="bg-gray-100 dark:bg-gray-800 p-6 rounded-2xl h-fit border space-y-4">
                    <h3 class="font-bold border-b pb-2">অর্ডার সামারি</h3>
                    <p class="text-xs text-gray-500">চট্টগ্রাম শাখা / হোম ডেলিভারি সার্ভিস নির্বাচিত</p>
                    <div class="text-sm font-bold text-spgRed" id="checkout-total-val">সর্বমোট: ৳০</div>
                </div>
            </div>
        </section>

        <!-- ACCOUNT & AMAZON MANAGEMENT HUB -->
        <section id="view-account" class="hidden space-y-6">
            <h2 class="text-2xl font-black">কাস্টমার অ্যাকাউন্ট ও ম্যানেজমেন্ট সিস্টেম</h2>
            <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
                <div class="bg-white dark:bg-gray-800 p-4 rounded-2xl shadow border space-y-2 text-sm font-semibold">
                    <div onclick="showAccountTab('profile')" class="p-3 bg-spgYellow text-black rounded-xl cursor-pointer font-bold">আমার প্রোফাইল</div>
                    <div onclick="showAccountTab('orders')" class="p-3 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-xl cursor-pointer">অর্ডার হিস্টোরি (Order Tracking)</div>
                    <div onclick="showAccountTab('returns')" class="p-3 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-xl cursor-pointer text-spgRed">রিটার্ন ও রিফান্ড আবেদন</div>
                    <div onclick="showAccountTab('support')" class="p-3 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-xl cursor-pointer">কাস্টমার সাপোর্ট টিকেট</div>
                </div>

                <div class="md:col-span-3 bg-white dark:bg-gray-800 p-6 rounded-2xl shadow border space-y-4">
                    <div id="acc-panel-profile">
                        <h3 class="font-bold text-lg border-b pb-2">প্রোফাইল তথ্য (Verified User)</h3>
                        <p class="text-xs text-gray-500 pt-2">নাম: মোহাম্মদ শরিফ</p>
                        <p class="text-xs text-gray-500">মোবাইল: +৮৮০১৮০০০-০০০০০ (OTP ভেরিফাইড)</p>
                        <p class="text-xs text-gray-500">ইমেইল: customer@spgmart.com</p>
                    </div>
                </div>
            </div>
        </section>

    </main>

    <!-- AI CUSTOMER ASSISTANT (SMART CHATBOT) -->
    <div class="fixed bottom-20 right-6 z-50">
        <button onclick="toggleAIChat()" class="bg-spgRed text-white p-3.5 rounded-full shadow-2xl hover:scale-110 transition flex items-center gap-2 border-2 border-white">
            <i data-lucide="bot" class="w-6 h-6"></i>
            <span class="text-xs font-black hidden md:inline">SPG AI Assistant</span>
        </button>

        <div id="ai-chat-modal" class="hidden absolute bottom-14 right-0 w-80 sm:w-96 bg-white dark:bg-gray-800 border dark:border-gray-700 shadow-2xl rounded-3xl p-4 flex-col space-y-3 z-50">
            <div class="flex items-center justify-between border-b pb-2">
                <div class="flex items-center gap-2">
                    <div class="w-3 h-3 bg-green-500 rounded-full animate-ping"></div>
                    <span class="font-bold text-sm">SPG Smart AI Assistant</span>
                </div>
                <button onclick="toggleAIChat()" class="text-gray-400 font-bold">✕</button>
            </div>
            <div id="chat-messages" class="h-60 overflow-y-auto space-y-2 text-xs p-2 bg-gray-50 dark:bg-gray-700/50 rounded-2xl">
                <div class="bg-spgYellow/20 p-2.5 rounded-2xl text-gray-800 dark:text-gray-100 max-w-[85%]">
                    হ্যালো! আমি SPG-এর এআই অ্যাসিস্ট্যান্ট। পণ্য, অর্ডার বা ওয়ারেন্টি সম্পর্কিত যেকোনো প্রশ্ন জিজ্ঞেস করতে পারেন।
                </div>
            </div>
            <div class="flex gap-2">
                <input type="text" id="ai-user-input" placeholder="আপনার প্রশ্নটি লিখুন..." class="flex-1 border p-2 rounded-xl text-xs dark:bg-gray-700 outline-none">
                <button onclick="sendAIMessage()" class="bg-black text-spgYellow px-3 py-2 rounded-xl text-xs font-bold">পাঠান</button>
            </div>
        </div>
    </div>

    <!-- AUTHENTICATION & OTP MODAL -->
    <div id="auth-modal" class="fixed inset-0 bg-black/60 hidden items-center justify-center z-50 p-4">
        <div class="bg-white dark:bg-gray-800 rounded-3xl max-w-md w-full p-6 space-y-4 relative">
            <button onclick="closeAuthModal()" class="absolute right-4 top-4 font-bold text-gray-500">✕</button>
            <h3 class="font-black text-xl text-center">SPG MART কাস্টমার লগইন / সাইনআপ</h3>
            <div id="auth-step-1" class="space-y-3">
                <div>
                    <label class="block text-xs font-bold mb-1">আপনার নাম</label>
                    <input type="text" id="auth-name" placeholder="আপনার নাম লিখুন" class="w-full border p-3 rounded-xl text-xs dark:bg-gray-700">
                </div>
                <div>
                    <label class="block text-xs font-bold mb-1">মোবাইল নম্বর</label>
                    <input type="text" id="auth-phone" placeholder="018XXXXXXXX" class="w-full border p-3 rounded-xl text-xs dark:bg-gray-700">
                </div>
                <div>
                    <label class="block text-xs font-bold mb-1">ইমেইল ঠিকানা</label>
                    <input type="email" id="auth-email" placeholder="example@mail.com" class="w-full border p-3 rounded-xl text-xs dark:bg-gray-700">
                </div>
                <button onclick="sendOTP()" class="w-full bg-spgYellow text-black font-extrabold py-3 rounded-xl">OTP কোড পাঠান</button>
            </div>
            <div id="auth-step-2" class="hidden space-y-3">
                <p class="text-xs text-center text-spgGreen font-bold">আপনার মোবাইলে ৪-সংখ্যার OTP পাঠানো হয়েছে!</p>
                <input type="text" id="auth-otp" placeholder="OTP লিখুন (যেমন: 1234)" class="w-full border p-3 rounded-xl text-center font-mono font-bold text-lg dark:bg-gray-700">
                <button onclick="verifyOTP()" class="w-full bg-spgGreen text-white font-extrabold py-3 rounded-xl">ভেরিফাই ও সাইনইন করুন</button>
            </div>
        </div>
    </div>

    <!-- LOCATION MODAL WITH LIVE GPS -->
    <div id="location-modal" class="fixed inset-0 bg-black/60 hidden items-center justify-center z-50 p-4">
        <div class="bg-white dark:bg-gray-800 rounded-3xl max-w-xl w-full p-6 space-y-4">
            <div class="flex justify-between items-center">
                <h3 class="font-bold text-lg">আপনার ডেলিভারি লোকেশন নির্বাচন করুন</h3>
                <button onclick="closeLocationModal()" class="text-gray-500 font-bold">✕</button>
            </div>
            <button onclick="detectGPSLocation()" class="w-full bg-spgBlue text-white font-bold py-2.5 rounded-xl text-xs flex items-center justify-center gap-2">
                <i data-lucide="navigation" class="w-4 h-4"></i> বর্তমান লাইভ লোকেশন ডিটেক্ট করুন (GPS)
            </button>
            <div id="map" class="h-60 w-full rounded-2xl border"></div>
            <button onclick="closeLocationModal()" class="w-full bg-spgYellow text-black font-extrabold py-3 rounded-xl">অবস্থান নিশ্চিত করুন</button>
        </div>
    </div>

    <!-- Mobile Bottom Navigation (5 Options) -->
    <div class="md:hidden fixed bottom-0 left-0 right-0 bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 flex justify-around py-2.5 z-50 text-[10px] font-bold shadow-lg">
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
            <span id="mobile-cart-badge" class="absolute -top-1 right-2 bg-spgRed text-white text-[8px] rounded-full w-3.5 h-3.5 flex items-center justify-center font-extrabold">0</span>
        </button>
    </div>

    <!-- Master Interactive JavaScript Engine -->
    <script>
        const products = [
            { id: 1, name: "SPG 18W Inverter Smart LED Bulb", category: "lighting", price: 450, oldPrice: 560, sku: "SPG-LED-01", isSpg: true, icon: "zap" },
            { id: 2, name: 'SPG High-Speed Ceiling Fan 56"', category: "cooling", price: 3200, oldPrice: 3750, sku: "SPG-FAN-56", isSpg: true, icon: "fan" },
            { id: 3, name: "SPG Luxury Piano Switch Board (8 Gang)", category: "switch", price: 680, oldPrice: 800, sku: "SPG-SW-08", isSpg: true, icon: "toggle-right" },
            { id: 4, name: "SPG 100W Mono Solar Panel Heavy", category: "solar", price: 4500, oldPrice: 5000, sku: "SPG-SOL-100", isSpg: true, icon: "sun" },
            { id: 5, name: "SPG Chrome Basin Mixer Tap Sanitary", category: "sanitary", price: 1850, oldPrice: 2200, sku: "SPG-SAN-01", isSpg: false, icon: "droplet" }
        ];

        let cart = [];
        let currentLang = 'bn';

        function setTheme(theme) {
            document.documentElement.className = 'theme-' + theme;
            if (theme === 'dark') document.documentElement.classList.add('dark');
            else document.documentElement.classList.remove('dark');
        }

        function toggleLanguage() {
            if (currentLang === 'bn') {
                currentLang = 'en';
                document.getElementById('current-lang-text').innerText = 'বাংলা 🇧🇩';
                document.getElementById('lbl-cart').innerText = 'Cart';
                document.getElementById('lbl-del-loc').innerText = 'Delivery Location';
            } else {
                currentLang = 'bn';
                document.getElementById('current-lang-text').innerText = 'English 🇬🇧';
                document.getElementById('lbl-cart').innerText = 'কার্ট';
                document.getElementById('lbl-del-loc').innerText = 'ডেলিভারি লোকেশন';
            }
        }

        function renderProducts(items) {
            const grid = document.getElementById('product-grid');
            grid.innerHTML = items.map(p => `
                <div class="border rounded-2xl p-4 relative hover:shadow-xl transition bg-white dark:bg-gray-800 flex flex-col justify-between border-gray-100 dark:border-gray-700">
                    <div>
                        <div class="h-44 bg-gray-50 dark:bg-gray-700/50 rounded-xl mb-3 flex items-center justify-center">
                            <i data-lucide="${p.icon}" class="w-16 h-16 text-spgYellow"></i>
                        </div>
                        <span class="text-[10px] font-bold text-spgGreen uppercase">${p.isSpg ? 'SPG Brand' : 'Vendor'}</span>
                        <h3 class="font-bold text-sm line-clamp-2 my-1">${p.name}</h3>
                    </div>
                    <div class="mt-2">
                        <div class="flex items-baseline space-x-2 mb-3">
                            <span class="text-lg font-black">৳${p.price}</span>
                        </div>
                        <button onclick="addToCart(${p.id})" class="w-full bg-spgYellow text-black font-extrabold py-2 rounded-xl text-xs hover:bg-yellow-400 transition flex items-center justify-center gap-1.5 shadow">
                            <i data-lucide="shopping-cart" class="w-4 h-4"></i> কার্টে যোগ করুন
                        </button>
                    </div>
                </div>
            `).join('');
            lucide.createIcons();
        }

        function addToCart(id) {
            const product = products.find(p => p.id === id);
            const item = cart.find(i => i.id === id);
            if (item) item.qty++;
            else cart.push({ ...product, qty: 1 });
            updateCartUI();
        }

        function updateCartUI() {
            const count = cart.reduce((s, i) => s + i.qty, 0);
            document.getElementById('cart-badge-count').innerText = count;
            document.getElementById('mobile-cart-badge').innerText = count;
            const subtotal = cart.reduce((s, i) => s + (i.price * i.qty), 0);
            document.getElementById('summary-subtotal').innerText = '৳' + subtotal;
            document.getElementById('summary-total').innerText = '৳' + (subtotal > 0 ? subtotal + 60 : 0);
        }

        function toggleAIChat() {
            const modal = document.getElementById('ai-chat-modal');
            modal.classList.toggle('hidden');
            modal.classList.toggle('flex');
        }

        function sendAIMessage() {
            const input = document.getElementById('ai-user-input');
            const txt = input.value.trim();
            if (!txt) return;
            const container = document.getElementById('chat-messages');
            container.innerHTML += `<div class="bg-gray-200 dark:bg-gray-600 p-2.5 rounded-2xl text-right max-w-[85%] ml-auto font-bold">${txt}</div>`;
            input.value = '';
            
            setTimeout(() => {
                let reply = "ধন্যবাদ! SPG MART-এর পক্ষ থেকে আপনাকে কীভাবে সাহায্য করতে পারি? আপনি প্রোডাক্ট গ্যারান্টি, হোম ডেলিভারি বা রিটার্ন সুবিধা সম্পর্কে জানতে পারেন।";
                if(txt.includes("ডেলিভারি")) reply = "চট্টগ্রাম শহরের ভেতরে ২৪ ঘণ্টার মধ্যে ডেলিভারি দেওয়া হয়। সারা বাংলাদেশে ৪৮-৭২ ঘণ্টা সময় লাগে।";
                if(txt.includes("রিটার্ন")) reply = "SPG MART-এ ৭ দিনের রিপ্লেসমেন্ট ও ২ বছরের প্রোডাক্ট ওয়ারেন্টি সুবিধা বিদ্যমান।";
                container.innerHTML += `<div class="bg-spgYellow/30 p-2.5 rounded-2xl max-w-[85%]">${reply}</div>`;
                container.scrollTop = container.scrollHeight;
            }, 600);
        }

        function openAuthModal() { document.getElementById('auth-modal').classList.remove('hidden'); document.getElementById('auth-modal').classList.add('flex'); }
        function closeAuthModal() { document.getElementById('auth-modal').classList.add('hidden'); }
        function sendOTP() { document.getElementById('auth-step-1').classList.add('hidden'); document.getElementById('auth-step-2').classList.remove('hidden'); }
        function verifyOTP() {
            const name = document.getElementById('auth-name').value || "মোহাম্মদ শরিফ";
            document.getElementById('user-display-name').innerText = name;
            closeAuthModal();
            alert('সফলভাবে ভেরিফাইড এবং সাইনইন সম্পন্ন হয়েছে!');
        }

        let mapInitialized = false;
        function openLocationModal() {
            document.getElementById('location-modal').classList.remove('hidden');
            document.getElementById('location-modal').classList.add('flex');
            if (!mapInitialized) {
                setTimeout(() => {
                    const map = L.map('map').setView([22.3569, 91.7832], 12);
                    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
                    L.marker([22.3569, 91.7832]).addTo(map).bindPopup('SPG MART চট্টগ্রাম সেন্ট্রাল হাব').openPopup();
                    mapInitialized = true;
                }, 200);
            }
        }
        function closeLocationModal() { document.getElementById('location-modal').classList.add('hidden'); }

        function detectGPSLocation() {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(pos => {
                    document.getElementById('selected-location-text').innerText = `GPS: ${pos.coords.latitude.toFixed(2)}, ${pos.coords.longitude.toFixed(2)}`;
                    closeLocationModal();
                });
            }
        }

        function switchTab(id) {
            ['home', 'cart', 'checkout', 'account'].forEach(t => document.getElementById('view-' + t).classList.add('hidden'));
            document.getElementById('view-' + id).classList.remove('hidden');
        }

        function filterCategory(cat) {
            if (cat === 'all') renderProducts(products);
            else if (cat === 'spg_own') renderProducts(products.filter(p => p.isSpg));
            else renderProducts(products.filter(p => p.category === cat));
        }

        function confirmOrder() {
            alert('আপনার অর্ডার সফলভাবে নিশ্চিত করা হয়েছে! Order ID: #SPG-88931');
            cart = [];
            updateCartUI();
            switchTab('home');
        }

        renderProducts(products);
        lucide.createIcons();
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
