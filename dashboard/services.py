import requests
import yfinance as yf
from .models import Asset, PriceHistory

def seed_initial_assets():
    """اگر دارایی‌ها در دیتابیس نبودند، اضافه شوند."""
    default_assets = [
        {'name_fa': 'بیت‌کوین', 'name_en': 'Bitcoin', 'symbol': 'BTC', 'asset_type': 'CRYPTO', 'base_price_usd': 60000.0},
        {'name_fa': 'اتریوم', 'name_en': 'Ethereum', 'symbol': 'ETH', 'asset_type': 'CRYPTO', 'base_price_usd': 3000.0},
        {'name_fa': 'طلای جهانی (اونس)', 'name_en': 'Gold Ounce', 'symbol': 'GOLD', 'asset_type': 'COMMODITY', 'base_price_usd': 2500.0},
        {'name_fa': 'نفت خام برنت', 'name_en': 'Brent Crude Oil', 'symbol': 'OIL', 'asset_type': 'COMMODITY', 'base_price_usd': 100.0},
    ]
    for item in default_assets:
        Asset.objects.get_or_create(
            symbol=item['symbol'],
            defaults={
                'name_fa': item['name_fa'],
                'name_en': item['name_en'],
                'asset_type': item['asset_type'],
                'base_price_usd': item['base_price_usd']
            }
        )

def fetch_and_update_prices():
    """دریافت زنده قیمت کریپتو از CoinGecko و کالاها (طلا و نفت) از Yahoo Finance"""
    seed_initial_assets()
    
    # 1. بروزرسانی کریپتو از CoinGecko
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            data = res.json()
            mapping = {
                'BTC': data.get('bitcoin', {}).get('usd'),
                'ETH': data.get('ethereum', {}).get('usd'),
            }
            for sym, price in mapping.items():
                if price:
                    asset = Asset.objects.filter(symbol=sym).first()
                    if asset:
                        asset.base_price_usd = float(price)
                        asset.save()
                        PriceHistory.objects.create(asset=asset, price_usd=price)
    except Exception as e:
        print(f"[CoinGecko Error] {e}")

    # 2. بروزرسانی نفت و طلا از Yahoo Finance
    # نماد BZ=F برای نفت برنت و GC=F برای طلای جهانی است
    commodities_map = {
        'OIL': 'BZ=F',
        'GOLD': 'GC=F'
    }
    
    for sym, ticker_symbol in commodities_map.items():
        try:
            ticker = yf.Ticker(ticker_symbol)
            # دریافت آخرین قیمت روز بازار
            price = ticker.fast_info.last_price
            if price:
                asset = Asset.objects.filter(symbol=sym).first()
                if asset:
                    asset.base_price_usd = round(float(price), 2)
                    asset.save()
                    PriceHistory.objects.create(asset=asset, price_usd=round(float(price), 2))
        except Exception as e:
            print(f"[YahooFinance Error for {sym}] {e}")
