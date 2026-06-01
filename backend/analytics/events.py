from django.core.cache import cache

class OrderEventDispatcher:
    @staticmethod
    def dispatch_order_created(store_id: str):
        """
        Invalidates the corresponding cache keys to avoid obsolete Data
        """
        # 1. Invalidate cache os specific tenant
        cache_key_tenant = f"dashboard_analytics_{store_id}"
        cache.delete(cache_key_tenant)

        # 2. Invalidate global cache pnale
        cache.delete("dashboard_analytics_global")
        
        print(f"📢 [Domain Event] Venta registrada. Caché destruida para Store: {store_id} y Global.")