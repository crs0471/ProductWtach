from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
from watch.models import ProductWatch, ProductHistory
from . import func
import random 
request_ = requests.Session()

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/600.7.12 (KHTML, like Gecko) Version/8.0.7 Safari/600.7.12",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/7.1.8 Safari/537.85.17",
    "Mozilla/5.0 (iPad; CPU OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H143 Safari/600.1.4",
    "Mozilla/5.0 (iPad; CPU OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12F69 Safari/600.1.4",
    "Mozilla/5.0 (Windows NT 6.1; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)",
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
]

def product_details_scrap():
    print(f"[Info] Cron started at {datetime.now()}")
    # Your code here
    try:
        all_active_products = ProductWatch.objects.filter(is_active=True)

        for product in all_active_products:
            now = func.now()
            if ProductHistory.objects.filter(product_watch=product, created_at__gte=(now-timedelta(minutes=5))).exists():
                continue
            
            headers = {'User-Agent': random.choice(user_agents),}
            req = request_.get(product.url, )
            while req.status_code != 200:
                headers = {'User-Agent': random.choice(user_agents),}
                req = request_.get(product.url, headers=headers)
            soup = BeautifulSoup(req.text, 'html.parser')
            title = soup.find('span', {'id': 'productTitle'}).text.strip()
            price = soup.find('span', {'class': 'a-price-whole'}).text.strip().replace(',', '').replace('₹', '').replace('.', '')
            last_product = ProductHistory.objects.filter(product_watch=product).order_by("-created_at").first()
            if last_product and str(last_product.price) == str(price):
                continue
            product.name = title
            product.save()
            ProductHistory.objects.create(product_watch=product, price=price)
    except Exception as e:
        print(f"[Error] {e}")
    print(f"[Info] Cron end at {datetime.now()}")