from django.db import models

class Asset(models.Model):
    ASSET_TYPES = [
        ('CRYPTO', 'Cryptocurrency'),
        ('COMMODITY', 'Commodity'),
        ('FOREX', 'Forex / Currency'),
    ]
    
    symbol = models.CharField(max_length=20, unique=True) # مثلا BTC, CRUDE_OIL, GOLD
    name_en = models.CharField(max_length=100)              # Bitcoin
    name_fa = models.CharField(max_length=100)              # بیت‌کوین
    asset_type = models.CharField(max_length=20, choices=ASSET_TYPES, default='CRYPTO')
    base_price_usd = models.DecimalField(max_digits=18, decimal_places=4, default=0.0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name_en} ({self.symbol})"

class PriceHistory(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='history')
    price_usd = models.DecimalField(max_digits=18, decimal_places=4)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.asset.symbol} - ${self.price_usd} @ {self.timestamp}"

class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"
