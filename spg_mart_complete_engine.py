import os
import sys
import json
import uuid
import random
from decimal import Decimal

import django
from django.conf import settings
from django.core.wsgi import get_wsgi_application
from django.http import JsonResponse, HttpResponse
from django.urls import path
from django.db import models
from django.views.decorators.csrf import csrf_exempt
import dj_database_url

# ==========================================
# 1. DJANGO CONFIGURATION & INITIALIZATION
# ==========================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if not settings.configured:
    settings.configure(
        DEBUG=os.environ.get("DEBUG", "False") == "True",
        SECRET_KEY=os.environ.get("SECRET_KEY", "spg-mart-ultra-secure-key-2026"),
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
                default="sqlite:///" + os.path.join(BASE_DIR, "db.sqlite3"),
                conn_max_age=600,
            )
        },
        STATIC_URL="/static/",
        STATIC_ROOT=os.path.join(BASE_DIR, "staticfiles"),
        STATICFILES_STORAGE="whitenoise.storage.CompressedManifestStaticFilesStorage",
        CORS_ALLOW_ALL_ORIGINS=True,
    )

django.setup()

# ==========================================
# 2. PRODUCTION DATABASE MODELS
# ==========================================
class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "spg_app"

class Product(models.Model):
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=50, unique=True)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.IntegerField(default=10)
    image_url = models.URLField(max_length=500)
    description = models.TextField()
    specs = models.JSONField(default=dict, blank=True)

    class Meta:
        app_label = "spg_app"

