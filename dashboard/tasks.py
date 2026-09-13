import requests
from celery import shared_task
from django.utils import timezone
from .models import Asset, PriceHistory

GECKO_MAP = {
    'BTC': 'bitcoin',
    'ETH': 'ethereum',
    'SOL': 'solana',
    'OIL': 'crude-oil',
    'GOLD': 'tether-gold',
}

@shared_task
def fetch_market_prices():
    """دریافت خودکار قیمت‌ها و ذخیره در PriceHistory بر اساس فیلدهای مدل"""
    assets = Asset.objects.all()
    if not assets.exists():
        return "هیچ دارایی یافت نشد."

    gecko_ids = [GECKO_MAP.get(a.symbol.upper(), a.symbol.lower()) for a in assets]
    ids_query = ",".join(set(gecko_ids))
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids_query}&vs_currencies=usd"

    # شناسایی داینامیک نام فیلد قیمت در مدل PriceHistory
    field_names = [f.name for f in PriceHistory._meta.get_fields()]
    price_field = next((f for f in ['price_usd', 'price', 'value', 'close_price', 'current_price'] if f in field_names), None)

    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            now = timezone.now()
            records = []

            for asset in assets:
                cg_id = GECKO_MAP.get(asset.symbol.upper(), asset.symbol.lower())
                if cg_id in data and 'usd' in data[cg_id]:
                    val = data[cg_id]['usd']
                    
                    # ساخت آبجکت متناسب با فیلدهای موجود در مدل دیتابیس
                    kwargs = {'asset': asset}
                    if 'timestamp' in field_names:
                        kwargs['timestamp'] = now
                    elif 'created_at' in field_names:
                        kwargs['created_at'] = now

                    if price_field:
                        kwargs[price_field] = val

                    records.append(PriceHistory(**kwargs))

            if records:
                PriceHistory.objects.bulk_create(records)
                return f"{len(records)} رکورد ذخیره شد (فیلد قیمت: {price_field})."
        return "پاسخ API خالی بود یا وضعیت ۲۰۰ نبود."
    except Exception as e:
        return f"خطا در پردازش: {str(e)}"
