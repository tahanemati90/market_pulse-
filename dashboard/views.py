from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .models import Asset, PriceHistory

def get_history_price(history_item):
    """استخراج قیمت فارغ از اینکه اسم فیلد چی تعریف شده باشد"""
    for field_name in ['price_usd', 'price', 'value', 'close_price', 'current_price']:
        if hasattr(history_item, field_name):
            val = getattr(history_item, field_name)
            if val is not None:
                return float(val)
    return 0.0

def index(request):
    selected_symbol = request.GET.get('asset', 'BTC').upper()
    selected_currency = request.GET.get('currency', 'USD')
    lang = request.GET.get('lang', 'fa')

    assets = Asset.objects.all()

    context = {
        'assets': assets,
        'selected_symbol': selected_symbol,
        'selected_currency': selected_currency,
        'lang': lang,
    }
    return render(request, 'dashboard/index.html', context)

@require_GET
def live_chart_data(request, symbol="BTC"):
    """API دریافت داده‌های زنده برای چارت - کاملاً منعطف و ایمن"""
    symbol = symbol.upper()
    try:
        asset = Asset.objects.filter(symbol__iexact=symbol).first()
        if not asset:
            return JsonResponse({"status": "error", "message": f"نماد {symbol} یافت نشد."}, status=404)

        # تشخیص داینامیک فیلد زمان در مدل PriceHistory
        ph_fields = [f.name for f in PriceHistory._meta.get_fields()]
        time_field = 'timestamp' if 'timestamp' in ph_fields else ('created_at' if 'created_at' in ph_fields else None)

        # کوئری مستقیم روی PriceHistory بدون وابستگی به related_name
        order_by_col = f"-{time_field}" if time_field else "-id"
        qs = PriceHistory.objects.filter(asset=asset).order_by(order_by_col)[:30]
        history = list(reversed(qs))

        if not history:
            base_p = float(asset.base_price_usd) if hasattr(asset, 'base_price_usd') and asset.base_price_usd else 0.0
            return JsonResponse({
                "status": "success",
                "symbol": symbol,
                "labels": ["الان"],
                "prices": [base_p],
                "latest_price": f"{base_p:,.2f}",
                "pct_change": 0.0,
                "is_positive": True
            })

        # ساخت برچسب زمان
        if time_field:
            labels = [getattr(item, time_field).strftime('%H:%M:%S') for item in history]
        else:
            labels = [f"#{item.id}" for item in history]

        prices = [get_history_price(item) for item in history]

        latest_price = prices[-1]
        prev_price = prices[-2] if len(prices) > 1 else latest_price
        pct_change = ((latest_price - prev_price) / prev_price * 100) if prev_price > 0 else 0.0

        return JsonResponse({
            "status": "success",
            "symbol": symbol,
            "labels": labels,
            "prices": prices,
            "latest_price": f"{latest_price:,.2f}",
            "pct_change": round(pct_change, 2),
            "is_positive": pct_change >= 0,
        })
    except Exception as e:
        return JsonResponse({"status": "error", "message": f"خطای سرور: {str(e)}"}, status=500)