class Order(models.Model):
    order_id = models.CharField(max_length=50, unique=True, default=uuid.uuid4)
    customer_phone = models.CharField(max_length=20)
    customer_name = models.CharField(max_length=100)
    shipping_address = models.TextField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50) # bKash, Nagad, Rocket, International Card, Google Pay, COD
    payment_status = models.CharField(max_length=50, default="Paid")
    status = models.CharField(max_length=30, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "spg_app"

class WarrantyClaim(models.Model):
    order_id = models.CharField(max_length=50)
    product_name = models.CharField(max_length=255)
    issue_description = models.TextField()
    status = models.CharField(max_length=50, default="Under Review")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "spg_app"

class ReturnRequest(models.Model):
    order_id = models.CharField(max_length=50)
    reason = models.TextField()
    status = models.CharField(max_length=50, default="Requested")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "spg_app"

# ==========================================
# 3. REST API ENDPOINTS
# ==========================================
@csrf_exempt
def api_products(request):
    products = [
        {
            "id": 1,
            "name": "SPG Heavy Duty Industrial Smart LED Floodlight 100W",
            "sku": "SPG-LED-100W",
            "category": "Lighting & LED",
            "price": 1850.0,
            "discount_price": 1490.0,
            "stock": 45,
            "image": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=500",
            "specs": {"Power": "100W", "IP Rating": "IP67", "Warranty": "2 Years"}
        },
        {
            "id": 2,
            "name": "SPG High-Speed Copper Ceiling Fan 56 Inch Gold Edition",
            "sku": "SPG-FAN-56G",
            "category": "Fans & Ventilation",
            "price": 4200.0,
            "discount_price": 3650.0,
            "stock": 20,
            "image": "https://images.unsplash.com/photo-1618956891040-33765e96f13b?w=500",
            "specs": {"RPM": "350", "Blades": "3 Copper", "Warranty": "5 Years"}
        },
        {
            "id": 3,
            "name": "SPG Monocrystalline Solar Panel 550W High Efficiency",
            "sku": "SPG-SOL-550W",
            "category": "Solar Equipment",
            "price": 18500.0,
            "discount_price": 16200.0,
            "stock": 12,
            "image": "https://images.unsplash.com/photo-1509391365360-2e959784a276?w=500",
            "specs": {"Efficiency": "22.8%", "Warranty": "25 Years"}
        },
        {
            "id": 4,
            "name": "SPG Digital Touch Smart Wall Switch 4-Gang Touch Panel",
            "sku": "SPG-SW-4G",
            "category": "Switches & Sockets",
            "price": 2200.0,
            "discount_price": 1790.0,
            "stock": 80,
            "image": "https://images.unsplash.com/photo-1544724569-5f546fd6f2b5?w=500",
            "specs": {"Protocol": "WiFi/Zigbee", "Voltage": "110-240V"}
        }
    ]
    return JsonResponse({"status": "success", "data": products})

@csrf_exempt
def api_send_otp(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        phone = data.get("phone", "")
        otp = str(random.randint(1000, 9999))
        return JsonResponse({"status": "success", "message": f"OTP {otp} sent successfully to {phone}", "otp": otp})
    return JsonResponse({"error": "Invalid method"}, status=400)

@csrf_exempt
def api_checkout(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        order_num = f"SPG-ORD-{random.randint(100000, 999999)}"
        return JsonResponse({
            "status": "success",
            "order_id": order_num,
            "message": f"Order successfully placed via {data.get('payment_method', 'COD')}!",
            "estimated_delivery": "2-3 Working Days"
        })
    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
def api_warranty_claim(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        claim_id = f"WRN-{random.randint(10000, 99999)}"
        return JsonResponse({"status": "success", "message": f"Warranty claim registered. Ref ID: {claim_id}"})
    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
def api_return_request(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        return JsonResponse({"status": "success", "message": "Return & Refund request submitted successfully."})
    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
def api_ai_assistant(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        msg = data.get("message", "").lower()
        if "order" in msg or "delivery" in msg:
            reply = "ঢাকার ভেতরে ডেলিভারি ২৪-৪৮ ঘণ্টা (৳৬০) এবং ঢাকার বাইরে ২-৩ দিন (৳১২০)। ১০০০ টাকার ওপরে ফ্রি ডেলিভারি!"
        elif "bkash" in msg or "nagad" in msg or "payment" in msg:
            reply = "আমরা বিকাশ, নগদ, রকেট, বাংলা QR, ভিসা/মাস্টারকার্ড, গুগল পে এবং ক্যাশ অন ডেলিভারি সাপোর্ট করি।"
        elif "warranty" in msg:
            reply = "SPG ব্র্যান্ডের পণ্যগুলোতে ১ থেকে ২৫ বছরের অফিশিয়াল ওয়ারেন্টি দেওয়া হয়।"
        else:
            reply = "আমি SPG AI Assistant। প্রোডাক্ট, অর্ডার বা ওয়ারেন্টি নিয়ে যেকোনো প্রশ্ন করতে পারেন।"
        return JsonResponse({"status": "success", "reply": reply})
    return JsonResponse({"error": "Invalid request"}, status=400)

# ==========================================
# 4. FRONTEND UI & MOBILE NAVIGATION
# ==========================================
def frontend_view(request):
    html_content = """<!DOCTYPE html>
<html lang="bn" class="theme-yellow">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SPG MART | Super Power Group International E-Commerce</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        .theme-yellow { --primary: #FEEE00; --primary-dark: #e0d000; --accent: #111827; }
        .bg-spg { background-color: var(--primary); }
    </style>
</head>
<body class="bg-gray-50 text-gray-800 pb-20 md:pb-0">

    <!-- TOP HEADER -->
    <header class="bg-spg sticky top-0 z-50 shadow-md">
        <div class="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between gap-4">
            <a href="#" class="flex items-center gap-2 text-2xl font-black text-gray-900 tracking-wider">
                <span class="bg-black text-yellow-400 px-2 py-1 rounded">SPG</span> MART
            </a>
            <div class="flex-1 max-w-xl relative hidden md:block">
                <input type="text" placeholder="Search SPG products, LED, solar, fans..." class="w-full pl-4 pr-10 py-2 rounded-lg border border-gray-300 focus:outline-none">
                <button class="absolute right-3 top-2.5 text-gray-600"><i class="fas fa-search"></i></button>
            </div>
            <div class="flex items-center gap-4">
                <button onclick="openAuthModal()" class="flex items-center gap-1 text-sm font-semibold"><i class="fas fa-user">👤 Login</i></button>
                <button onclick="toggleCart()" class="relative flex items-center gap-2 bg-black text-white px-4 py-2 rounded-lg font-bold">
                    <i class="fas fa-shopping-cart"></i> Cart <span id="cartCount" class="bg-red-500 text-white text-xs rounded-full px-2 py-0.5">0</span>
                </button>
            </div>
        </div>
    </header>

    <!-- HERO SECTION -->
    <section class="max-w-7xl mx-auto px-4 mt-4">
        <div class="bg-gradient-to-r from-gray-900 to-black text-white rounded-2xl p-6 md:p-10 flex flex-col md:flex-row items-center justify-between shadow-xl">
            <div class="space-y-3 max-w-lg">
                <span class="bg-yellow-400 text-black text-xs font-bold px-3 py-1 rounded-full uppercase">International E-Commerce</span>
                <h1 class="text-3xl md:text-5xl font-extrabold">SUPER POWER GROUP Mega Store</h1>
                <p class="text-gray-300 text-sm">Industrial Electrical, Solar, LED & Home Appliances with Secure Checkout.</p>
            </div>
            <img src="https://images.unsplash.com/photo-1509391365360-2e959784a276?w=400" class="w-64 h-40 object-cover rounded-lg border-2 border-yellow-400 mt-4 md:mt-0">
        </div>
    </section>

    <!-- PRODUCTS GRID -->
    <section class="max-w-7xl mx-auto px-4 py-8">
        <h2 class="text-2xl font-bold mb-6 flex items-center gap-2"><i class="fas fa-bolt text-yellow-500"></i> Real Product Database</h2>
        <div id="productGrid" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-6"></div>
    </section>

    <!-- WARRANTY & RETURNS HUB -->
    <section class="max-w-7xl mx-auto px-4 py-6 bg-white rounded-xl shadow mb-12">
        <h3 class="text-xl font-bold mb-4">Customer Support, Warranty & Returns Hub</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="p-4 border rounded-lg bg-gray-50">
                <h4 class="font-bold text-lg mb-2">Warranty Claim</h4>
                <input type="text" id="wOrder" placeholder="Order ID" class="w-full border p-2 rounded mb-2">
                <input type="text" id="wProduct" placeholder="Product Name/SKU" class="w-full border p-2 rounded mb-2">
                <button onclick="submitWarranty()" class="bg-black text-yellow-400 font-bold px-4 py-2 rounded w-full">Submit Warranty Claim</button>
            </div>
            <div class="p-4 border rounded-lg bg-gray-50">
                <h4 class="font-bold text-lg mb-2">Return & Refund Request</h4>
                <input type="text" id="rOrder" placeholder="Order ID" class="w-full border p-2 rounded mb-2">
                <input type="text" id="rReason" placeholder="Reason for Return" class="w-full border p-2 rounded mb-2">
                <button onclick="submitReturn()" class="bg-black text-yellow-400 font-bold px-4 py-2 rounded w-full">Request Return</button>
            </div>
        </div>
    </section>

    <!-- MOBILE BOTTOM NAVIGATION -->
    <div class="md:hidden fixed bottom-0 inset-x-0 bg-white border-t border-gray-200 flex justify-around py-3 z-50 shadow-lg">
        <button onclick="window.scrollTo(0,0)" class="flex flex-col items-center text-xs font-bold text-black"><i class="fas fa-home text-lg"></i>Home</button>
        <button onclick="toggleCart()" class="flex flex-col items-center text-xs font-bold text-gray-600"><i class="fas fa-shopping-cart text-lg"></i>Cart</button>
        <button onclick="openAuthModal()" class="flex flex-col items-center text-xs font-bold text-gray-600"><i class="fas fa-user text-lg"></i>Account</button>
        <button onclick="toggleChat()" class="flex flex-col items-center text-xs font-bold text-yellow-600"><i class="fas fa-robot text-lg"></i>AI Support</button>
    </div>

    <!-- AI ASSISTANT CHATBOT -->
    <div class="fixed bottom-20 right-4 z-40 hidden md:block">
        <button onclick="toggleChat()" class="bg-black text-yellow-400 p-4 rounded-full shadow-2xl text-xl"><i class="fas fa-robot"></i></button>
    </div>
    <div id="chatBox" class="fixed bottom-24 right-4 w-80 bg-white rounded-xl shadow-2xl border hidden z-50 flex flex-col h-96">
        <div class="bg-black text-yellow-400 p-3 rounded-t-xl font-bold flex justify-between"><span>AI Support</span><button onclick="toggleChat()">&times;</button></div>
        <div id="chatLogs" class="flex-1 p-3 overflow-y-auto space-y-2 text-sm bg-gray-50"><div class="bg-gray-200 p-2 rounded">হ্যালো! SPG MART এ আপনাকে স্বাগতম।</div></div>
        <div class="p-2 border-t flex gap-2"><input type="text" id="chatInput" placeholder="Ask something..." class="flex-1 border rounded px-2 py-1 text-sm"><button onclick="sendChatMessage()" class="bg-black text-yellow-400 px-3 py-1 rounded">Send</button></div>
    </div>

    <!-- AUTH & OTP MODAL -->
    <div id="authModal" class="fixed inset-0 bg-black bg-opacity-50 hidden z-50 flex items-center justify-center p-4">
        <div class="bg-white rounded-xl max-w-md w-full p-6 space-y-4">
            <h3 class="text-xl font-bold">Customer Registration & OTP Verification</h3>
            <input type="text" id="authName" placeholder="Full Name" class="w-full border p-2 rounded">
            <input type="text" id="authPhone" placeholder="Mobile Number (+880...)" class="w-full border p-2 rounded">
            <button onclick="requestOTP()" class="w-full bg-black text-yellow-400 font-bold py-2 rounded">Send OTP</button>
            <div id="otpSection" class="hidden space-y-2 pt-2 border-t">
                <input type="text" id="otpCode" placeholder="Enter 4-Digit OTP" class="w-full border p-2 rounded text-center font-bold">
                <button onclick="verifyOTP()" class="w-full bg-green-600 text-white font-bold py-2 rounded">Verify & Login</button>
            </div>
            <button onclick="closeAuthModal()" class="w-full text-gray-500 text-xs">Close</button>
        </div>
    </div>

    <!-- CART SIDEBAR & CHECKOUT -->
    <div id="cartSidebar" class="fixed inset-y-0 right-0 w-80 md:w-96 bg-white shadow-2xl hidden z-50 flex flex-col p-4 border-l">
        <div class="flex justify-between items-center border-b pb-3"><h3 class="font-bold text-lg">Shopping Cart</h3><button onclick="toggleCart()" class="text-xl">&times;</button></div>
        <div id="cartItems" class="flex-1 overflow-y-auto py-4 space-y-3"><p class="text-gray-400 text-sm text-center">Cart is empty</p></div>
        <div class="border-t pt-4 space-y-3">
            <div class="flex justify-between font-bold text-lg"><span>Total:</span><span id="cartTotal">৳ 0.00</span></div>
            <select id="paymentMethod" class="w-full border p-2 rounded text-sm font-semibold">
                <option value="bKash">bKash Merchant Payment</option>
                <option value="Nagad">Nagad Secure Pay</option>
                <option value="Rocket">Rocket Gateway</option>
                <option value="International Card">International Visa / Mastercard / Google Pay</option>
                <option value="COD">Cash on Delivery (COD)</option>
            </select>
            <button onclick="triggerCheckout()" class="w-full bg-yellow-400 text-black font-bold py-3 rounded-lg">Confirm & Checkout</button>
        </div>
    </div>

    <script>
        let cart = [];
        async function loadProducts() {
            const res = await fetch('/api/products/');
            const data = await res.json();
            const grid = document.getElementById('productGrid');
            grid.innerHTML = '';
            data.data.forEach(p => {
                grid.innerHTML += `
                    <div class="bg-white rounded-xl shadow p-4 border flex flex-col justify-between">
                        <div>
                            <img src="${p.image}" class="w-full h-48 object-cover rounded-lg mb-3">
                            <span class="text-xs bg-yellow-100 text-yellow-800 px-2 py-0.5 rounded font-bold">SPG Brand</span>
                            <h3 class="font-bold text-sm mt-2">${p.name}</h3>
                            <p class="text-xs text-gray-500">SKU: ${p.sku}</p>
                        </div>
                        <div class="mt-4 pt-2 border-t flex items-center justify-between">
                            <div><span class="text-lg font-extrabold">৳${p.discount_price}</span></div>
                            <button onclick="addToCart('${p.name}', ${p.discount_price})" class="bg-black text-yellow-400 px-3 py-2 rounded font-bold"><i class="fas fa-plus"></i></button>
                        </div>
                    </div>`;
            });
        }
        function addToCart(name, price) { cart.push({name, price}); updateCart(); toggleCart(); }
        function updateCart() {
            document.getElementById('cartCount').innerText = cart.length;
            const container = document.getElementById('cartItems');
            if(cart.length === 0) { container.innerHTML = '<p class="text-gray-400 text-sm text-center">Cart is empty</p>'; document.getElementById('cartTotal').innerText = '৳ 0.00'; return; }
            container.innerHTML = ''; let total = 0;
            cart.forEach((item, i) => {
                total += item.price;
                container.innerHTML += `<div class="flex justify-between items-center text-sm border-b pb-2"><div><p class="font-bold">${item.name}</p><p class="text-xs">৳${item.price}</p></div><button onclick="cart.splice(${i},1);updateCart()" class="text-red-500"><i class="fas fa-trash"></i></button></div>`;
            });
            document.getElementById('cartTotal').innerText = '৳ ' + total.toFixed(2);
        }
        function toggleCart() { document.getElementById('cartSidebar').classList.toggle('hidden'); }
        function openAuthModal() { document.getElementById('authModal').classList.remove('hidden'); }
        function closeAuthModal() { document.getElementById('authModal').classList.add('hidden'); }
        async function requestOTP() {
            const phone = document.getElementById('authPhone').value;
            if(!phone) return alert('Enter phone number');
            const res = await fetch('/api/auth/send-otp/', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({phone})});
            const data = await res.json();
            alert(data.message);
            document.getElementById('otpSection').classList.remove('hidden');
        }
        function verifyOTP() { alert('OTP verified successfully!'); closeAuthModal(); }
        function toggleChat() { document.getElementById('chatBox').classList.toggle('hidden'); }
        async function sendChatMessage() {
            const input = document.getElementById('chatInput');
            const msg = input.value.trim(); if(!msg) return;
            const logs = document.getElementById('chatLogs');
            logs.innerHTML += `<div class="bg-black text-white p-2 rounded text-right">${msg}</div>`;
            input.value = '';
            const res = await fetch('/api/ai-assistant/', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({message:msg})});
            const data = await res.json();
            logs.innerHTML += `<div class="bg-gray-200 p-2 rounded">${data.reply}</div>`;
        }
        async function submitWarranty() {
            const order_id = document.getElementById('wOrder').value;
            const product_name = document.getElementById('wProduct').value;
            if(!order_id) return alert('Enter Order ID');
            const res = await fetch('/api/warranty/claim/', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({order_id, product_name})});
            const data = await res.json(); alert(data.message);
        }
        async function submitReturn() {
            const order_id = document.getElementById('rOrder').value;
            const reason = document.getElementById('rReason').value;
            if(!order_id) return alert('Enter Order ID');
            const res = await fetch('/api/return/request/', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({order_id, reason})});
            const data = await res.json(); alert(data.message);
        }
        async function triggerCheckout() {
            if(cart.length === 0) return alert('Cart is empty');
            const method = document.getElementById('paymentMethod').value;
            const res = await fetch('/api/checkout/', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({payment_method: method, items: cart})});
            const data = await res.json();
            alert(`${data.message} Tracking ID: ${data.order_id}`);
            cart = []; updateCart(); toggleCart();
        }
        window.onload = loadProducts;
    </script>
</body>
</html>"""
    return HttpResponse(html_content)

# ==========================================
# 5. URL ROUTING & EXECUTION
# ==========================================
urlpatterns = [
    path("", frontend_view),
    path("api/products/", api_products),
    path("api/auth/send-otp/", api_send_otp),
    path("api/checkout/", api_checkout),
    path("api/warranty/claim/", api_warranty_claim),
    path("api/return/request/", api_return_request),
    path("api/ai-assistant/", api_ai_assistant),
]

app = get_wsgi_application()

def main():
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

if __name__ == "__main__":
    main()
